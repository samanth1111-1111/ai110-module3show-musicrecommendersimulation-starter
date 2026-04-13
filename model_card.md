# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatcher 1.0**

A rule-based music recommender that scores songs against a listener's stated preferences and returns the top five best matches.

---

## 2. Intended Use

VibeMatcher is designed to suggest songs from a small catalog based on what a user tells it they like. You give it a genre, a mood, and a few audio preferences (how energetic, how acoustic, how fast), and it ranks every song in the catalog by how closely it matches those preferences.

It is built for classroom exploration, not production. It assumes the user can describe their taste in advance — it does not learn from listening history or adapt over time. It should not be used to make recommendations for real users in a real app, because it has no privacy protections, no user data handling, and a tiny 20-song catalog that does not represent real musical diversity.

**Not intended for:** personalized streaming services, commercial deployment, or any context where fairness across music genres and listener backgrounds matters.

---

## 3. How the Model Works

Think of it like a points system. Every song starts at zero. Then the system checks a few things:

- **Genre match** — if the song's genre label exactly matches what the user said they like, it earns 1 point.
- **Mood match** — if the song's mood exactly matches (e.g., "happy," "chill," "intense"), it earns another 1 point.
- **Energy closeness** — songs close to the user's preferred energy level earn up to 3 points. Songs far away earn fewer. This is the most powerful factor.
- **Acousticness, tempo, valence, and danceability** — each adds a smaller bonus based on how close the song's number is to what the user wants.

All points are added up, and the five songs with the highest totals are recommended. Songs are never filtered out entirely — even a heavy metal track can appear in a jazz recommendation list if its numbers happen to be close enough.

The original genre weight was 2.0 and energy was 1.5. After experimenting, genre was reduced to 1.0 and energy was raised to 3.0, which made recommendations feel more driven by actual sound and less by label.

---

## 4. Data

The catalog contains **20 songs** stored in a CSV file. Each song has: title, artist, genre, mood, energy (0–1), tempo in BPM, valence (positivity, 0–1), danceability (0–1), and acousticness (0–1).

**Genres represented:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, classical, R&B, country, EDM, folk, metal, soul, reggae, blues. Most genres have only one song each.

**Moods represented:** happy, chill, intense, focused, relaxed, moody, energetic, melancholic, romantic, nostalgic, euphoric, sad, angry, uplifting, peaceful, brooding.

**Gaps in the data:**
- No Latin, K-pop, afrobeats, or world music.
- Almost every genre has exactly one song, so there is no real competition within a genre.
- The catalog skews toward English-language Western music.
- No songs represent genre blends (e.g., jazz-hop, country-rock).

No songs were added or removed from the original starter dataset.

---

## 5. Strengths

The system works best when a user's preferred genre has at least one song that also closely matches their audio preferences. In those cases, the top result feels genuinely right.

- **High-Energy Pop listener** → Sunrise City ranked #1. It is pop, happy, moderately fast, and bright — a natural fit that matched intuition immediately.
- **Chill Lofi listener** → Library Rain and Midnight Coding filled the top two spots. Both are genuine lofi/chill tracks with slow tempos and high acousticness. The margin between them (7.61 vs 7.48) correctly reflected that Library Rain's energy was slightly closer to the target.
- **Transparent explanations** — every recommendation shows exactly which factors contributed and by how many points. You can always see *why* a song ranked where it did, which makes the system easy to audit and debug. This is something most real recommenders cannot offer.

---

## 6. Limitations and Bias

**Genre Scarcity Creates a Hard Filter Bubble.** Because 15 of the 20 songs in the catalog belong to unique genres (one rock song, one jazz song, one metal song, etc.), the genre match bonus effectively acts as a hard ceiling rather than a soft preference signal. A user who prefers rock will always receive Storm Runner as their top result regardless of how poorly it matches their energy, tempo, or valence targets — simply because no other rock song exists to compete with it. This means the system is not recommending the *best* match for the user; it is recommending the *only* match, which is a false sense of personalization. The bias disproportionately affects users of niche or underrepresented genres, while pop and lofi listeners (who have 2 songs each) at least get a small ranking competition. To address this, the catalog would need multiple songs per genre, or the genre weight should be reduced further so that a near-perfect audio match in a different genre can realistically outrank a poor same-genre match.

