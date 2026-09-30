/*
 * ============================================================
 * SatiARM ESP32 Firmware v1.0
 * 5-Finger Robotic Hand + FSR Feedback
 * ============================================================
 * Hardware:
 *   - 5x Servo (SG90/MG90S)
 *   - 5x FSR at fingertips
 *   - LED status
 * Serial Commands (115200 baud):
 *   1) Manual  2) FSR Monitor  3) Breathing
 *   4) Adaptive  5) Calibrate  6) Status  7) Reset
 *   T/I/M/R/P<angle>  A<angle>  B<ms>  X<thr>  S  ?
 * ============================================================
 */
#include <ESP32Servo.h>

#define PIN_SERVO_THUMB   13
#define PIN_SERVO_INDEX   12
#define PIN_SERVO_MIDDLE  14
#define PIN_SERVO_RING    27
#define PIN_SERVO_PINKY   26

#define PIN_FSR_THUMB     34
#define PIN_FSR_INDEX     35
#define PIN_FSR_MIDDLE    32
#define PIN_FSR_RING      33
#define PIN_FSR_PINKY     25

#define PIN_LED           2

Servo sThumb, sIndex, sMiddle, sRing, sPinky;

int fsrThreshold = 600;
int breathPeriodMs = 8000;
int servoMin = 0;
int servoMax = 180;

enum Mode { MODE_IDLE, MODE_BREATH, MODE_ADAPTIVE, MODE_MANUAL };
Mode currentMode = MODE_IDLE;

unsigned long lastBreathMs = 0;
float curlAmount = 0.0;
int fsrValues[5] = {0, 0, 0, 0, 0};

void setup() {
  Serial.begin(115200);
  delay(500);
  pinMode(PIN_LED, OUTPUT);
  digitalWrite(PIN_LED, LOW);

  sThumb.attach(PIN_SERVO_THUMB);
  sIndex.attach(PIN_SERVO_INDEX);
  sMiddle.attach(PIN_SERVO_MIDDLE);
  sRing.attach(PIN_SERVO_RING);
  sPinky.attach(PIN_SERVO_PINKY);

  setAllServos(0);
  printWelcome();
  printMenu();
}

void loop() {
  handleSerial();
  if (currentMode == MODE_BREATH) updateBreathing();
  else if (currentMode == MODE_ADAPTIVE) updateAdaptive();
  else if (currentMode == MODE_MANUAL) readAllFSR();
}

void handleSerial() {
  if (!Serial.available()) return;
  String line = Serial.readStringUntil('\n');
  line.trim();
  if (line.length() == 0) return;

  char cmd = line.charAt(0);
  String arg = line.substring(1);
  arg.trim();

  switch (cmd) {
    case '1': enterBreathMode(); break;
    case '2': enterFSRMode(); break;
    case '3': enterBreathMode(); break;
    case '4': enterAdaptiveMode(); break;
    case '5': calibrateFSR(); break;
    case '6': printStatus(); break;
    case '7': resetSystem(); break;
    case 'T': setServo(sThumb, arg.toInt(), "Thumb"); break;
    case 'I': setServo(sIndex, arg.toInt(), "Index"); break;
    case 'M': setServo(sMiddle, arg.toInt(), "Middle"); break;
    case 'R': setServo(sRing, arg.toInt(), "Ring"); break;
    case 'P': setServo(sPinky, arg.toInt(), "Pinky"); break;
    case 'A':
      setAllServos(arg.toInt());
      Serial.print("[OK] All servos -> "); Serial.println(arg);
      break;
    case 'B':
      breathPeriodMs = arg.toInt();
      Serial.print("[OK] Breath period = "); Serial.println(breathPeriodMs);
      break;
    case 'X':
      fsrThreshold = arg.toInt();
      Serial.print("[OK] FSR threshold = "); Serial.println(fsrThreshold);
      break;
    case 'S': printFSR(); break;
    case '?': printMenu(); break;
    default:
      Serial.print("[ERR] Unknown: "); Serial.println(line);
  }
}

void enterBreathMode() {
  currentMode = MODE_BREATH;
  lastBreathMs = millis();
  digitalWrite(PIN_LED, HIGH);
  Serial.println("[MODE] Breathing Guide");
  Serial.print("[INFO] Period = "); Serial.print(breathPeriodMs); Serial.println(" ms");
}

void enterFSRMode() {
  currentMode = MODE_IDLE;
  digitalWrite(PIN_LED, LOW);
  Serial.println("[MODE] FSR Monitor");
  printFSR();
}

void enterAdaptiveMode() {
  currentMode = MODE_ADAPTIVE;
  lastBreathMs = millis();
  digitalWrite(PIN_LED, HIGH);
  Serial.println("[MODE] Adaptive Grasp");
}

void resetSystem() {
  currentMode = MODE_IDLE;
  setAllServos(0);
  digitalWrite(PIN_LED, LOW);
  Serial.println("[OK] Reset");
  printMenu();
}

