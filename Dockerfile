FROM python:3.9-slim

WORKDIR /app

# 必要なパッケージのインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードのコピー
COPY . .
COPY templates /app/templates
# 環境変数の設定
ENV FLASK_PORT=5000
ENV STREAMLIT_PORT=8501
ENV CTF_PORT=5001
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1

# ポートの公開
EXPOSE 5000 8501 8502 5001

# 実行権限の付与
RUN chmod +x *.py

# アプリケーションの実行
CMD ["bash", "-c", "python main.py & python ctf.py"]
