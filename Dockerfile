# 使用官方 Python 基础镜像
FROM python:3.9-slim

# 安装必要的工具和依赖
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    libnss3 \
    libgconf-2-4 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    libatk1.0-0 \
    libcups2 \
    libxss1 \
    libxshmfence1 \
    libgbm-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装 Chrome 浏览器
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# 安装对应版本的 ChromeDriver
RUN CHROME_DRIVER_VERSION=$(apt list | grep google-chrome-stable | awk '{print $2}' | cut -d '-' -f 1) && \
    wget -q https://storage.googleapis.com/chrome-for-testing-public/${CHROME_DRIVER_VERSION}/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    cd chromedriver-linux64 && \
    mv chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    cd .. && \
    rm chromedriver-linux64.zip

# 设置工作目录
WORKDIR /v2ex-signin

# 复制项目文件
COPY . /v2ex-signin

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 设置环境变量
ENV PYTHONUNBUFFERED=1

# 启动程序
CMD ["python", "main.py"]
