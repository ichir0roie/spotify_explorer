import os
import pandas as pd
import time
from module import spotify_api
from module import spotify_model


def load_items() -> list[spotify_model.TrackItem]:
    df = pd.read_csv(
        "out/summary/search.csv"
    )
    items: list[spotify_model.TrackItem] = []
    for c, row in df.iterrows():
        items.append(
            spotify_model.TrackItem(
                row.to_dict()
            )
        )
    return items


def insert_all_tracks(
    target_playlist_id: str,
):

    items = load_items()
    for r in range(len(items))[::50]:
        print(r)
        spotify_api.playlists_tracks_post(
            target_playlist_id,
            items[r:r+50]
        )
        time.sleep(0.5)
