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


def add_play_list(
    playlist_id: str,
    item: spotify_model.TrackItem
):

    pass
