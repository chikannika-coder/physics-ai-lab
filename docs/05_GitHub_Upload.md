# 🐙 วิธีนำขึ้น GitHub

> **เวลา:** 15-20 นาที | **ระดับ:** ผู้เริ่มต้น

---

## 📋 สิ่งที่ต้องมี

| รายการ | ลิงก์ |
|--------|-------|
| GitHub account | github.com/signup |
| Git | git-scm.com |

---

## 📥 ขั้นที่ 1: สร้างบัญชี GitHub

1. ไปที่ github.com/signup
2. กรอก Email, Password, Username
3. ยืนยัน Email

---

## 📥 ขั้นที่ 2: สร้าง Repository

1. คลิก + มุมขวาบน -> New repository
2. กรอก:
   - Repository name: physics-ai-lab
   - Description: AI for Physics Education
   - Visibility: Public
   - อย่าติ๊ก Initialize
3. คลิก Create repository

---

## 📥 ขั้นที่ 3: ตั้งค่า Git

```bash
git config --global user.name "chikannika"
git config --global user.email "email@example.com"
```

---

## 📥 ขั้นที่ 4: Init + Commit

```bash
cd "D:\ai ด้านฟิสิกส์"
git init
git add .
git commit -m "Initial commit: Physics AI Lab v5"
git branch -M main
```

---

## 📥 ขั้นที่ 5: เชื่อม GitHub

```bash
git remote add origin https://github.com/chikannika/physics-ai-lab.git
```

ตรวจสอบ:
```bash
git remote -v
```

---

## 📥 ขั้นที่ 6: สร้าง Personal Access Token

1. ไปที่ github.com/settings/tokens
2. Generate new token -> Classic
3. Note: physics-ai-lab
4. Expiration: 90 days
5. Scopes: ติ๊ก repo + workflow
6. Generate token
7. Copy token ทันที (ghp_xxxx...)

---

## 📥 ขั้นที่ 7: Push

```bash
git push -u origin main
```

GitHub จะถาม:
- Username: chikannika
- Password: ใช้ token (ไม่ใช่ password จริง)

---

## 📥 ขั้นที่ 8: ตรวจสอบ

เปิด: https://github.com/chikannika/physics-ai-lab

---

## 🔄 อัปเดตในอนาคต

```bash
git add .
git commit -m "Update"
git push
```

---

## 🐛 Troubleshooting

| Error | วิธีแก้ |
|-------|--------|
| Repository not found | สร้าง repo ก่อน |
| Permission denied | ใช้ PAT แทน password |
| Failed to push | git pull origin main --rebase |

---

**Version:** 1.0.0 | **Last Updated:** 2026-09-30