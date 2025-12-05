# 📚 Hướng Dẫn Upload Project Lên GitHub

## 🎯 Mục Tiêu
Upload source code của **Vietnamese Sentiment Assistant** lên GitHub repository.

---

## 📋 Bước 1: Chuẩn Bị

### 1.1. Tạo tài khoản GitHub (nếu chưa có)
- Truy cập: https://github.com
- Đăng ký tài khoản mới hoặc đăng nhập

### 1.2. Cài đặt Git (nếu chưa có)
Kiểm tra Git đã cài đặt:
```bash
git --version
```

Nếu chưa có, tải về: https://git-scm.com/downloads

---

## 📋 Bước 2: Tạo Repository Trên GitHub

1. **Đăng nhập GitHub** → Click nút **"+"** (góc trên bên phải) → Chọn **"New repository"**

2. **Điền thông tin:**
   - **Repository name**: `Sentiment_Assistant` (hoặc tên bạn muốn)
   - **Description**: "Vietnamese Sentiment Analysis using PhoBERT"
   - **Visibility**: 
     - ✅ **Public** (mọi người có thể xem)
     - 🔒 **Private** (chỉ bạn xem được)
   - **⚠️ KHÔNG** tích vào "Initialize with README" (vì đã có code sẵn)

3. Click **"Create repository"**

4. **Copy URL repository** (sẽ có dạng: `https://github.com/username/Sentiment_Assistant.git`)

---

## 📋 Bước 3: Khởi Tạo Git Repository (Local)

Mở **PowerShell** hoặc **Command Prompt** tại thư mục project:

```bash
# Di chuyển vào thư mục project
cd D:\Workspace\python\Sentiment_Assistant

# Khởi tạo git repository
git init

# Kiểm tra trạng thái
git status
```

---

## 📋 Bước 4: Cấu Hình Git (Lần Đầu Tiên)

Nếu chưa cấu hình Git, chạy các lệnh sau:

```bash
# Cấu hình tên (thay bằng tên của bạn)
git config --global user.name "Your Name"

# Cấu hình email (thay bằng email GitHub của bạn)
git config --global user.email "your.email@example.com"
```

---

## 📋 Bước 5: Thêm Files Vào Git

```bash
# Thêm tất cả files (trừ những file trong .gitignore)
git add .

# Kiểm tra files đã được thêm
git status
```

**Lưu ý:** File `.gitignore` đã được tạo để loại trừ:
- `venv/` (virtual environment)
- `*.db` (database files)
- `__pycache__/` (Python cache)
- Các file không cần thiết khác

---

## 📋 Bước 6: Commit Code

```bash
# Tạo commit đầu tiên
git commit -m "Initial commit: Vietnamese Sentiment Assistant"

# Hoặc commit với message chi tiết hơn
git commit -m "Initial commit: Vietnamese Sentiment Analysis using PhoBERT and Streamlit"
```

---

## 📋 Bước 7: Kết Nối Với GitHub Repository

```bash
# Thêm remote repository (thay URL bằng URL repository của bạn)
git remote add origin https://github.com/username/Sentiment_Assistant.git

# Kiểm tra remote đã được thêm
git remote -v
```

**Lưu ý:** 
- Thay `username` bằng username GitHub của bạn
- Thay `Sentiment_Assistant` bằng tên repository bạn đã tạo

---

## 📋 Bước 8: Push Code Lên GitHub

```bash
# Push code lên GitHub (lần đầu tiên)
git branch -M main
git push -u origin main
```

**Nếu gặp lỗi authentication:**
- GitHub yêu cầu **Personal Access Token** thay vì password
- Xem hướng dẫn tạo token ở **Bước 9**

---

## 📋 Bước 9: Tạo Personal Access Token (Nếu Cần)

Nếu Git yêu cầu username/password:

1. **GitHub** → Click **avatar** (góc trên phải) → **Settings**

2. **Developer settings** → **Personal access tokens** → **Tokens (classic)**

3. Click **"Generate new token"** → **"Generate new token (classic)"**

