# Raspberry Pi 4 (4GB) Implementation Guide for CAS-E

This guide provide a zero-error, step-by-step setup for CAS-E as a humanoid robot chest display.

## 1. Hardware Requirements
- **Raspberry Pi 4 (4GB RAM)**
- **microSD Card** (16GB+ Class 10 recommended)
- **USB Microphone** (Standard plug-and-play USB mic)
- **Speaker / Audio Output** (3.5mm jack or USB speakers)
- **5V 3A Power Supply** (Official USB-C recommended)
- **Display** (7-inch LCD or any HDMI/DSI display for the chest)

## 2. Operating System Setup
1. Download **Raspberry Pi Imager** on your PC.
2. Select **Raspberry Pi OS (64-bit)** with Desktop Environment.
3. Click the gear icon to pre-configure **WiFi**, **SSH**, and User credentials.
4. Flash the microSD card, insert it into the Pi, and boot it up.

## 3. System Dependencies
Open the terminal on your Raspberry Pi and execute the following commands precisely:

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install audio and build dependencies
sudo apt install -y python3-pip python3-venv libasound2-dev portaudio19-dev python3-pyaudio
```

## 4. Software Environment Setup
Navigate to your desired project directory:

```bash
# Create project folder
mkdir ~/cas-e && cd ~/cas-e

# Set up Python Virtual Environment
python3 -m venv venv
source venv/bin/activate

# Install required Python libraries
pip install pyaudio google-genai google-generativeai pillow requests beautifulsoup4
```

## 5. Deployment & Configuration
1. **Transfer Files**: Copy the entire project directory ([main.py](file:///c:/Users/Geoel/OneDrive/Desktop/Gemini_html/main.py), [ui.py](file:///c:/Users/Geoel/OneDrive/Desktop/Gemini_html/ui.py), `actions/`, `config/`, etc.) into `~/cas-e`.
2. **API Keys**: On first run, the UI will prompt for your **Gemini API Key**.
3. **Execution**:
   ```bash
   source venv/bin/activate
   python main.py
   ```

## 6. Robotic Chest Display Optimization
- **Auto-Fullscreen**: When the browser window opens for the UI, press **F11** once to enter kiosk/fullscreen mode. 
- **Symmetry**: The UI has been balanced to be perfectly centered for a humanoid robot's chest.
- **Heartbeat Core**: The central orb pulses with heartbeat-like animations, responding to "Speaking" states.
- **Emotion Display**: CAS-E automatically parses hidden tags (e.g., `[EMOTION: HAPPY]`) to update the "Emotion Status" indicator on the display.

## 7. Campus Assistant Features
- Ask CAS-E about **RIT Kottayam** courses, history, or facilities.
- Request the latest **circulars** or notices specifically for RIT.
- The AI is programmed to treat RIT as its primary campus environment.
