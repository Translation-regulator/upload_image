FROM python:3.11-slim

# 安裝必要套件
RUN apt-get update && apt-get install -y gcc libmariadb-dev

# 建立工作目錄
WORKDIR /app

# 複製檔案
COPY . .

# 安裝依賴
RUN pip install --no-cache-dir -r requirements.txt

# 啟動 FastAPI 伺服器
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