4. **Điền thông tin:**
   - **Note**: "Sentiment Assistant Project"
   - **Expiration**: Chọn thời hạn (ví dụ: 90 days)
   - **Scopes**: Tích vào **`repo`** (full control of private repositories)

5. Click **"Generate token"**

6. **Copy token** (chỉ hiển thị 1 lần, lưu lại!)

7. Khi Git hỏi password, **paste token** thay vì password

---

## 📋 Bước 10: Kiểm Tra Kết Quả

1. Truy cập repository trên GitHub: `https://github.com/username/Sentiment_Assistant`

2. Kiểm tra:
   - ✅ Files đã được upload
   - ✅ Code hiển thị đúng
   - ✅ `.gitignore` hoạt động (không thấy `venv/`, `*.db`)

---

## 🔄 Cập Nhật Code Sau Này

Khi có thay đổi code, chạy các lệnh sau:

```bash
# Xem thay đổi
git status

# Thêm files đã thay đổi
git add .

# Commit với message mô tả thay đổi
git commit -m "Mô tả thay đổi: ví dụ 'Fix normalization function'"

# Push lên GitHub
git push
```

---

## 📝 Tạo README.md (Tùy Chọn)

Để project chuyên nghiệp hơn, tạo file `README.md`:

```markdown
# Vietnamese Sentiment Assistant

Ứng dụng phân loại cảm xúc tiếng Việt sử dụng PhoBERT và Streamlit.

## Tính Năng

- Phân loại cảm xúc: POSITIVE, NEUTRAL, NEGATIVE
- Xử lý tiếng Việt: viết tắt, thiếu dấu
- Lưu lịch sử phân loại vào SQLite
- Giao diện Streamlit thân thiện

## Cài Đặt

```bash
pip install -r requirements.txt
```

## Chạy Ứng Dụng

```bash
streamlit run streamlit_app.py
```

## Model

- Model: `wonrax/phobert-base-vietnamese-sentiment`
- Framework: Hugging Face Transformers
```

---

## ⚠️ Lưu Ý Quan Trọng

1. **KHÔNG commit:**
   - `venv/` (virtual environment)
   - `*.db` (database files)
   - `__pycache__/` (Python cache)
   - File `.env` chứa secrets

2. **NÊN commit:**
   - `streamlit_app.py` (source code)
   - `requirements.txt` (dependencies)
   - `.gitignore` (git ignore rules)
   - `README.md` (documentation)

3. **Database:**
   - File `sentiments.db` sẽ **KHÔNG** được commit (đã có trong `.gitignore`)
   - Database sẽ được tạo tự động khi chạy ứng dụng

---

## 🆘 Xử Lý Lỗi Thường Gặp

### Lỗi: "fatal: not a git repository"
```bash
# Chạy lại: git init
git init
```

### Lỗi: "remote origin already exists"
```bash
# Xóa remote cũ
git remote remove origin

# Thêm lại remote
git remote add origin https://github.com/username/Sentiment_Assistant.git
```

### Lỗi: "failed to push some refs"
```bash
# Pull code từ GitHub trước
git pull origin main --allow-unrelated-histories

# Sau đó push lại
git push -u origin main
```

### Lỗi: Authentication failed
- Kiểm tra Personal Access Token đã tạo chưa
- Đảm bảo token có quyền `repo`

---

## ✅ Checklist

Trước khi push, đảm bảo:

- [ ] Đã tạo repository trên GitHub
- [ ] Đã tạo file `.gitignore`
- [ ] Đã chạy `git init`
- [ ] Đã chạy `git add .`
- [ ] Đã chạy `git commit`
- [ ] Đã thêm remote `origin`
- [ ] Đã push code lên GitHub
- [ ] Đã kiểm tra code trên GitHub

---

## 🎉 Hoàn Thành!

Sau khi hoàn thành các bước trên, code của bạn đã được upload lên GitHub!

**URL Repository:** `https://github.com/username/Sentiment_Assistant`

---

## 📚 Tài Liệu Tham Khảo

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [GitHub Authentication](https://docs.github.com/en/authentication)

