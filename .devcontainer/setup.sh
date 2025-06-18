#!/bin/bash

set -e

echo "[INFO] Updating apt sources to use HTTPS..."
sudo find /etc/apt/ -name '*.list' -exec sed -i 's|http://|https://|g' {} +

echo "[INFO] Updating system and installing dependencies..."
sudo apt-get update && sudo apt-get install -y \
  curl gnupg ca-certificates \
  libcups2 libnss3 libnspr4 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 \
  libatspi2.0-0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
  libgbm1 libxkbcommon0 libasound2 libx11-xcb1 libxshmfence1 \
  libxss1 libxtst6 fonts-liberation unzip wget ntpdate \
  --no-install-recommends && sudo apt-get clean

echo "[INFO] Installing Python dependencies..."
pip install --user --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

echo "[INFO] Installing latest Google Chrome..."
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo gpg --dearmor -o /usr/share/keyrings/google-linux-signing-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-signing-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list > /dev/null
sudo apt-get update && sudo apt-get install -y google-chrome-stable && sudo rm -rf /var/lib/apt/lists/*
echo "[INFO] Installing dependencies..."
sudo apt-get update && sudo apt-get install -y curl gpg

echo "[INFO] Installing Ollama via shell script..."
curl -fsSL https://ollama.com/install.sh | sh

echo "[INFO] Starting Ollama in background to allow model pulling..."
ollama serve &
sleep 5

echo "[INFO] Pulling llama3 model..."
ollama pull llama3 || echo "[WARN] Pull failed, try manually later"

echo "[INFO] Installing Playwright browsers..."
python3 -m playwright install

echo "[INFO] Setup complete ✅"
