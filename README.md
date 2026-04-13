# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

Each `Song` stores ten fields — `id`, `title`, `artist`, and seven scoring features: `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`.

The `UserProfile` stores `favorite_genre`, `favorite_mood`, `target_energy`, and `likes_acoustic`. The functional scorer (`score_song`) extends this with optional numeric targets for `target_tempo_bpm`, `target_valence`, `target_danceability`, and `target_acousticness`.

**Scoring — Algorithm Recipe:**

Each song is scored out of a maximum of **7.75 points** using a point-weighted formula:

| Signal | Type | Points |
|---|---|---|
| Genre matches user preference | Categorical (exact) | +2.00 |
| Mood matches user preference | Categorical (exact) | +1.00 |
| Energy closeness | Numeric similarity | up to +1.50 |
| Acousticness closeness | Numeric similarity | up to +1.00 |
| Tempo closeness (normalized over 120 bpm) | Numeric similarity | up to +1.00 |
| Valence closeness | Numeric similarity | up to +0.75 |
| Danceability closeness | Numeric similarity | up to +0.50 |

Numeric similarity is calculated as: `points = weight × (1 − clamped_distance)`, so a perfect match earns the full weight and a maximum-distance mismatch earns 0. Categorical fields are all-or-nothing — no partial credit.

All songs are scored, collected into a list, sorted by score descending, and the top-k are returned.

**Sample terminal output** (pop/happy profile, top 5):

```
============================================================
  MUSIC RECOMMENDATIONS
  Profile: genre=pop | mood=happy
============================================================

#1  Sunrise City  —  Neon Echo
    Score : 7.64 / 7.75
    Genre : pop  |  Mood: happy
    Why   :
            • genre match (pop): +2.0
            • mood match (happy): +1.0
            • energy (song=0.82, target=0.80): +1.47
            • acousticness (song=0.18, target=0.20): +0.98
            • tempo (song=118.00, target=115.00): +0.97
            • valence (song=0.84, target=0.85): +0.74
            • danceability (song=0.79, target=0.75): +0.48

#2  Gym Hero  —  Max Pulse
    Score : 6.13 / 7.75
    Genre : pop  |  Mood: intense
    Why   :
            • genre match (pop): +2.0
            • energy (song=0.93, target=0.80): +1.30
            • acousticness (song=0.05, target=0.20): +0.85
            • tempo (song=132.00, target=115.00): +0.86
            • valence (song=0.77, target=0.85): +0.69
            • danceability (song=0.88, target=0.75): +0.43

#3  Rooftop Lights  —  Indigo Parade
    Score : 5.41 / 7.75
    Genre : indie pop  |  Mood: happy
    Why   :
            • mood match (happy): +1.0
            • energy (song=0.76, target=0.80): +1.44
            • acousticness (song=0.35, target=0.20): +0.85
            • tempo (song=124.00, target=115.00): +0.93
            • valence (song=0.81, target=0.85): +0.72
            • danceability (song=0.82, target=0.75): +0.47

#4  Night Drive Loop  —  Neon Echo
    Score : 4.33 / 7.75
    Genre : synthwave  |  Mood: moody
    Why   :
            • energy (song=0.75, target=0.80): +1.42
            • acousticness (song=0.22, target=0.20): +0.98
            • tempo (song=110.00, target=115.00): +0.96
            • valence (song=0.49, target=0.85): +0.48
            • danceability (song=0.73, target=0.75): +0.49

#5  Rise Up Together  —  Marla Sinclair
    Score : 4.23 / 7.75
    Genre : soul  |  Mood: uplifting
    Why   :
            • energy (song=0.68, target=0.80): +1.32
            • acousticness (song=0.41, target=0.20): +0.79
            • tempo (song=102.00, target=115.00): +0.89
            • valence (song=0.86, target=0.85): +0.74
            • danceability (song=0.77, target=0.75): +0.49

============================================================
```
<img width="601" height="237" alt="image" src="https://github.com/user-attachments/assets/27be1b1d-2e19-4dbc-a968-cf656a19c729" />


