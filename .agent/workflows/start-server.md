---
description: how to start the optimized Sakhi backend and verify latency
---

### 1. Start the Unified Backend Server
Run this command from the `Sakhi_Webapp_Backend` directory. It starts the server on port 8000.

// turbo
```powershell
.\venv\Scripts\uvicorn.exe main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Run Streaming & Latency Test
Open a **new terminal** and run this command to verify that the TTFB is under 3 seconds and streaming is working.

// turbo
```powershell
.\venv\Scripts\python.exe test_streaming.py
```

### 3. Troubleshooting: Port 8000 already in use
If you see an error about the port being occupied, run this command to clear it:

```powershell
Stop-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess -Force
```
