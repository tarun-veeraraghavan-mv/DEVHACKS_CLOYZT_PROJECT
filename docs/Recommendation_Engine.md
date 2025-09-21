# The Clozyt Recommendation Engine: A Technical Summary

This document provides a detailed overview of the machine learning recommendation engine designed for the Clozyt fashion discovery platform. The engine is built to be accurate, adaptive, and innovative, creating an "addictive" user experience that balances showing users what they love (exploitation) with introducing them to new styles (exploration).

## 1. Core Concept: Vector-Based Personalization

At its heart, the engine represents both clothing items and user preferences as numerical vectors in a high-dimensional space.

-   **Item Vector**: A numerical signature that captures the essence of a clothing item (e.g., its visual style, color, brand, price).
-   **User Vector**: A numerical signature that represents a user's unique fashion taste.

The core principle is simple: if we can represent items and users in the same vector space, we can recommend items whose vectors are "closest" to the user's vector. The magic lies in how these vectors are created and updated.

## 2. Item Representation: Turning Fashion into Data

To create a rich, nuanced representation of each clothing item, the engine combines multiple signals into a single `item_vector`.

-   **Visual Embeddings (CLIP)**: The primary signal is the product's image. We use OpenAI's **CLIP (Contrastive Language–Image Pre-training)** model to generate a dense vector embedding from the image. This vector captures a vast amount of visual information, including colors, shapes, textures, and abstract styles (e.g., "bohemian," "formal").
-   **Metadata Embeddings**: Visuals alone are not enough. Other attributes are converted into numerical form and concatenated with the CLIP vector. This includes:
    -   **Price**: Normalized to a standard range.
    -   **Brand/Category/Style**: Encoded into a numerical format (e.g., using one-hot or multi-hot encoding).

The result is a `combined_vector` that holistically represents the item, allowing the engine to understand the difference between a cheap, white t-shirt from one brand and an expensive, white blouse from another.

## 3. The Learning Mechanism: Adapting to Swipes

The engine learns a user's style in real-time with every swipe. This is achieved by updating the `user_vector` using a well-established formula that incorporates a learning rate.

The formula is:
**`updated_user_vector = (1 - alpha) * current_user_vector + alpha * direction * item_vector`**

Where:
-   `current_user_vector`: The user's existing style profile.
-   `item_vector`: The vector of the item the user just swiped on.
-   `direction`: **+1** for a "like" (swipe right) and **-1** for a "dislike" (swipe left).
-   `alpha` (Learning Rate): A parameter that controls how much a single swipe influences the user's profile. A higher alpha means preferences change more quickly.

When a user likes an item, their `user_vector` is pulled slightly closer to that `item_vector`. When they dislike an item, it's pushed away. This allows the user's profile to continuously evolve, adapting to their changing tastes.

## 4. Recommendation Generation: Balancing Exploitation & Exploration

A successful recommendation feed must balance showing users what they want with helping them discover new things.

-   **Exploitation**: To show users items similar to what they've liked, the system uses the updated `user_vector` to query a vector database (like FAISS or Pinecone). The database performs a nearest neighbor search to find and return the `item_vectors` that are most similar (closest) to the user's profile.
-   **Exploration**: To prevent the feed from becoming repetitive, the engine introduces novelty. A certain percentage of the recommendations (e.g., 20%) are reserved for items that are not necessarily a close match but are sampled from a wider, more random pool. This is the key to surfacing unexpected styles and keeping the experience "addictive."

## 5. Preference Balancing: Long-Term Style vs. Short-Term Swipes

The system is designed to learn broad preferences without overreacting to a single action.

-   **Short-Term Adaptability**: A swipe right on a teal mini-dress will immediately increase the likelihood of seeing similar dresses.
-   **Long-Term Learning**: One "dislike" on a red dress won't banish the color forever. However, if the user consistently dislikes red items, their `user_vector` will gradually drift away from the "red" region of the vector space, making such recommendations less frequent over time. The system learns the user's broader style by aggregating their interactions.

## 6. Future Enhancements & Innovation

The current design serves as a powerful foundation, with several planned improvements to enhance its sophistication further:

-   **Dynamic Learning Rate**: Adjusting `alpha` based on user history (e.g., higher for new users, lower for established users).
-   **Separate Like/Dislike Vectors**: Maintaining two separate vectors for a user's likes and dislikes to model their preferences with greater nuance.
-   **Time Decay**: Giving more weight to recent swipes and gradually "forgetting" older interactions to keep the profile fresh and relevant.
-   **Diversity Constraints**: Ensuring the feed doesn't show items that are too visually similar to each other in succession.