Genre carries the single largest weight in the system (+2.0), which is double the mood weight (+1.0). This creates a structural bias: a song that perfectly matches the user's mood and all numeric features but belongs to the wrong genre can score at most **5.75 / 7.75 (74%)**, while a genre-matching song with the wrong mood and identical numeric features scores **6.75 / 7.75 (87%)**. The genre-match song wins every time, even if the mood-match song would feel like a better fit to the listener.

In practice this means a user who wants "intense" songs could receive rock tracks they dislike simply because their profile says `genre=rock`, while a perfect-mood EDM track gets buried. Systems that over-weight a single categorical label risk creating a filter bubble around that label — the recommender stops surfacing diversity and starts reinforcing one identity (genre) regardless of how well everything else fits.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Three standard profiles and two adversarial edge-case profiles were defined in `src/main.py` and run against the full catalog. Terminal output for each is captured below.

---

### Profile 1 — High-Energy Pop (`genre=pop | mood=happy`)

```
============================================================
  PROFILE: High-Energy Pop
  genre=pop | mood=happy
============================================================

#1  Sunrise City  —  Neon Echo
    Score : 7.39 / 7.75
    Genre : pop  |  Mood: happy
    Why   :
            • genre match (pop): +2.0
            • mood match (happy): +1.0
            • energy (song=0.82, target=0.90): +1.38
            • acousticness (song=0.18, target=0.10): +0.92
            • tempo (song=118.00, target=128.00): +0.92
            • valence (song=0.84, target=0.90): +0.70
            • danceability (song=0.79, target=0.85): +0.47

#2  Gym Hero  —  Max Pulse
    Score : 6.51 / 7.75
    Genre : pop  |  Mood: intense
    Why   :
            • genre match (pop): +2.0
            • energy (song=0.93, target=0.90): +1.46
            • acousticness (song=0.05, target=0.10): +0.95
            • tempo (song=132.00, target=128.00): +0.97
            • valence (song=0.77, target=0.90): +0.65
            • danceability (song=0.88, target=0.85): +0.48

#3  Rooftop Lights  —  Indigo Parade
    Score : 5.17 / 7.75
    Genre : indie pop  |  Mood: happy
    Why   :
            • mood match (happy): +1.0
            • energy (song=0.76, target=0.90): +1.29
            • acousticness (song=0.35, target=0.10): +0.75
            • tempo (song=124.00, target=128.00): +0.97
            • valence (song=0.81, target=0.90): +0.68
            • danceability (song=0.82, target=0.85): +0.48

#4  Overdrive  —  Pulse Grid
    Score : 4.44 / 7.75
    Genre : edm  |  Mood: euphoric
    Why   :
            • energy (song=0.96, target=0.90): +1.41
            • acousticness (song=0.03, target=0.10): +0.93
            • tempo (song=138.00, target=128.00): +0.92
            • valence (song=0.88, target=0.90): +0.73
            • danceability (song=0.95, target=0.85): +0.45

#5  Street Chronicles  —  Verse Architect
    Score : 4.25 / 7.75
    Genre : hip-hop  |  Mood: energetic
    Why   :
            • energy (song=0.87, target=0.90): +1.46
            • acousticness (song=0.08, target=0.10): +0.98
            • tempo (song=96.00, target=128.00): +0.73
            • valence (song=0.72, target=0.90): +0.61
            • danceability (song=0.91, target=0.85): +0.47

============================================================
```

**Observation:** Genre lock-in is strong — the top 2 slots are both `pop` regardless of numeric fit. #3 wins mood-match but loses the genre bonus.

---

### Profile 2 — Chill Lofi (`genre=lofi | mood=chill`)

