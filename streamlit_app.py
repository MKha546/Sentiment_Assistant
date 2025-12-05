"""
Vietnamese Sentiment Assistant
Sử dụng PhoBERT qua pipeline sentiment-analysis để phân loại cảm xúc tiếng Việt.
"""

import os
import re
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

import streamlit as st
from transformers import pipeline

# Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sentiments.db")
MODEL_NAME = "wonrax/phobert-base-vietnamese-sentiment"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Khởi tạo database SQLite với bảng sentiments.
    Theo yêu cầu: id, text, sentiment, timestamp (ISO string YYYY-MM-DD HH:MM:SS)
    Tự động migrate schema nếu database cũ có schema khác.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Kiểm tra xem bảng có tồn tại không
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sentiments'")
        table_exists = cursor.fetchone()
        
        if table_exists:
            # Kiểm tra schema hiện tại
            cursor.execute("PRAGMA table_info(sentiments)")
            columns_info = cursor.fetchall()
            column_names = [col[1] for col in columns_info]
            
            # Nếu schema cũ (không có timestamp hoặc có text_input/created_at), migrate
            if 'timestamp' not in column_names or 'text' not in column_names:
                # Xóa bảng cũ và tạo lại với schema mới
                conn.execute("DROP TABLE IF EXISTS sentiments")
                conn.commit()
                table_exists = False
        
        # Tạo bảng mới với schema đúng (hoặc tạo nếu chưa tồn tại)
        if not table_exists:
            conn.execute(
                """
                CREATE TABLE sentiments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    sentiment TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
                """
            )
            conn.commit()
        else:
            # Đảm bảo bảng có đúng schema (CREATE IF NOT EXISTS)
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS sentiments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    sentiment TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
                """
            )
            conn.commit()


def save_history(text: str, sentiment: str):
    """
    Lưu lịch sử phân loại vào database.
    Sử dụng parameterized queries để tránh SQL injection.
    Timestamp format: YYYY-MM-DD HH:MM:SS (ISO string)
    
    Args:
        text: Câu đã nhập
        sentiment: Nhãn cảm xúc (POSITIVE/NEUTRAL/NEGATIVE)
    """
    # Tạo timestamp theo format ISO: YYYY-MM-DD HH:MM:SS
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with get_db_connection() as conn:
        # Sử dụng parameterized queries để tránh SQL injection
        conn.execute(
            """
            INSERT INTO sentiments (text, sentiment, timestamp)
            VALUES (?, ?, ?)
            """,
            (text, sentiment, timestamp),
        )
        conn.commit()


def fetch_history(limit: int = 50) -> List[Dict]:
    """
    Lấy lịch sử phân loại từ database.
    Theo yêu cầu: giới hạn 50 bản ghi mới nhất, ORDER BY timestamp DESC.
    
    Args:
        limit: Số lượng bản ghi cần lấy (mặc định 50)
        
    Returns:
        Danh sách dictionary chứa thông tin lịch sử
    """
    with get_db_connection() as conn:
        # Sử dụng parameterized queries và ORDER BY timestamp DESC LIMIT 50
        rows = conn.execute(
            """
            SELECT * FROM sentiments 
            ORDER BY timestamp DESC 
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [
            {
                "Câu nhập": row["text"],
                "Kết quả": map_sentiment_to_vietnamese(row["sentiment"]),  # Hiển thị tiếng Việt
                "Sentiment": row["sentiment"],  # Giữ format POSITIVE/NEUTRAL/NEGATIVE đầy đủ
                "Thời gian": row["timestamp"],  # Format: YYYY-MM-DD HH:MM:SS
            }
            for row in rows
        ]


# Text normalization dictionary
# Lưu ý: Thứ tự quan trọng - cụm từ dài hơn phải được xử lý trước
COMMON_REPLACEMENTS = {
    # Cụm từ cảm xúc đặc biệt (xử lý trước)
    "buồn cười": "hài hước",  # "buồn cười" = funny (positive), không phải buồn + cười
    "buon cuoi": "hài hước",
    "buồn cuời": "hài hước",
    
    # Từ viết tắt thông thường
    "rat": "rất",
    "hok": "không",
    "ko": "không",
    "k": "không",
    "khong": "không",
    "dc": "được",
    "duoc": "được",
    "bt": "bình thường",
    "oke": "ok",
    "ok": "ok",
    "vs": "với",
    "hong": "không",
    "bùn": "buồn",
}


