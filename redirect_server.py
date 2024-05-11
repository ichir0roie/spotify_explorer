import os
import json
from datetime import datetime, timedelta
from fastapi.responses import HTMLResponse
import requests
import uvicorn
from fastapi import FastAPI, Request
from module.constants import *
# from module.token import Token
# token = Token()

app = FastAPI()


@app.get("/")
def root():
    a = "a"
    b = "b" + a
    return {"hello world": b}


@app.get("/start_auth")
def start_auth():
    import subprocess
    import random
    import string

    rand_str = random.sample(string.ascii_letters, 16)

    scopes = [
        "playlist-read-private",
        "playlist-read-collaborative",
        "playlist-modify-private",
        "playlist-modify-public",
        "user-library-modify",
        "user-library-read",
        "user-read-email",
        "user-read-private",
    ]
    scope = " ".join(scopes)

    url = "https://accounts.spotify.com/authorize"

    res = requests.get(
        url=url,
        params={
            "response_type": "token",
            "client_id": CLIENT_ID,
            "scope": scope,
            "redirect_uri": "http://localhost:8888/callback",
            "state": rand_str,
        }
    )
    print(res.status_code)
    print(res.url)
    print(res.history)

    chrome = '"{chrome_path}" --profile-directory="Default" {url}'
    subprocess.run(
        chrome.format(
            chrome_path=CHROME_PATH,
            url=res.url
        ), shell=True
    )


@app.get("/callback", response_class=HTMLResponse)
def callback(
):
    with open("template/redirect_hash.html", "r", encoding="utf-8") as f:
        html = f.read()
    return html


@app.get("/callback_hash")
def callback_hash(
    request: Request
):
    print(request.query_params)
    now = datetime.now()
    now_str = now.strftime("%Y%m%d%H%M%S")
    out_path = f"out/access_token_history/{now_str}.json"
    latest_out = f"out/token.json"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(request.query_params._dict, f, indent=2)
    with open(latest_out, "w", encoding="utf-8") as f:
        json.dump(request.query_params._dict, f, indent=2)

    return request.query_params


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
