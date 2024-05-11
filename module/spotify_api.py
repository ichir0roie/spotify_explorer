import json
import os
from datetime import datetime, timedelta
from module import constants, token, spotify_model
import requests

my_token = token.Token()

__endpoint_base = "https://api.spotify.com/v1"

__out_dir_base = "out/reponse"


def __get_base(
    function_url: str,
    method: str = "GET",
    headers: dict = {},
    params: dict = {}
):
    url = f"{__endpoint_base}/{function_url}"
    headers = {
        "Authorization": "Bearer {access_token}".format(access_token=my_token.access_token)
    }
    headers.update(
        headers
    )
    response = requests.get(
        url=url,
        headers=headers,
        params=params
    )
    data = response.json()

    out_file = f"{__out_dir_base}/{function_url}"
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(f"{out_file}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    # print(data)
    return data


def users_playlists(
    user_id: str
):
    return __get_base(
        f"users/{user_id}/playlists"
    )


def playlists_tracks(
    playlist_id: str
):
    return __get_base(
        f"playlists/{playlist_id}/tracks"
    )


def search(
    q_dict: dict = {},
    type: list[str] = ["track"],
    market: str = "JP",
    limit: int = 10,
    offset: int = 0
):
    q_list = []
    for k, v in q_dict.items():
        q_list.append(f"{k}%2520{v}")
    res = __get_base(
        f"search",
        params={
            "q": "%3".join(q_list),
            "type": type,
            "market": market,
            "limit": limit,
            "offset": offset
        }
    )
    return spotify_model.Search(res)