```
============================================================
  PROFILE: Chill Lofi
  genre=lofi | mood=chill
============================================================

#1  Library Rain  —  Paper Lanterns
    Score : 7.26 / 7.75
    Genre : lofi  |  Mood: chill
    Why   :
            • genre match (lofi): +2.0
            • mood match (chill): +1.0
            • energy (song=0.35, target=0.25): +1.35
            • acousticness (song=0.86, target=0.75): +0.89
            • tempo (song=72.00, target=75.00): +0.97
            • valence (song=0.60, target=0.45): +0.64
            • danceability (song=0.58, target=0.40): +0.41

#2  Midnight Coding  —  LoRoom
    Score : 7.24 / 7.75
    Genre : lofi  |  Mood: chill
    Why   :
            • genre match (lofi): +2.0
            • mood match (chill): +1.0
            • energy (song=0.42, target=0.25): +1.25
            • acousticness (song=0.71, target=0.75): +0.96
            • tempo (song=78.00, target=75.00): +0.97
            • valence (song=0.56, target=0.45): +0.67
            • danceability (song=0.62, target=0.40): +0.39

#3  Focus Flow  —  LoRoom
    Score : 6.25 / 7.75
    Genre : lofi  |  Mood: focused
    Why   :
            • genre match (lofi): +2.0
            • energy (song=0.40, target=0.25): +1.27
            • acousticness (song=0.78, target=0.75): +0.97
            • tempo (song=80.00, target=75.00): +0.96
            • valence (song=0.59, target=0.45): +0.65
            • danceability (song=0.60, target=0.40): +0.40

#4  Spacewalk Thoughts  —  Orbit Bloom
    Score : 5.26 / 7.75
    Genre : ambient  |  Mood: chill
    Why   :
            • mood match (chill): +1.0
            • energy (song=0.28, target=0.25): +1.46
            • acousticness (song=0.92, target=0.75): +0.83
            • tempo (song=60.00, target=75.00): +0.88
            • valence (song=0.65, target=0.45): +0.60
            • danceability (song=0.41, target=0.40): +0.49

#5  Crossroads at Midnight  —  Eli Gravel
    Score : 4.30 / 7.75
    Genre : blues  |  Mood: brooding
    Why   :
            • energy (song=0.38, target=0.25): +1.30
            • acousticness (song=0.88, target=0.75): +0.87
            • tempo (song=72.00, target=75.00): +0.97
            • valence (song=0.36, target=0.45): +0.68
            • danceability (song=0.44, target=0.40): +0.48

============================================================
```

**Observation:** The system surfaces all three lofi songs, then falls back to acoustically similar genres (ambient, blues). Results feel correct for this profile.

---

### Profile 3 — Deep Intense Rock (`genre=rock | mood=intense`)

```
============================================================
  PROFILE: Deep Intense Rock
  genre=rock | mood=intense
============================================================

#1  Storm Runner  —  Voltline
    Score : 7.35 / 7.75
    Genre : rock  |  Mood: intense
    Why   :
            • genre match (rock): +2.0
            • mood match (intense): +1.0
            • energy (song=0.91, target=0.95): +1.44
            • acousticness (song=0.10, target=0.05): +0.95
            • tempo (song=152.00, target=140.00): +0.90
            • valence (song=0.48, target=0.30): +0.61
            • danceability (song=0.66, target=0.55): +0.45

#2  Gym Hero  —  Max Pulse
    Score : 5.14 / 7.75
    Genre : pop  |  Mood: intense
    Why   :
            • mood match (intense): +1.0
            • energy (song=0.93, target=0.95): +1.47
            • acousticness (song=0.05, target=0.05): +1.00
            • tempo (song=132.00, target=140.00): +0.93
            • valence (song=0.77, target=0.30): +0.40
            • danceability (song=0.88, target=0.55): +0.34

#3  Iron Requiem  —  Shatter Hex
    Score : 4.42 / 7.75
    Genre : metal  |  Mood: angry
    Why   :
            • energy (song=0.95, target=0.95): +1.50
            • acousticness (song=0.06, target=0.05): +0.99
            • tempo (song=175.00, target=140.00): +0.71
            • valence (song=0.33, target=0.30): +0.73
            • danceability (song=0.58, target=0.55): +0.49

#4  Overdrive  —  Pulse Grid
    Score : 4.05 / 7.75
    Genre : edm  |  Mood: euphoric
    Why   :
            • energy (song=0.96, target=0.95): +1.48
            • acousticness (song=0.03, target=0.05): +0.98
            • tempo (song=138.00, target=140.00): +0.98
            • valence (song=0.88, target=0.30): +0.31
            • danceability (song=0.95, target=0.55): +0.30

#5  Night Drive Loop  —  Neon Echo
    Score : 3.80 / 7.75
    Genre : synthwave  |  Mood: moody
    Why   :
            • energy (song=0.75, target=0.95): +1.20
            • acousticness (song=0.22, target=0.05): +0.83
            • tempo (song=110.00, target=140.00): +0.75
            • valence (song=0.49, target=0.30): +0.61
            • danceability (song=0.73, target=0.55): +0.41

============================================================
```

