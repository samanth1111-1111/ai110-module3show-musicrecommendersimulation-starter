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

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

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

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

