import os
import json
import time
import threading
import sys
import webbrowser
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
from collections import deque

def get_base_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent

BASE_DIR   = get_base_dir()
CONFIG_DIR = BASE_DIR / "config"
API_FILE   = CONFIG_DIR / "api_keys.json"

SYSTEM_NAME = "CAS-E"
MODEL_BADGE = "RAI RIT KOTTAYAM 26"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CAS-E — RAI RIT KOTTAYAM 26</title>
    <style>
        :root {
            --bg: #000000;
            --pri: #00d4ff;
            --mid: #007a99;
            --dim: #003344;
            --dimmer: #001520;
            --acc: #ff6600;
            --text: #8ffcff;
            --panel: #010c10;
        }

        @import url('https://fonts.googleapis.com/css2?family=Courier+Prime:ital,wght@0,400;0,700;1,400;1,700&display=swap');

        body, html {
            margin: 0;
            padding: 0;
            width: 100vw;
            height: 100vh;
            background-color: var(--bg);
            color: var(--text);
            font-family: 'Courier Prime', Courier, monospace;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        .grid-bg {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(var(--dimmer) 1px, transparent 1px),
                linear-gradient(90deg, var(--dimmer) 1px, transparent 1px);
            background-size: 40px 40px;
            z-index: 0;
            opacity: 0.5;
        }

        .header {
            height: 60px;
            background-color: #00080d;
            border-bottom: 1px solid var(--mid);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 40px;
            z-index: 10;
        }

        .header > div {
            flex: 1;
            display: flex;
        }

        .header .badge-container {
            justify-content: flex-start;
        }

        .header .clock-container {
            justify-content: flex-end;
        }

        .header .title-container {
            justify-content: center;
        }

        .header .title {
            color: var(--pri);
            font-size: 1.2rem;
            font-weight: bold;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }

        .header .title span {
            color: var(--mid);
            font-size: 0.6rem;
            margin-top: 4px;
        }

        .header .badge {
            color: var(--dim);
            font-size: 0.8rem;
            letter-spacing: 1px;
        }

        .header .clock {
            color: var(--pri);
            font-size: 1.1rem;
            font-weight: bold;
            letter-spacing: 1px;
        }

        .main-container {
            flex: 1;
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 10;
        }

        /* ORB ANIMATIONS */
        .orb-container {
            position: relative;
            width: 300px;
            height: 300px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-top: -50px;
        }

        .orb {
            position: absolute;
            border-radius: 50%;
            transition: all 0.3s ease;
        }

        .halo {
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, rgba(0, 212, 255, 0.4) 0%, rgba(0, 212, 255, 0) 70%);
            animation: pulse-halo 4s infinite alternate ease-in-out;
        }

        .glow-ring {
            width: 50%;
            height: 50%;
            border: 2px solid rgba(0, 212, 255, 0.5);
            box-shadow: 0 0 20px var(--pri), inset 0 0 20px var(--pri);
            animation: pulse-ring 2s infinite alternate ease-in-out;
        }

        .speaking .glow-ring {
            border-color: rgba(255, 102, 0, 0.8);
            box-shadow: 0 0 30px var(--acc), inset 0 0 30px var(--acc);
            transform: scale(1.1);
            animation: pulse-ring-speak 0.4s infinite alternate ease-in-out;
        }
        
        .speaking .halo {
            background: radial-gradient(circle, rgba(255, 102, 0, 0.5) 0%, rgba(255, 102, 0, 0) 70%);
            animation: pulse-halo-speak 0.8s infinite alternate ease-in-out;
        }

        .face-img {
            position: absolute;
            width: 140px;
            height: 140px;
            border-radius: 50%;
            object-fit: cover;
            z-index: 5;
            transition: transform 0.2s;
        }
        
        .speaking .face-img {
            transform: scale(1.08);
        }

        .core-text {
            position: absolute;
            color: var(--pri);
            font-weight: bold;
            font-size: 1.2rem;
            z-index: 6;
            text-shadow: 0 0 10px var(--pri);
            letter-spacing: 2px;
        }

        .speaking .core-text {
            color: var(--acc);
            text-shadow: 0 0 15px var(--acc);
        }

        .scan-arc {
            position: absolute;
            width: 90%;
            height: 90%;
            border-radius: 50%;
            border: 3px solid transparent;
            border-top-color: var(--pri);
            animation: spin 3s linear infinite;
        }
        
        .scan-arc-2 {
            position: absolute;
            width: 90%;
            height: 90%;
            border-radius: 50%;
            border: 2px solid transparent;
            border-bottom-color: rgba(255, 100, 0, 0.6);
            animation: spin-reverse 4s linear infinite;
        }

        .speaking .scan-arc {
            border-top-color: var(--acc);
            animation: spin 1s linear infinite;
        }

        @keyframes spin { 100% { transform: rotate(360deg); } }
        @keyframes spin-reverse { 100% { transform: rotate(-360deg); } }
        @keyframes pulse-ring { 0% { transform: scale(0.95); opacity: 0.8; } 100% { transform: scale(1.05); opacity: 1; } }
        @keyframes pulse-ring-speak { 0% { transform: scale(1.08); opacity: 0.9; } 100% { transform: scale(1.15); opacity: 1; } }
        @keyframes pulse-halo { 0% { opacity: 0.5; transform: scale(0.9); } 100% { opacity: 0.8; transform: scale(1.1); } }
        @keyframes pulse-halo-speak { 0% { opacity: 0.7; transform: scale(1.1); } 100% { opacity: 1; transform: scale(1.3); } }

        /* STATUS DISPLAY */
        .status-container {
            margin-top: 40px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .status-text {
            font-size: 1.1rem;
            font-weight: bold;
            color: var(--pri);
            letter-spacing: 2px;
            margin-bottom: 10px;
        }
        
        .speaking .status-text {
            color: var(--acc);
        }
        
        .status-text .dot {
            animation: blink 1s step-end infinite;
        }
        
        .emotion-text {
            font-size: 0.8rem;
            color: var(--mid);
            letter-spacing: 1px;
            margin-bottom: 20px;
            border: 1px solid var(--dim);
            padding: 2px 10px;
            border-radius: 4px;
            background: rgba(0, 0, 0, 0.5);
        }

        @keyframes blink { 50% { opacity: 0; } }

        .audio-bars {
            display: flex;
            align-items: flex-end;
            height: 20px;
            gap: 4px;
        }

        .bar {
            width: 6px;
            background-color: var(--dim);
            height: 4px;
            transition: height 0.1s;
        }

        /* LOG PANEL */
        .log-panel {
            width: 70%;
            height: 120px;
            background-color: var(--panel);
            border: 1px solid var(--mid);
            margin-bottom: 30px;
            padding: 10px 15px;
            overflow-y: auto;
            font-size: 0.9rem;
            line-height: 1.5;
            box-shadow: 0 0 15px rgba(0, 122, 153, 0.2);
            position: relative;
        }

        .log-panel::-webkit-scrollbar { width: 8px; }
        .log-panel::-webkit-scrollbar-track { background: var(--dimmer); }
        .log-panel::-webkit-scrollbar-thumb { background: var(--dim); border-radius: 4px; }

        .log-entry.sys { color: #ffcc00; }
        .log-entry.you { color: #e8e8e8; }
        .log-entry.ai { color: var(--pri); }

        .footer {
            height: 28px;
            background-color: #00080d;
            border-top: 1px solid var(--dim);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--dim);
            font-size: 0.7rem;
            z-index: 10;
        }

        /* SETUP MODAL */
        .modal-overlay {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.85);
            backdrop-filter: blur(4px);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 100;
        }

        .modal {
            background: #00080d;
            border: 1px solid var(--pri);
            padding: 30px 40px;
            width: 400px;
            box-shadow: 0 0 30px rgba(0, 212, 255, 0.2);
            text-align: center;
        }

        .modal h2 { color: var(--pri); font-size: 1.2rem; margin-top: 0; letter-spacing: 1px; }
        .modal p { color: var(--mid); font-size: 0.85rem; margin-bottom: 25px; }
        .modal input {
            width: 100%; padding: 10px; box-sizing: border-box;
            background: #000d12; border: 1px solid var(--dim); color: var(--text);
            font-family: 'Courier Prime', Courier, monospace; outline: none;
            margin-bottom: 25px; text-align: center;
        }
        .modal input:focus { border-color: var(--pri); box-shadow: 0 0 10px rgba(0, 212, 255, 0.3); }
        .modal button {
            background: var(--bg); border: 1px solid var(--pri); color: var(--pri);
            padding: 10px 20px; font-family: 'Courier Prime', Courier, monospace;
            cursor: pointer; transition: all 0.2s; font-weight: bold; width: 100%;
        }
        .modal button:hover { background: var(--dim); box-shadow: 0 0 15px rgba(0, 212, 255, 0.4); }

    </style>
</head>
<body id="app-body">
    <div class="grid-bg"></div>

    <div class="header">
        <div class="badge-container">
            <div class="badge">SYSTEM READY</div>
        </div>
        <div class="title-container">
            <div class="title">CAS-E<span>RAI RIT KOTTAYAM 26</span></div>
        </div>
        <div class="clock-container">
            <div class="clock" id="clock">00:00:00</div>
        </div>
    </div>

    <div class="main-container">
        <div class="orb-container">
            <div class="orb halo"></div>
            <div class="orb scan-arc"></div>
            <div class="orb scan-arc-2"></div>
            <div class="orb glow-ring"></div>
            <div class="core-text" id="core-text">CAS-E</div>
            <img src="/face.png" class="face-img" id="face-img" alt="face" onerror="this.style.display='none'; document.getElementById('core-text').style.display='block';" style="display:none;">
        </div>

        <div class="status-container">
            <div class="status-text" id="status-text"><span class="dot">●</span> INITIALISING</div>
            <div class="emotion-text" id="emotion-text">EMOTION: NEUTRAL</div>
            <div class="audio-bars" id="audio-bars">
                <!-- Bars generated by JS -->
            </div>
        </div>
    </div>

    <div class="log-panel" id="log-panel"></div>

    <div class="footer">RAI RIT KOTTAYAM 26</div>

    <div class="modal-overlay" id="setup-modal">
        <div class="modal">
            <h2>◈  INITIALISATION REQUIRED</h2>
            <p>Enter your Gemini API key to boot J.A.R.V.I.S.</p>
            <input type="password" id="api-key" placeholder="GEMINI API KEY">
            <button onclick="submitKey()">▸  INITIALISE SYSTEMS</button>
        </div>
    </div>

    <script>
        // Clock
        setInterval(() => {
            const now = new Date();
            document.getElementById('clock').textContent = now.toLocaleTimeString('en-US', {hour12: false});
        }, 1000);

        // Audio Bars
        const numBars = 32;
        const barsContainer = document.getElementById('audio-bars');
        const bars = [];
        for (let i = 0; i < numBars; i++) {
            const bar = document.createElement('div');
            bar.className = 'bar';
            barsContainer.appendChild(bar);
            bars.push(bar);
        }

        let isSpeaking = false;
        let isTyping = false;
        let logQueue = [];
        let statusText = "INITIALISING";

        function updateBars() {
            bars.forEach((bar, i) => {
                let h = 4;
                if (isSpeaking) {
                    h = Math.floor(Math.random() * 16) + 4;
                    bar.style.backgroundColor = h > 12 ? 'var(--pri)' : 'var(--mid)';
                } else {
                    h = Math.floor(3 + 2 * Math.sin(Date.now() / 200 + i * 0.5));
                    bar.style.backgroundColor = 'var(--dim)';
                }
                bar.style.height = `${h}px`;
            });
            requestAnimationFrame(updateBars);
        }
        updateBars();

        // Typewriter effect for logs
        const logPanel = document.getElementById('log-panel');
        
        function processNextLog() {
            if (isTyping || logQueue.length === 0) return;
            
            isTyping = true;
            const logDef = logQueue.shift();
            const text = logDef.text;
            const className = logDef.cls;
            
            const reqStatus = (className === 'you') ? "PROCESSING" : 
                              (className === 'ai') ? "RESPONDING" : 
                              isSpeaking ? "SPEAKING" : "ONLINE";
                              
            document.getElementById('status-text').innerHTML = `<span class="dot">${isSpeaking ? '●' : '○'}</span> ${reqStatus}`;

            const entry = document.createElement('div');
            entry.className = `log-entry ${className}`;
            logPanel.appendChild(entry);
            
            // Extract Emotion Tag if exists (e.g., [EMOTION: HAPPY])
            let cleanText = text;
            const emotionMatch = text.match(/\[EMOTION:\s*([A-Za-z0-9_-]+)\]/i);
            if (emotionMatch) {
                const emotionObj = document.getElementById('emotion-text');
                emotionObj.textContent = `EMOTION: ${emotionMatch[1].toUpperCase()}`;
                emotionObj.style.color = "var(--pri)";
                setTimeout(() => { emotionObj.style.color = "var(--mid)"; }, 2000);
                cleanText = text.replace(/\[EMOTION:\s*([A-Za-z0-9_-]+)\]/gi, '').trim();
            }

            let i = 0;
            function typeChar() {
                if (i < cleanText.length) {
                    entry.textContent += cleanText.charAt(i);
                    logPanel.scrollTop = logPanel.scrollHeight;
                    i++;
                    setTimeout(typeChar, 8);
                } else {
                    isTyping = false;
                    document.getElementById('status-text').innerHTML = `<span class="dot">${isSpeaking ? '●' : '○'}</span> ${isSpeaking ? "SPEAKING" : "ONLINE"}`;
                    setTimeout(processNextLog, 25);
                }
            }
            typeChar();
        }

        // Image loading logic
        const faceImg = document.getElementById('face-img');
        const coreText = document.getElementById('core-text');
        faceImg.onload = () => {
            faceImg.style.display = 'block';
            coreText.style.display = 'none';
        }

        // State polling
        async function pollState() {
            try {
                const res = await fetch('/state');
                const data = await res.json();
                
                if (data.needs_key) {
                    document.getElementById('setup-modal').style.display = 'flex';
                } else {
                    document.getElementById('setup-modal').style.display = 'none';
                }

                if (data.speaking !== isSpeaking) {
                    isSpeaking = data.speaking;
                    if (isSpeaking) {
                        document.getElementById('app-body').classList.add('speaking');
                        document.getElementById('status-text').innerHTML = `<span class="dot">●</span> SPEAKING`;
                    } else {
                        document.getElementById('app-body').classList.remove('speaking');
                        document.getElementById('status-text').innerHTML = `<span class="dot">○</span> ONLINE`;
                    }
                }

                if (data.logs && data.logs.length > 0) {
                    data.logs.forEach(log => {
                        let cls = 'sys';
                        const tl = log.toLowerCase();
                        if (tl.startsWith('you:')) cls = 'you';
                        else if (tl.startsWith('case:') || tl.startsWith('ai:')) cls = 'ai';
                        logQueue.push({ text: log, cls: cls });
                    });
                    processNextLog();
                }

            } catch (e) {
                console.error("Polling error:", e);
            }
            setTimeout(pollState, 200);
        }
        pollState();

        async function submitKey() {
            const key = document.getElementById('api-key').value.trim();
            if (!key) return;
            
            await fetch('/setup', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `key=${encodeURIComponent(key)}`
            });
            document.getElementById('api-key').value = '';
        }
    </script>
