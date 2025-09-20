🔥 Step 1: Frame the MVP Clearly
Your end goal:
A swipe-based UI (like Tinder/Instagram) → left = dislike, right = like.

A recommendation backend that balances exploitation (similar styles to likes) and exploration (new/unexpected items).

A demo that feels addictive even if the logic is basic.

You’re not being judged on scaling to 10M users. You’re judged on accuracy, adaptability, creativity, balancing, usability.

🔥 Step 2: Data Pipeline (4–6 hours)
Dataset: Each product has image, brand, price, attributes.

Image Embeddings: Use CLIP (OpenAI’s CLIP or HuggingFace version) to turn images into vectors.

Metadata Embeddings: Convert brand, price, style tags into embeddings (e.g., sentence-transformers).

Vector DB: Use FAISS (quick) or Pinecone (if allowed cloud).

📌 Deliverable: Each product = combined embedding (image + attributes). Stored in FAISS index.

🔥 Step 3: Recommendation Logic (10–12 hours)
Start simple, then add innovation:
Exploitation (core):

When user likes an item → fetch top-K similar from FAISS.

When user dislikes → downweight similar items in the queue.

Exploration (creativity):

Add a small random % of dissimilar items (so the feed doesn’t stagnate).

Maybe weight in brand diversity or price range diversity.

Adaptability:

Track recent swipes in session memory.

Use exponential decay → recent swipes matter more than old ones.

Preference balancing:

If user hates 4 red dresses → gradually suppress reds overall.

If they like 3 floral prints → surface florals more often.

📌 Deliverable: A function recommend(user_id, last_swipe) that returns the next item ID.

🔥 Step 4: Frontend MVP (6–8 hours)
Use React + Tailwind + Framer Motion → fast swipe UI.

Integrate with backend /swipe and /recommendation endpoints.

Show product image + brand + price.

Make it addictive: smooth swipes, instant feedback.

📌 Deliverable: A demo where judges can actually swipe 10–20 items and see personalization in real-time.

🔥 Step 5: Innovation Layer (optional, 4–6 hours)
If you have extra time (and want to win, not just finish), add signals beyond swipes:
Time spent on card before swipe = implicit signal.

Backtracking option → if they undo a swipe, that’s a strong signal.

Diversity meter → ensures they don’t only see one brand/style.

Fashion trend tagging → cluster embeddings into style categories and label (e.g., “streetwear,” “business casual”).

This shows “innovation” beyond vanilla recommendation.

🔥 Step 6: Pitch & Presentation (last 2–3 hours)
Don’t just demo code. They want a story:
Open with problem: “Fashion discovery is broken. Too much choice, boring feeds.”

Show demo: 10 swipes, personalization kicks in.

Explain pillars:

Accuracy → CLIP embeddings.

Adaptability → exponential decay learning.

Innovation → time-spent signals / diversity balancing.

Preference balance → not overreacting to one swipe.

Usability → addictive swipe UI.

End with punchline: “This is fashion discovery as addictive as TikTok.”

✅ Bottom line: Build an MVP. Embeddings + FAISS + swipe UI + adaptive recsys. If you nail usability and personalization in 36 hours, you’ll stand out. Don’t overengineer.