**Other limitations:**
- The system cannot handle multi-genre users. If you like both jazz and blues, you declare one genre and the other is ignored entirely.
- Mood matching is all-or-nothing. "Sad" and "melancholic" are treated as completely different, even though a human would consider them close.
- Contradictory preferences (e.g., maximum energy AND maximum acousticness) produce arbitrary results. The system adds up partial scores rather than flagging the conflict.
- There is no diversity enforcement. The same artist could theoretically fill all five slots if they had multiple songs with similar audio profiles.

---

## 7. Evaluation

Five user profiles were tested: **High-Energy Pop**, **Chill Lofi**, **Deep Intense Rock**, and two adversarial edge cases (a conflicting High-Energy + Sad Mood pop listener, and an All-Extremes jazz/moody profile with physically impossible targets).

For the standard profiles, the top results were largely sensible — Sunrise City for the pop listener, Library Rain for the lofi listener, and Storm Runner for the rock listener — which confirmed that the scoring logic behaves correctly when the catalog contains a clear best match.

The most surprising result was from the **All-Extremes edge case**: the system returned Coffee Shop Stories (a quiet jazz café track) as the top pick for a profile that simultaneously requested maximum energy and maximum acousticness. It won purely because the `jazz` genre tag gave it a free point head start, even though its actual audio numbers were a terrible fit.

A second experiment changed the genre weight from 2.0 down to 1.0 and doubled the energy weight to 3.0. This caused the **Chill Lofi** profile to surface an ambient track (Spacewalk Thoughts) over a third lofi track (Focus Flow), because the ambient song's energy of 0.28 was a closer numerical match than Focus Flow's 0.40 — which actually felt more musically accurate.

The adversarial profiles revealed that the system has no mechanism to resolve contradictions: a user who wants high energy *and* low valence (sad but intense) simply gets whichever pop song is closest to the energy target, with no awareness that the mood conflict is unusual.

---

## 8. Future Work

**1. Soft genre matching.** Instead of a binary genre check, assign partial credit for related genres. A blues fan should get some points for a soul or R&B song, not zero. This would reduce filter bubbles and surface cross-genre discoveries that a human curator would naturally make.

**2. Bigger and more balanced catalog.** Twenty songs is too small to produce real variety. A production version would need at least 5–10 songs per genre, covering a wider range of cultures and styles, so that genre matching creates genuine competition rather than automatic wins for the only song wearing that label.

**3. Conflict detection for contradictory profiles.** Before scoring, check whether the user's targets are internally consistent (e.g., high energy + high acousticness almost never coexist in real music). Flag the conflict and either ask the user to clarify or split the weight between the competing signals rather than blindly adding partial scores that produce a confident but meaningless answer.

---

## 9. Personal Reflection

**Biggest learning moment:** The weight experiment made algorithmic bias feel concrete for the first time. Changing genre from 2.0 to 1.0 — a single number in a single line of code — shifted which songs appeared in the top five for two profiles and brought an ambient track ahead of a genre-matched lofi one. Before this project, "bias in algorithms" felt like an abstract concept people talked about in articles. Here it was visible: a deliberate number I chose, producing a measurable and different kind of unfairness depending on which value I picked.

**How AI tools helped, and when I double-checked them:** Using Agent Mode to apply the weight shift and verify the new maximum score (8.25) saved time and avoided a small arithmetic mistake I would likely have made manually. But the agent could only verify that the math *summed correctly* — it could not tell me whether 3.0 for energy was a *good* weight or whether the change made the system fairer. I had to run the simulation myself and compare the outputs to musical intuition to judge that. The tool handled the mechanical work; the judgment call was still mine.

**What surprised me about simple algorithms "feeling" like recommendations:** The system has no taste, no memory, and no understanding of music — it just adds up six numbers per song. And yet, for the Chill Lofi profile, the top two results genuinely felt right. Library Rain and Midnight Coding are exactly what you would queue up for late-night studying. That feeling is not magic; it happens because the numbers (low energy, slow tempo, high acousticness) are a decent proxy for what "chill lofi" means acoustically. The surprise is how much you can simulate understanding with simple arithmetic if your features are well-chosen. The failure cases — the jazz song winning on energy=1.0, Gym Hero surfacing for a sad-mood listener — reveal the exact moments where the proxy breaks down and the numbers stop mapping to human experience.

**What I would try next:** I would replace the exact genre match with a genre similarity table — a small lookup that gives partial credit for related genres (rock ↔ metal = 0.6, jazz ↔ blues = 0.7, pop ↔ indie pop = 0.8). This single change would break the single-song filter bubble for niche genres without requiring a larger dataset, and it would let musically adjacent styles compete on a level playing field for the first time.