void updateBreathing() {
  unsigned long now = millis();
  float phase = 2.0 * PI * ((now - lastBreathMs) % breathPeriodMs) / breathPeriodMs;
  float breath = sin(phase);
  curlAmount = 0.5 + 0.5 * breath;

  int angle = (int)(curlAmount * 180);
  setAllServosAdaptive(angle);

  static unsigned long lastReport = 0;
  if (now - lastReport > 500) {
    lastReport = now;
    Serial.print("[BREATH] ");
    Serial.print(breath >= 0 ? "INHALE" : "EXHALE");
    Serial.print(" curl="); Serial.print(curlAmount, 3);
    Serial.print(" angle="); Serial.println(angle);
  }
}

void updateAdaptive() {
  unsigned long now = millis();
  float phase = 2.0 * PI * ((now - lastBreathMs) % breathPeriodMs) / breathPeriodMs;
  float breath = sin(phase);
  float baseCurl = 0.5 + 0.5 * breath;

  readAllFSR();
  int maxFSR = 0;
  for (int i = 0; i < 5; i++) if (fsrValues[i] > maxFSR) maxFSR = fsrValues[i];

  float curl = baseCurl;
  if (maxFSR > fsrThreshold) {
    float excess = (float)(maxFSR - fsrThreshold) / (1023.0 - fsrThreshold);
    curl = baseCurl * (1.0 - 0.7 * excess);
    if (curl < 0) curl = 0;
  }

  int angle = (int)(curl * 180);
  setAllServosAdaptive(angle);

  static unsigned long lastReport = 0;
  if (now - lastReport > 500) {
    lastReport = now;
    Serial.print("[ADAPTIVE] maxFSR="); Serial.print(maxFSR);
    Serial.print(" curl="); Serial.print(curl, 3);
    Serial.print(" angle="); Serial.println(angle);
  }
}

void setServo(Servo &s, int angle, const char* name) {
  if (angle < servoMin) angle = servoMin;
  if (angle > servoMax) angle = servoMax;
  s.write(angle);
  Serial.print("[OK] "); Serial.print(name); Serial.print(" -> "); Serial.print(angle); Serial.println(" deg");
}

void setAllServos(int angle) {
  if (angle < servoMin) angle = servoMin;
  if (angle > servoMax) angle = servoMax;
  sThumb.write(angle); sIndex.write(angle); sMiddle.write(angle);
  sRing.write(angle); sPinky.write(angle);
}

void setAllServosAdaptive(int angle) {
  sThumb.write((int)(angle * 0.85));
  sIndex.write(angle);
  sMiddle.write(angle);
  sRing.write((int)(angle * 0.95));
  sPinky.write((int)(angle * 0.85));
}

void readAllFSR() {
  fsrValues[0] = analogRead(PIN_FSR_THUMB);
  fsrValues[1] = analogRead(PIN_FSR_INDEX);
  fsrValues[2] = analogRead(PIN_FSR_MIDDLE);
  fsrValues[3] = analogRead(PIN_FSR_RING);
  fsrValues[4] = analogRead(PIN_FSR_PINKY);
}

void printFSR() {
  readAllFSR();
  Serial.println("[FSR]");
  Serial.print("  Thumb:  "); Serial.println(fsrValues[0]);
  Serial.print("  Index:  "); Serial.println(fsrValues[1]);
  Serial.print("  Middle: "); Serial.println(fsrValues[2]);
  Serial.print("  Ring:   "); Serial.println(fsrValues[3]);
  Serial.print("  Pinky:  "); Serial.println(fsrValues[4]);
}

void calibrateFSR() {
  Serial.println("[CAL] Hold fingers at rest 3s...");
  delay(3000);
  long sum[5] = {0, 0, 0, 0, 0};
  for (int i = 0; i < 20; i++) {
    readAllFSR();
    for (int j = 0; j < 5; j++) sum[j] += fsrValues[j];
    delay(50);
  }
  Serial.println("[CAL] Baseline:");
  for (int j = 0; j < 5; j++) {
    Serial.print("  Finger "); Serial.print(j);
    Serial.print(": "); Serial.println(sum[j] / 20);
  }
  Serial.println("[CAL] Done");
}

void printWelcome() {
  Serial.println();
  Serial.println("============================================================");
  Serial.println("  SatiARM ESP32 Firmware v1.0");
  Serial.println("  5-Finger Robotic Hand + FSR Feedback");
  Serial.println("============================================================");
}

void printMenu() {
  Serial.println();
  Serial.println("--- MENU ---");
  Serial.println(" 1) Manual  2) FSR Monitor  3) Breathing");
  Serial.println(" 4) Adaptive  5) Calibrate  6) Status  7) Reset");
  Serial.println("Commands: T/I/M/R/P<a>  A<a>  B<ms>  X<thr>  S  ?");
  Serial.println();
}

void printStatus() {
  Serial.println("[STATUS]");
  Serial.print("  Mode: ");
  switch (currentMode) {
    case MODE_IDLE: Serial.println("IDLE"); break;
    case MODE_BREATH: Serial.println("BREATH"); break;
    case MODE_ADAPTIVE: Serial.println("ADAPTIVE"); break;
    case MODE_MANUAL: Serial.println("MANUAL"); break;
  }
  Serial.print("  Threshold: "); Serial.println(fsrThreshold);
  Serial.print("  Breath period: "); Serial.println(breathPeriodMs);
  printFSR();
}
