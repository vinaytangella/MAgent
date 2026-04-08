#!/bin/bash
set -e

echo "🚀 Installing  MAgent metric collector..."

# Resolve the real user (important for LaunchAgents)
if [ -n "$SUDO_USER" ]; then
  USER_HOME=$(eval echo ~${SUDO_USER})
else
  USER_HOME="$HOME"
fi

AGENT_DIR="/usr/local/magent_metrics"
LAUNCH_AGENTS_DIR="$USER_HOME/Library/LaunchAgents"

METRICS_URL="https://raw.githubusercontent.com/vinaytangella/MAgent/refs/heads/main/CollectMetrics.py"
PLIST_URL="https://raw.githubusercontent.com/vinaytangella/MAgent/refs/heads/main/com.metrics.magent.plist"

PLIST_NAME="com.metrics.magent.plist"

echo "📁 Creating agent directory..."
sudo mkdir -p "$AGENT_DIR"

echo "⬇️ Downloading metrics agent..."
sudo curl -fsSL "$METRICS_URL" -o "$AGENT_DIR/metrics.py"
sudo chmod +x "$AGENT_DIR/metrics.py"

echo "📁 Ensuring LaunchAgents directory exists..."
mkdir -p "$LAUNCH_AGENTS_DIR"

echo "⬇️ Downloading plist..."
curl -fsSL "$PLIST_URL" -o "$LAUNCH_AGENTS_DIR/$PLIST_NAME"
chmod 644 "$LAUNCH_AGENTS_DIR/$PLIST_NAME"

echo "📦 Installing Python dependency (psutil)..."
python3 -m pip install --user psutil >/dev/null

echo "🔁 Reloading launch agent..."
launchctl unload "$LAUNCH_AGENTS_DIR/$PLIST_NAME" 2>/dev/null || true
launchctl load "$LAUNCH_AGENTS_DIR/$PLIST_NAME"

echo "✅ Installation complete!"
echo "📊 Metrics agent is now running in the background."
