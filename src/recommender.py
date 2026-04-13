from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of song dictionaries."""
    # TODO: Implement CSV loading logic
    import csv
    songs = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences and return a (score, reasons) tuple."""
    # TODO: Implement scoring logic using your Algorithm Recipe from Phase 2.
    # Expected return format: (score, reasons)
     
    score = 0.0
    reasons: List[str] = []

    # ── Categorical matches ───────────────────────────────────────────────────
    if song.get("genre") == user_prefs.get("genre"):
        score += 1.0
        reasons.append(f"genre match ({song['genre']}): +1.0")

    if song.get("mood") == user_prefs.get("mood"):
        score += 1.0
        reasons.append(f"mood match ({song['mood']}): +1.0")

    # ── Numeric similarity ────────────────────────────────────────────────────
    def _sim(song_val: float, target_val: Optional[float],
             weight: float, label: str, norm: float = 1.0) -> None:
        """Add similarity points; skip silently if target not in profile."""
        nonlocal score
        if target_val is None:
            return
        dist = min(abs(song_val - target_val) / norm, 1.0)
        pts = round(weight * (1.0 - dist), 2)
        score += pts
        reasons.append(
            f"{label} (song={song_val:.2f}, target={target_val:.2f}): +{pts:.2f}"
        )

    _sim(song["energy"],       user_prefs.get("target_energy"),       3.00, "energy")
    _sim(song["acousticness"], user_prefs.get("target_acousticness"), 1.00, "acousticness")
    _sim(song["tempo_bpm"],    user_prefs.get("target_tempo_bpm"),    1.00, "tempo",  norm=120.0)
    _sim(song["valence"],      user_prefs.get("target_valence"),      0.75, "valence")
    _sim(song["danceability"], user_prefs.get("target_danceability"), 0.50, "danceability")

    return round(score, 2), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return the top-k songs ranked by score against user preferences, with explanations."""
    # TODO: Implement scoring and ranking logic
    # Expected return format: (song_dict, score, explanation)
    
    scored = []
    for song in songs:
        s, reasons = score_song(user_prefs, song)
        scored.append((song, s, " | ".join(reasons)))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
