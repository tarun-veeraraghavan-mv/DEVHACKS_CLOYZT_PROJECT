1️⃣ Image embeddings
Current: You’re using CLIP “as-is” → get_image_features, normalized, stored in Pinecone.
Pros: Standard, works out-of-the-box.
Cons & improvements:
Single modality: Only visual features, ignores price, brand, category. Judges love clever signal combination.

Actionable improvement:

Concatenate metadata embeddings (price, brand, style tags) with CLIP vector. For example:

metadata_vector = np.array([price_normalized, brand_encoded, style_encoded])
combined_vector = np.concatenate([clip_vector, metadata_vector])
→ gives a richer representation of fashion taste.

Batch processing: Use torch.no_grad() + batches if the catalog is big (~1000 items per brand) for speed.

2️⃣ User profile & update
Current: user_vector updated with EWMA-style formula per swipe.
Pros: Simple, works, adapts slowly.
Cons & improvements:
Alpha is static: All swipes have equal weight.

Improvement: dynamic alpha:

Increase alpha for new users (cold start).

Decrease alpha for experienced users to prevent swings.

Separate like/dislike vectors: Instead of direction=1/-1, maintain:

user_like_vector += alpha _ item_vector
user_dislike_vector += alpha _ item_vector
user_vector = user_like_vector - user_dislike_vector
→ better long-term vs short-term preference modeling.

Time-decay swipes: Old dislikes/likes fade:

user_vector \*= decay_rate # e.g., 0.99 per N swipes
→ prevents a single “bad” swipe from permanently skewing the feed.

3️⃣ Query & recommendation
Current: Query Pinecone with user vector → get top-k nearest.
Pros: Works.
Cons & improvements:
No exploration: Right now it’s pure exploitation.

Solution: Mix exploration items:

top_k = 3
top_matches = pinecone_query(user_vector, top_k=int(top_k*0.8))
random_explore = sample_random_items(top_k=int(top_k*0.2))
final_feed = top_matches + random_explore

Diversity constraint: Filter out items too similar to last N swipes to prevent repeats.

Weighted scoring: Combine Pinecone similarity with metadata-based boosts (brand loyalty, price preference).

4️⃣ Backend performance
Current: Every swipe queries + updates Pinecone immediately.

Improvements:

Batch updates for speed: accumulate 5–10 swipes and update vector to avoid Pinecone throttling.

Async handling: Use async queries to avoid blocking user interface.

5️⃣ Experiment tracking
Hackathon judges will test accuracy and adaptability. Track internally:

How often recommendations match actual next swipe.

How fast user vector adapts after several likes/dislikes.

Maintain a small local cache of recent interactions to tune alpha or exploration ratio in real-time.

6️⃣ Optional hacks for “wow” factor
Multi-modal embeddings: Combine CLIP + color palette + brand + text tags.

Cluster user tastes: Keep small clusters for quick cold-start recommendations.

Reranking: After top-k, rerank by price, brand, or novelty to increase engagement.

Visual diversity: Avoid showing three teal mini-dresses in a row.

7️⃣ Immediate next step
Upgrade user profile to like/dislike vector separation with decay.

Add exploration in recommendations (20% randomness).

Optionally concatenate metadata to CLIP vector → richer embeddings.

Track swipe history → use for dynamic alpha & diversity.