def normalize_text(text: str) -> str:
    """
    Chuẩn hóa văn bản tiếng Việt: xử lý viết tắt, thiếu dấu, cụm từ đặc biệt.
    
    Args:
        text: Văn bản đầu vào
        
    Returns:
        Văn bản đã chuẩn hóa
    """
    cleaned = text.strip().lower()
    
    # Xử lý cụm từ đặc biệt trước (không dùng word boundary để match cụm từ)
    # Ví dụ: "buồn cười" -> "hài hước" (tích cực)
    special_phrases = {
        "buồn cười": "hài hước",
        "buon cuoi": "hài hước",
        "buồn cuời": "hài hước",
    }
    for phrase, replacement in special_phrases.items():
        cleaned = cleaned.replace(phrase, replacement)
    
    # Xử lý các từ đơn lẻ với word boundary
    for src, tgt in COMMON_REPLACEMENTS.items():
        # Bỏ qua các cụm từ đã xử lý ở trên
        if src not in special_phrases:
            cleaned = re.sub(rf"\b{re.escape(src)}\b", tgt, cleaned)
    
    return cleaned


def get_sentiment_label(label: str, score: float) -> str:
    """
    Chuyển đổi label từ model sang POSITIVE/NEUTRAL/NEGATIVE đầy đủ.
    Giữ nguyên logic cũ - chỉ map label, không thay đổi dựa trên score.
    
    Args:
        label: Label từ model (LABEL_0, LABEL_1, LABEL_2 hoặc POSITIVE/NEGATIVE/NEUTRAL)
        score: Độ tin cậy của prediction (không dùng để thay đổi kết quả)
        
    Returns:
        Label chuẩn đầy đủ: POSITIVE, NEUTRAL, hoặc NEGATIVE
    """
    # Mapping từ label model sang POSITIVE/NEUTRAL/NEGATIVE đầy đủ
    # Xử lý nhiều format có thể có từ model
    mapping = {
        "LABEL_0": "NEGATIVE",
        "LABEL_1": "NEUTRAL", 
        "LABEL_2": "POSITIVE",
        "NEGATIVE": "NEGATIVE",
        "NEUTRAL": "NEUTRAL",
        "POSITIVE": "POSITIVE",
        "negative": "NEGATIVE",
        "neutral": "NEUTRAL",
        "positive": "POSITIVE",
        "NEG": "NEGATIVE",
        "POS": "POSITIVE",
        "neg": "NEGATIVE",
        "pos": "POSITIVE",
    }
    
    # Nếu label rỗng hoặc không tìm thấy, kiểm tra score để quyết định
    if not label or label not in mapping:
        # Nếu không tìm thấy trong mapping, thử parse từ label string
        label_upper = label.upper() if label else ""
        if "POS" in label_upper or "TÍCH CỰC" in label_upper or "TICH CUC" in label_upper:
            return "POSITIVE"
        elif "NEG" in label_upper or "TIÊU CỰC" in label_upper or "TIEU CUC" in label_upper:
            return "NEGATIVE"
        elif "NEU" in label_upper or "TRUNG TÍNH" in label_upper or "TRUNG TINH" in label_upper:
            return "NEUTRAL"
        else:
            # Mặc định trả về NEUTRAL nếu không xác định được
            return "NEUTRAL"
    
    # Giữ nguyên kết quả từ model, chỉ đảm bảo format đầy đủ
    return mapping.get(label, "NEUTRAL")


def map_sentiment_to_vietnamese(sentiment: str) -> str:
    """
    Chuyển đổi sentiment (POSITIVE/NEUTRAL/NEGATIVE) sang tiếng Việt để hiển thị.
    
    Args:
        sentiment: POSITIVE, NEUTRAL, hoặc NEGATIVE
        
    Returns:
        Label tiếng Việt tương ứng
    """
    mapping = {
        "POSITIVE": "Tích cực",
        "NEUTRAL": "Trung tính",
        "NEGATIVE": "Tiêu cực",
    }
    return mapping.get(sentiment, sentiment)


# Danh sách từ cảm xúc được phép nhập 1 từ
EMOTION_WORDS = {
    "vui", "buồn", "chán", "cười", "buon", "chan", "cuoi",
    "vui vẻ", "buồn bã", "chán nản", "cười vui",
    "hạnh phúc", "tức giận", "sợ hãi", "ngạc nhiên",
    "yêu", "ghét", "thích", "không thích"
}


@st.cache_resource(show_spinner=True)
def load_classifier():
    """
    Tải model PhoBERT qua pipeline sentiment-analysis.
    Model được cache để không tải lại mỗi lần chạy.
    
    Returns:
        Pipeline sentiment-analysis đã được load
    """
    return pipeline(
        "sentiment-analysis",
        model=MODEL_NAME,
        device=-1,  # CPU; dùng 0 nếu có GPU
    )


