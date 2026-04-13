"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "target_energy": 0.80,
        "target_tempo_bpm": 115,
        "target_valence": 0.85,
        "target_danceability": 0.75,
        "target_acousticness": 0.20,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 60)
    print("  MUSIC RECOMMENDATIONS")
    print(f"  Profile: genre={user_prefs['genre']} | mood={user_prefs['mood']}")
    print("=" * 60)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']}  —  {song['artist']}")
        print(f"    Score : {score:.2f} / 7.75")
        print(f"    Genre : {song['genre']}  |  Mood: {song['mood']}")
        print("    Why   :")
        for reason in explanation.split(" | "):
            print(f"            • {reason}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
