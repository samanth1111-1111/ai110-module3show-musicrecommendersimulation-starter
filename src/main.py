"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


# ── User Profiles ──────────────────────────────────────────────────────────────

PROFILES = [
    (
        "High-Energy Pop",
        {
            "genre": "pop",
            "mood": "happy",
            "target_energy": 0.90,
            "target_tempo_bpm": 128,
            "target_valence": 0.90,
            "target_danceability": 0.85,
            "target_acousticness": 0.10,
        },
    ),
    (
        "Chill Lofi",
        {
            "genre": "lofi",
            "mood": "chill",
            "target_energy": 0.25,
            "target_tempo_bpm": 75,
            "target_valence": 0.45,
            "target_danceability": 0.40,
            "target_acousticness": 0.75,
        },
    ),
    (
        "Deep Intense Rock",
        {
            "genre": "rock",
            "mood": "intense",
            "target_energy": 0.95,
            "target_tempo_bpm": 140,
            "target_valence": 0.30,
            "target_danceability": 0.55,
            "target_acousticness": 0.05,
        },
    ),
    # ── Adversarial / edge-case profiles ──────────────────────────────────────
    (
        "Edge Case: High Energy + Sad Mood (conflicting)",
        {
            "genre": "pop",
            "mood": "sad",
            "target_energy": 0.95,        # normally associated with upbeat songs
            "target_tempo_bpm": 130,
            "target_valence": 0.15,       # low valence (sad) vs. high energy — tension
            "target_danceability": 0.80,
            "target_acousticness": 0.10,
        },
    ),
    (
        "Edge Case: All Extremes (energy=1.0, acousticness=1.0)",
        {
            "genre": "jazz",
            "mood": "moody",
            "target_energy": 1.00,        # maximum energy
            "target_tempo_bpm": 200,      # far above any song in catalog
            "target_valence": 0.50,
            "target_danceability": 1.00,  # maximum danceability
            "target_acousticness": 1.00,  # maximum acousticness — conflicts with energy=1.0
        },
    ),
]


def print_recommendations(label: str, user_prefs: dict, recommendations: list) -> None:
    """Print a formatted recommendation block for one user profile."""
    print("\n" + "=" * 60)
    print(f"  PROFILE: {label}")
    print(f"  genre={user_prefs.get('genre')} | mood={user_prefs.get('mood')}")
    print("=" * 60)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']}  —  {song['artist']}")
        print(f"    Score : {score:.2f} / 8.25")
        print(f"    Genre : {song['genre']}  |  Mood: {song['mood']}")
        print("    Why   :")
        for reason in explanation.split(" | "):
            print(f"            • {reason}")
    print("\n" + "=" * 60)


def main() -> None:
    """Load songs and run the recommender for every defined user profile."""
    songs = load_songs("data/songs.csv")

    for label, user_prefs in PROFILES:
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(label, user_prefs, recommendations)


if __name__ == "__main__":
    main()
