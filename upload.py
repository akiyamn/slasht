import sources
import requests
import pyperclip
import subprocess
import os

KEY_PATH = "key.txt"
POST_URL = "https://slimecorp.biz/t/upload.php"

def post():

    clip = sources.Clipboard()
    text = clip.get_text()
    key = get_key()
    req = requests.post(POST_URL, data={"data": text, "key": key})
    if req.status_code == 200:
        response = req.json()
        if response["error"] == "":
            pyperclip.copy(response["url"])
            notify("Text Upload Successful!", response["url"])
        else:
            show_error("Server error received: ", f"{response['error']} from {POST_URL}:")
    else:
        show_error("HTTP error received:", f"Error {req.status_code} {req.reason} from {POST_URL}")

def get_key():
    """
    Gets the key from the first line of `key.txt`
    If it doesn't exist, it will be created.
    :return: a string representation of the key
    """
    try:
        with open(KEY_PATH, "r") as key_file:
            return key_file.readline()
    except IOError:
        print("Key not found, creating new key.txt file...")
        with open(KEY_PATH, "w") as _:
            pass
        return ""

def notify(title, text):
    subprocess.Popen(["notify-send", "-i", "text-x-generic", title, text])

def show_error(title, details=""):
    notify(title, details)
    print(f"[ERROR] {title} - {details}")