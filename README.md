# 😊 Vietnamese Sentiment Assistant

Ứng dụng phân loại cảm xúc tiếng Việt sử dụng **PhoBERT** và **Streamlit**.

## ✨ Tính Năng

- 🎯 **Phân loại cảm xúc**: POSITIVE, NEUTRAL, NEGATIVE
- 🇻🇳 **Xử lý tiếng Việt**: Hỗ trợ viết tắt, thiếu dấu, cụm từ đặc biệt
- 💾 **Lưu lịch sử**: Lưu lịch sử phân loại vào SQLite database
- 🎨 **Giao diện thân thiện**: Streamlit UI đẹp mắt, dễ sử dụng
- 🔄 **Chuẩn hóa văn bản**: Tự động chuẩn hóa văn bản tiếng Việt

## 🚀 Cài Đặt

### Yêu Cầu

- Python 3.8+
- pip

### Bước 1: Clone Repository

```bash
git clone https://github.com/username/Sentiment_Assistant.git
cd Sentiment_Assistant
```

### Bước 2: Tạo Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Bước 3: Cài Đặt Dependencies

```bash
pip install -r requirements.txt
```

## 🎮 Chạy Ứng Dụng

```bash
streamlit run streamlit_app.py
```

Ứng dụng sẽ mở tự động tại: `http://localhost:8501`

## 📊 Model

- **Model**: `wonrax/phobert-base-vietnamese-sentiment`
- **Framework**: Hugging Face Transformers
- **Pipeline**: `sentiment-analysis`
- **Architecture**: PhoBERT (Vietnamese RoBERTa)

## 🏗️ Kiến Trúc

```
Input Text (Tiếng Việt)
    ↓
Preprocessing (Chuẩn hóa văn bản)
    ↓
Sentiment Analysis (PhoBERT Pipeline)
    ↓
Output: {"text": "...", "sentiment": "POSITIVE"}
    ↓
Save to SQLite Database
```

## 📁 Cấu Trúc Project

```
Sentiment_Assistant/
├── streamlit_app.py      # Ứng dụng chính
├── requirements.txt      # Dependencies
├── .gitignore           # Git ignore rules
├── README.md            # File này
└── sentiments.db        # SQLite database (tự động tạo)
```

## 💡 Ví Dụ Sử Dụng

1. **Nhập câu tiếng Việt** vào ô text area
2. Click nút **"Phân loại"**
3. Xem kết quả:
   - Nhãn cảm xúc: Tích cực / Trung tính / Tiêu cực
   - Độ tin cậy (%)
   - Câu đã chuẩn hóa
   - Dictionary output: `{"text": "...", "sentiment": "POSITIVE"}`

## 🔧 Tính Năng Xử Lý Tiếng Việt

- **Chuẩn hóa viết tắt**: "rat" → "rất", "ko" → "không"
- **Xử lý cụm từ đặc biệt**: "buồn cười" → "hài hước"
- **Hỗ trợ thiếu dấu**: Tự động xử lý văn bản không dấu

## 📝 Format Output

```json
{
  "text": "Hôm nay tôi rất vui",
  "sentiment": "POSITIVE"
}
```

## 🗄️ Database

- **SQLite**: `sentiments.db`
- **Bảng**: `sentiments`
- **Cột**: `id`, `text`, `sentiment`, `timestamp`
- **Lịch sử**: Hiển thị 50 bản ghi mới nhất

## 🛠️ Dependencies

- `streamlit>=1.29.0` - Web framework
- `transformers>=4.35.0` - Hugging Face Transformers
- `torch>=2.1.0` - PyTorch
- `sentencepiece>=0.1.99` - Tokenization
- `protobuf>=4.25.0` - Protocol buffers

## 📚 Tài Liệu

- Xem file `HUONG_DAN_GITHUB.md` để biết cách upload project lên GitHub
- Xem file `THEORY.md` (nếu có) để biết thêm về lý thuyết Transformer

## 🤝 Đóng Góp

Mọi đóng góp đều được chào đón! Vui lòng:

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit thay đổi (`git commit -m 'Add some AmazingFeature'`)
4. Push lên branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## 📄 License

Project này được phát hành dưới MIT License.

## 👤 Tác Giả

[Your Name]

## 🙏 Cảm Ơn

- **VinAI Research** - PhoBERT model
- **Hugging Face** - Transformers library
- **Streamlit** - Web framework

---

⭐ Nếu project này hữu ích, hãy cho một star! ⭐

