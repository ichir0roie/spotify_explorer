import json
from dataclasses import dataclass


class Token:
    access_token: str
    token_type: str
    expires_in: str

    def __init__(self):
        with open("out/token.json", "r", encoding="utf-8") as f:
            j = json.load(f)
            self.access_token = j["access_token"]
            self.token_type = j["token_type"]
            self.expires_in = j["expires_in"]
