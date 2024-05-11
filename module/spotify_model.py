from dataclasses import dataclass


class TrackItem:
    def __init__(self, data: dict) -> None:
        self.disc_number = data.get("disc_number")
        self.duration_ms = data.get("duration_ms")
        self.id = data.get("id")
        self.href = data.get("href")
        self.popularity = data.get("popularity")
        self.name = data.get("name")
        self.spotify_external_url = data.get(
            "external_urls", {}).get("spotify")
        pass


class Tracks:
    def __init__(self, data: dict) -> None:
        self.items: list[TrackItem] = []
        for item in data["items"]:
            self.items.append(
                TrackItem(item)
            )


class Search:
    def __init__(self, data: dict) -> None:
        self.tracks = Tracks(data["tracks"])
