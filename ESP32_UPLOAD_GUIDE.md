# ESP32 Firmware Upload Guide

## อุปกรณ์
- ESP32 DevKit
- Servo 5 ตัว (SG90/MG90S)
- FSR 5 ตัว

## 1. Arduino IDE
https://www.arduino.cc/en/software

## 2. ESP32 Board
File > Preferences > Additional Boards URLs:
https://espressif.github.io/arduino-esp32/package_esp32_index.json

Tools > Board > Boards Manager > esp32 > Install

## 3. Library
Tools > Manage Libraries > ESP32Servo

## 4. Pinout
| Servo | Pin | FSR | Pin |
|-------|-----|-----|-----|
| Thumb | 13 | Thumb | 34 |
| Index | 12 | Index | 35 |
| Middle | 14 | Middle | 32 |
| Ring | 27 | Ring | 33 |
| Pinky | 26 | Pinky | 25 |

## 5. Power
- Servo VCC -> 5V ภายนอก
- GND ร่วมกัน
- FSR: 3.3V - FSR - GPIO - 10k - GND

## 6. Upload
Tools > Board: ESP32 Dev Module > Port: COM_X > Upload

## 7. Serial Monitor 115200
เมนู 1-7 + commands: T/I/M/R/P/A/B/X/S/?
