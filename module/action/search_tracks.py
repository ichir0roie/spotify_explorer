import os
import pandas as pd
import time
from module import spotify_api
from module import spotify_model


def search_major_track(
    track_name: str
):
    res = spotify_api.search(
        q_dict={
            "track": track_name
        }
    )
    items = res.tracks.items[:3]
    items: list[spotify_model.TrackItem] = sorted(
        items,
        key=lambda i: i.popularity,
        reverse=True
    )

    for item in items[:3]:
        print(
            f"{item.id}\t{item.popularity}\t{item.spotify_external_url}"
        )
    return items


def _search_tracks(
    track_name_list=[]
) -> list[spotify_model.TrackItem]:
    all_items = []
    for c, track_name in enumerate(track_name_list):
        print(f"{c}/{len(track_name_list)}\t{track_name}")
        time.sleep(0.2)
        items = search_major_track(track_name)
        all_items.extend(items)

    return all_items


def _save_track_items(
    items: list[spotify_model.TrackItem]
):
    dict_list = []
    for item in items:
        dict_list.append(
            item.__dict__
        )
    df = pd.DataFrame.from_dict(dict_list)
    os.makedirs("out/summary", exist_ok=True)
    df.to_csv("out/summary/search.csv", index=False)


def dump_search(
    track_name_list: list = []
):
    items = _search_tracks(track_name_list)
    _save_track_items(items)
    return items
