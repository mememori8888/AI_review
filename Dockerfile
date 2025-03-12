# ベースイメージとしてPython 3.9を使用
FROM python:3.9-slim-buster

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコードをコピー
COPY . .

# 環境変数を設定 (APIキーは環境変数として渡すことを推奨)
ENV GOOGLE_API_KEY="AIzaSyALDC8dXBD6Dk8cCuvsjHf1zN3woCAzYfQ"
ENV MYSQL_HOST="mysql"
ENV MYSQL_USER="root"
ENV MYSQL_PASSWORD="mamhidet_mysql"

# MySQLサーバーへの接続を待機するためのスクリプト
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# アプリケーションを実行
CMD ["/app/wait-for-it.sh", "mysql:3306", "--", "flet", "run", "main.py", "-p", "8000", "--web"]