</body>
</html>"""

class CASEUIState:
    def __init__(self):
        self.speaking = False
        self.log_queue = []
        self.api_key_ready = API_FILE.exists()
        self.face_path = "face.png"
        
global_ui_state = CASEUIState()

class CASEUIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode('utf-8'))
        elif self.path == '/state':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            logs = global_ui_state.log_queue[:]
            global_ui_state.log_queue.clear()
            
            state = {
                "speaking": global_ui_state.speaking,
                "needs_key": not global_ui_state.api_key_ready,
                "logs": logs
            }
            self.wfile.write(json.dumps(state).encode('utf-8'))
        elif self.path == '/face.png':
            try:
                face_full_path = str(get_base_dir() / global_ui_state.face_path)
                with open(face_full_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'image/png')
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_error(404, 'File Not Found')
        else:
            self.send_error(404, 'File Not Found')

    def do_POST(self):
        if self.path == '/setup':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            parsed = urllib.parse.parse_qs(post_data)
            
            if 'key' in parsed:
                key = parsed['key'][0].strip()
                if key:
                    os.makedirs(CONFIG_DIR, exist_ok=True)
                    with open(API_FILE, "w", encoding="utf-8") as f:
                        json.dump({"gemini_api_key": key}, f, indent=4)
                    global_ui_state.api_key_ready = True
                    global_ui_state.log_queue.append("SYS: Systems initialised. CASE online.")
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode('utf-8'))
        else:
            self.send_error(404, 'File Not Found')

    def log_message(self, format, *args):
        # Disable default logging to keep terminal clean
        pass

class DummyRoot:
    def __init__(self):
        self._quit = False

    def mainloop(self):
        # Keep the main thread alive, acting like tkinter's mainloop
        try:
            while not self._quit:
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass
        finally:
            os._exit(0)

class CASEUI:
    def __init__(self, face_path, size=None):
        global_ui_state.face_path = face_path
        self.root = DummyRoot()
        
        # Start server in a background thread
        self.port = 8080
        # Find an open port
        import socket
        while True:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', self.port))
            if result != 0:
                sock.close()
                break
            sock.close()
            self.port += 1
            
        self.server = HTTPServer(('127.0.0.1', self.port), CASEUIHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()
        
        # Open the browser
        url = f"http://127.0.0.1:{self.port}/"
        webbrowser.open(url)
        
        if not global_ui_state.api_key_ready:
            print(f"[UI] Please configure API key in the browser: {url}")
            
    def write_log(self, text: str):
        global_ui_state.log_queue.append(text)

    def start_speaking(self):
        global_ui_state.speaking = True

    def stop_speaking(self):
        global_ui_state.speaking = False

    def wait_for_api_key(self):
        """Block until API key is saved (called from main thread before starting CASE)."""
        while not global_ui_state.api_key_ready:
            time.sleep(0.1)