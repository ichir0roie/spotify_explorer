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

    out_file = f"{__out_dir_base}/get/{function_url}"
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(f"{out_file}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    # print(data)
    return data


def __post_base(
    function_url: str,
    headers: dict = {},
    data: dict = {},
    params: dict = {}
):
    url = f"{__endpoint_base}/{function_url}"
    headers = {
        "Authorization": "Bearer {access_token}".format(access_token=my_token.access_token),
        "Content-Type": "application/json",
    }
    headers.update(
        headers
    )
    response = requests.post(
        url=url,
        headers=headers,
        data=data,
        params=params
    )
    res = response.json()

    out_file = f"{__out_dir_base}/post/{function_url}"
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(f"{out_file}.json", "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)
    # print(data)
    return res


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


def playlists_tracks_post(
    playlist_id: str,
    track_items: list[spotify_model.TrackItem]
):
    track_uris = []
    for track_item in track_items:
        url = f"spotify:track:{track_item.id}"
        track_uris.append(url)
    res = __post_base(
        f"playlists/{playlist_id}/tracks",
        # data={
        #     "uris": track_uris
        # }
        params={
            "uris": ",".join(track_uris)
        }
    )
    return res
