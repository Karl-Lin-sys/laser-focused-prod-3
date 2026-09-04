# 軽量化とビルド速度向上のためのマルチステージビルド
FROM python:3.11-slim AS builder

WORKDIR /build

COPY requirements.txt .
# pip自体のアップグレードと、ネットワーク遅延によるタイムアウト(ReadTimeoutError)を防ぐための設定追加
RUN pip install --upgrade pip && \
    pip install --default-timeout=1000 --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

# builderステージからインストール済みのパッケージをコピー
COPY --from=builder /root/.local /root/.local
COPY . /app

# パスを通す
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# アプリケーションの実行
CMD ["python", "app/app.py"]