**Observation:** Only one `rock` song exists in the catalog so results 2–5 are from unrelated genres. The catalog is too narrow for a rock user.

---

### Edge Case 1 — High Energy + Sad Mood (conflicting preferences)

```
============================================================
  PROFILE: Edge Case: High Energy + Sad Mood (conflicting)
  genre=pop | mood=sad
============================================================

#1  Gym Hero  —  Max Pulse
    Score : 6.15 / 7.75
    Genre : pop  |  Mood: intense
    Why   :
            • genre match (pop): +2.0
            • energy (song=0.93, target=0.95): +1.47
            • acousticness (song=0.05, target=0.10): +0.95
            • tempo (song=132.00, target=130.00): +0.98
            • valence (song=0.77, target=0.15): +0.29
            • danceability (song=0.88, target=0.80): +0.46

#2  Sunrise City  —  Neon Echo
    Score : 5.84 / 7.75
    Genre : pop  |  Mood: happy
    Why   :
            • genre match (pop): +2.0
            • energy (song=0.82, target=0.95): +1.30
            • acousticness (song=0.18, target=0.10): +0.92
            • tempo (song=118.00, target=130.00): +0.90
            • valence (song=0.84, target=0.15): +0.23
            • danceability (song=0.79, target=0.80): +0.49

#3  Storm Runner  —  Voltline
    Score : 4.19 / 7.75
    Genre : rock  |  Mood: intense
    Why   :
            • energy (song=0.91, target=0.95): +1.44
            • acousticness (song=0.10, target=0.10): +1.00
            • tempo (song=152.00, target=130.00): +0.82
            • valence (song=0.48, target=0.15): +0.50
            • danceability (song=0.66, target=0.80): +0.43

#4  Iron Requiem  —  Shatter Hex
    Score : 4.08 / 7.75
    Genre : metal  |  Mood: angry
    Why   :
            • energy (song=0.95, target=0.95): +1.50
            • acousticness (song=0.06, target=0.10): +0.96
            • tempo (song=175.00, target=130.00): +0.62
            • valence (song=0.33, target=0.15): +0.61
            • danceability (song=0.58, target=0.80): +0.39

#5  Overdrive  —  Pulse Grid
    Score : 3.97 / 7.75
    Genre : edm  |  Mood: euphoric
    Why   :
            • energy (song=0.96, target=0.95): +1.48
            • acousticness (song=0.03, target=0.10): +0.93
            • tempo (song=138.00, target=130.00): +0.93
            • valence (song=0.88, target=0.15): +0.20
            • danceability (song=0.95, target=0.80): +0.43

============================================================
```

