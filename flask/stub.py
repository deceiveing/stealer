import requests

# Server configuration (matches server.py)
SERVER_URL = "http://127.0.0.1:1111/upload"

# Dummy file to upload (safe)
FILE_CONTENT = b"This is a safe test file from the stub."
FILE_NAME = "test_file.txt"

def upload_file():
    files = {'file': (FILE_NAME, FILE_CONTENT)}
    try:
        response = requests.post(SERVER_URL, files=files)
        print("Server response:", response.text)
    except Exception as e:
        print("Error connecting to server:", e)

if __name__ == "__main__":
    upload_file()
