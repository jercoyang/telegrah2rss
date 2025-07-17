FROM python:3.9-slim

WORKDIR /app

# 安装必要的系统依赖
RUN apt-get update && apt-get install -y gcc libxml2-dev libxslt-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p processed && \
    mkdir -p templates && \
    python -c "from db import init_db; init_db()"

CMD ["python", "app.py"]