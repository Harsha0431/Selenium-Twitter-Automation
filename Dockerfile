FROM python:3.12-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable

# Install ChromeDriver
RUN wget -q -O /usr/bin/chromedriver https://chromedriver.storage.googleapis.com/$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip && \
    chmod +x /usr/bin/chromedriver

# Add Chrome and ChromeDriver to PATH
ENV PATH="/usr/bin/chromedriver:/usr/bin/google-chrome:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set Flask environment variable
ENV FLASK_ENV=production
ENV COMMAND_EXECUTOR=http://localhost:4444/wd/hub

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