**Observation (adversarial):** The mood signal `sad` is completely ignored — no `sad` song exists, and the genre bonus of +2.0 dominates so strongly that upbeat pop songs (#1 Gym Hero, #2 Sunrise City) float to the top even though their valence contradicts the user's preference. This reveals the genre-lock bias described in the scoring section.

---

### Edge Case 2 — All Extremes (energy=1.0 AND acousticness=1.0, tempo=200)

```
============================================================
  PROFILE: Edge Case: All Extremes (energy=1.0, acousticness=1.0)
  genre=jazz | mood=moody
============================================================

#1  Coffee Shop Stories  —  Slow Stereo
    Score : 4.38 / 7.75
    Genre : jazz  |  Mood: relaxed
    Why   :
            • genre match (jazz): +2.0
            • energy (song=0.37, target=1.00): +0.55
            • acousticness (song=0.89, target=1.00): +0.89
            • tempo (song=90.00, target=200.00): +0.08
            • valence (song=0.71, target=0.50): +0.59
            • danceability (song=0.54, target=1.00): +0.27

#2  Night Drive Loop  —  Neon Echo
    Score : 3.69 / 7.75
    Genre : synthwave  |  Mood: moody
    Why   :
            • mood match (moody): +1.0
            • energy (song=0.75, target=1.00): +1.12
            • acousticness (song=0.22, target=1.00): +0.22
            • tempo (song=110.00, target=200.00): +0.25
            • valence (song=0.49, target=0.50): +0.74
            • danceability (song=0.73, target=1.00): +0.36

#3  Iron Requiem  —  Shatter Hex
    Score : 3.18 / 7.75
    Genre : metal  |  Mood: angry
    Why   :
            • energy (song=0.95, target=1.00): +1.42
            • acousticness (song=0.06, target=1.00): +0.06
            • tempo (song=175.00, target=200.00): +0.79
            • valence (song=0.33, target=0.50): +0.62
            • danceability (song=0.58, target=1.00): +0.29

#4  Storm Runner  —  Voltline
    Score : 3.12 / 7.75
    Genre : rock  |  Mood: intense
    Why   :
            • energy (song=0.91, target=1.00): +1.36
            • acousticness (song=0.10, target=1.00): +0.10
            • tempo (song=152.00, target=200.00): +0.60
            • valence (song=0.48, target=0.50): +0.73
            • danceability (song=0.66, target=1.00): +0.33

#5  Overdrive  —  Pulse Grid
    Score : 2.88 / 7.75
    Genre : edm  |  Mood: euphoric
    Why   :
            • energy (song=0.96, target=1.00): +1.44
            • acousticness (song=0.03, target=1.00): +0.03
            • tempo (song=138.00, target=200.00): +0.48
            • valence (song=0.88, target=0.50): +0.46
            • danceability (song=0.95, target=1.00): +0.47

============================================================
```

**Observation (adversarial):** Requesting both `energy=1.0` and `acousticness=1.0` is physically contradictory — no real song can max both. The scores collapse (top result is only 4.38 / 7.75) and the genre match for `jazz` (#1) wins even though the jazz song scores poorly on energy and tempo. The `tempo=200` target is outside the entire catalog's range, earning near-zero tempo points everywhere. This shows the system handles impossible preferences gracefully but returns low-confidence results.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

Recommenders do not understand music — they translate it into numbers and find the numbers that are closest together. This project made that substitution visible. The system has no idea what "chill lofi" sounds like, but it knows that low energy + slow tempo + high acousticness tends to match the label, and that proxy works well enough that the top results feel right. The failure cases are equally instructive: when a user asks for `mood=sad` and no sad song exists in the catalog, the system does not say "I don't know" — it quietly ignores the mood signal and returns the best energy match, which happens to be an upbeat gym track. That silent fallback is exactly how real-world bias creeps into production systems. The algorithm keeps running, keeps producing confident-looking output, and the user has no way to know that one of their preferences was simply discarded.

The clearest bias discovered here is that a single categorical label — genre — can act as a gatekeeper that prevents any amount of numerical similarity from overcoming it. A near-perfect audio match in the wrong genre scores lower than a mediocre match in the right genre. In a 20-song catalog where most genres have exactly one representative, this means the recommender is not surfacing the best song for the listener; it is surfacing the only song that wears the right label. Scaling this up to a real app with millions of songs would not automatically fix the problem — if the catalog is imbalanced (more pop than blues, more English than Spanish), the genre bonus rewards whichever identity the system has the most data for, and underrepresented genres lose before the audio features are even compared.

---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

Every song is scored on seven things: its genre label, its mood label, and five audio numbers — energy (how loud/intense), tempo (speed in BPM), acousticness (how instrument-driven vs. electronic), valence (how positive/upbeat), and danceability. The user tells the system their preferred genre, preferred mood, and target values for those same audio numbers. The system then checks each song: genre match earns 1 point, mood match earns 1 point, and each audio number earns up to a few points depending on how close the song's value is to the user's target. A perfect match gets full points; the further away, the fewer points. All points are added up and the top five songs win.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

There are **20 songs** in `data/songs.csv`. No songs were added or removed from the original starter dataset. Genres represented include pop, lofi, rock, jazz, ambient, synthwave, indie pop, hip-hop, classical, R&B, country, EDM, folk, metal, soul, reggae, and blues. Moods include happy, chill, intense, focused, relaxed, moody, energetic, melancholic, romantic, euphoric, sad, angry, and uplifting. Most genres have only one song each. The catalog skews toward Western, English-language music and does not include Latin, K-pop, afrobeats, or world music, so it mostly reflects a mainstream Western listener's taste.

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

The system worked best for the **Chill Lofi** profile — Library Rain and Midnight Coding came back as #1 and #2, which are exactly the kind of slow, acoustic, quiet tracks that fit that mood. The **High-Energy Pop** profile also felt right: Sunrise City was a natural #1. The biggest strength is transparency — every recommendation shows a breakdown of exactly which factors contributed and by how many points, so you can always see *why* a song ranked where it did. Most real recommenders cannot do that.

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

Yes — if a mood the user wants (e.g., "sad") does not exist in the catalog, the system silently ignores it and picks the closest audio match instead, which can surface completely wrong-feeling songs. It treats every user the same way: one genre, one mood, fixed weights. It does not adapt to different taste shapes. Because most genres have only one song, the genre bonus acts like a guaranteed win — the lone genre representative always floats to the top regardless of how poorly it fits everything else. In a real product this would be unfair to listeners of niche or underrepresented genres, who would receive low-quality matches while mainstream pop or lofi listeners get better results just because the catalog has more songs for them.

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

Five profiles were tested: three standard (High-Energy Pop, Chill Lofi, Deep Intense Rock) and two adversarial edge cases (High-Energy + Sad Mood, and All-Extremes with physically impossible targets like energy=1.0 and acousticness=1.0 at the same time). For each profile, the output was compared against intuition — did the top result feel musically right? Standard profiles passed; edge cases revealed that the system returns confident-looking but musically wrong answers when the targets are contradictory or when a requested mood does not exist in the catalog. No single numeric metric was used; evaluation was qualitative, comparing output against expected songs.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

1. **Soft genre matching** — instead of all-or-nothing, give partial credit for related genres (e.g., blues ↔ soul = 0.7, pop ↔ indie pop = 0.8). This would break the single-song filter bubble for niche genres.
2. **Bigger, balanced catalog** — at least 5–10 songs per genre so that genre matching creates real competition rather than an automatic win for the only song with that label.
3. **Conflict detection** — before scoring, check if the user's targets are internally contradictory (e.g., max energy + max acousticness almost never coexist). Flag the conflict instead of silently adding up partial scores that mean nothing.

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

The most surprising moment was changing a single weight genre from 2.0 to 1.0 and watching which songs appeared in the top five shift immediately. Before this project algorithmic bias felt like an abstract idea. Here it was one number I chose that produced a change in who gets good recommendations. Building this showed that recommenders do not understand music at all they just add up numbers and find the closest match. That works good when the features are good proxies for what the label means but it fails the moment the proxy breaks down like a sad mood user getting an upbeat gym track. Human judgment still matters most when the system is confident but wrong someone needs to notice that the results feel off decide the weights need changing and check whether the fix actually improved things the algorithm cannot do any of that itself.