def main():
    """Hàm chính của ứng dụng Streamlit."""
    st.set_page_config(
        page_title="Vietnamese Sentiment Assistant",
        page_icon="😊",
        layout="centered"
    )
    st.title("Trợ lý phân loại cảm xúc tiếng Việt")
    #st.markdown("**Sử dụng PhoBERT qua pipeline sentiment-analysis**")
    #st.caption("Model: `wonrax/phobert-base-vietnamese-sentiment`")

    init_db()
    classifier = load_classifier()

    text_input = st.text_area("Nhập câu tiếng Việt", height=150, placeholder="Ví dụ: Hôm nay tôi rất vui")
    col1, col2 = st.columns([1, 2])

    with col1:
        run_btn = st.button("Phân loại", use_container_width=True, type="primary")

    error_box = st.empty()
    result_box = st.empty()

    if run_btn:
        error_box.empty()
        result_box.empty()

        # ============================================
        # INPUT: Đầu vào - Câu tiếng Việt
        # ============================================
        text = (text_input or "").strip()
        
        # ============================================
        # COMPONENT 3: Hợp nhất & xử lý lỗi (Validation)
        # Kiểm tra đầu vào hợp lệ
        # ============================================
        # Kiểm tra 1: Không có nội dung
        if not text:
            error_box.error("⚠️ Vui lòng nhập câu cần phân tích!")
            return
        
        # Kiểm tra 2: Đếm số từ và kiểm tra từ cảm xúc
        words = text.split()
        word_count = len([w for w in words if w.strip()])  # Đếm từ không rỗng
        
        if word_count < 2:
            # Nếu chỉ có 1 từ, kiểm tra xem có phải từ cảm xúc không
            if word_count == 1:
                single_word = text.strip().lower()
                # Kiểm tra xem từ này có trong danh sách từ cảm xúc không
                if single_word not in EMOTION_WORDS:
                    error_box.error("⚠️ Vui lòng nhập ít nhất 2 từ hoặc một từ cảm xúc! Ví dụ: 'Tôi vui', 'Hôm nay tôi rất vui', hoặc 'vui', 'buồn', 'chán', 'cười'")
                    return
                # Nếu là từ cảm xúc, cho phép tiếp tục
            else:
                error_box.error("⚠️ Vui lòng nhập đầy đủ câu có ít nhất 2 từ!")
                return
        
        # Kiểm tra 3: Độ dài tối thiểu
        if len(text) < 2:
            error_box.error("⚠️ Câu quá ngắn, vui lòng nhập câu đầy đủ hơn!")
            return
        
        # ============================================
        # COMPONENT 1: Tiền xử lý (Preprocessing)
        # Chuẩn hóa câu tiếng Việt
        # ============================================
        normalized = normalize_text(text)
        
        # ============================================
        # COMPONENT 2: Phân loại cảm xúc (Sentiment Analysis)
        # Sử dụng Transformer pipeline để phân loại
        # ============================================
        try:
            with st.spinner("Đang phân tích..."):
                res = classifier(normalized)
                
                # Xử lý kết quả từ pipeline
                if isinstance(res, list):
                    if res:
                        res = res[0]
                    else:
                        raise ValueError("Không nhận được kết quả từ model!")
                
                # Lấy label và score từ model
                label = res.get("label", "")
                score = float(res.get("score", 0.0))
                
                # Chuyển đổi label sang format POSITIVE/NEUTRAL/NEGATIVE
                sentiment = get_sentiment_label(label, score)
                
        except Exception as e:
            # COMPONENT 3: Xử lý lỗi
            error_box.error(f"Lỗi khi phân tích: {str(e)}")
            return
        
        # ============================================
        # COMPONENT 3: Hợp nhất & xử lý lỗi (Validation)
        # Tạo dictionary output theo đúng format yêu cầu
        # ============================================
        result_dict = {
            "text": text,
            "sentiment": sentiment
        }
        
        # ============================================
        # CORE ENGINE: Lưu & hiển thị
        # ============================================
        # Lưu vào database (chỉ lưu text và sentiment theo yêu cầu)
        save_history(text=text, sentiment=sentiment)
        
        # Chuyển sang tiếng Việt để hiển thị
        vietnamese_label = map_sentiment_to_vietnamese(sentiment)
        
        # Hiển thị kết quả
        color = "#10b981" if sentiment == "POSITIVE" else "#ef4444" if sentiment == "NEGATIVE" else "#6b7280"
        icon = "😊" if sentiment == "POSITIVE" else "😞" if sentiment == "NEGATIVE" else "😐"
        
        result_box.markdown(
            f"<div style='padding:12px;border-radius:10px;background:#f3f4f6;'>"
            f"<div style='font-size:18px;font-weight:700;color:{color};'>{icon} {vietnamese_label} ({sentiment})</div>"
            f"<div style='margin-top:4px;'>Độ tin cậy: {round(score*100, 2)}%</div>"
            f"<div style='margin-top:4px;color:#374151;'>Câu (chuẩn hóa): {normalized}</div>"
            f"</div>",
            unsafe_allow_html=True, 
        )
        
        # Hiển thị dictionary output theo đúng format yêu cầu
        st.json(result_dict)

    st.subheader("Lịch sử phân loại")
    # Hiển thị 50 bản ghi mới nhất theo yêu cầu
    history = fetch_history(limit=50)
    if history:
        st.table(history)
    else:
        st.info("Chưa có lịch sử. Hãy nhập câu để bắt đầu.")


if __name__ == "__main__":
    main()

