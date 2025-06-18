FROM mcr.microsoft.com/playwright/python:v1.52.0-jammy
WORKDIR /app
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./
# COPY init/entrypoint.sh /init/entrypoint.sh
# RUN chmod +x /init/entrypoint.sh

# ENTRYPOINT ["/bin/bash","/init/entrypoint.sh"]

# RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt &&     python -m playwright install chromium
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
# RUN find /etc/apt/sources.list.d /etc/apt -name '*.list' -exec sed -i 's|http://|https://|g' {} +
RUN find /etc/apt/ -name '*.list' -exec sed -i 's|http://|https://|g' {} + && apt-get update && apt-get install -y \
  curl gnupg ca-certificates \
  libcups2 libnss3 libnspr4 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 \
  libatspi2.0-0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libdbus-1-3\
  libgbm1 libxkbcommon0 libasound2 libx11-xcb1 libxshmfence1 libxss1 libxtst6 fonts-liberation unzip wget\
  ntpdate \
  --no-install-recommends && apt-get clean

# RUN ntpdate time.nist.gov

# RUN python -m playwright install
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /usr/share/keyrings/google-linux-signing-keyring.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-signing-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*
# Install Ollama CLI
# RUN curl -fsSL https://ollama.com/download/Ollama.zip -o ollama.zip && \
#     unzip ollama.zip && \
#     mv ollama /usr/local/bin/ollama && \
#     chmod +x /usr/local/bin/ollama && \
#     rm -rf ollama.zip

COPY . .

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0","--logger.level=debug"]

