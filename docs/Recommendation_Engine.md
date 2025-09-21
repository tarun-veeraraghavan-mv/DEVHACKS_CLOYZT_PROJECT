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

## 3. The Learning Mechanism: Real-time Style Adaptation via SGD

The engine learns a user's style in real-time with every swipe using an online learning approach with **Stochastic Gradient Descent (SGD)**. Instead of just averaging vectors, this method treats the recommendation as a modeling problem, actively trying to minimize the error between its predictions and the user's actions.

The process for each swipe is as follows:

1.  **Predict Preference**: The system first predicts how much the user will like an item by calculating the dot product of the user and item vectors.
    - `predicted_rating = dot(user_vector, item_vector)`

2.  **Calculate Error**: It then measures the error between the prediction and the user's actual swipe (where a "like" is `+1` and a "dislike" is `-1`).
    - `error = actual_rating - predicted_rating`

3.  **Update User Vector**: Finally, it updates the user's vector using the SGD update rule, which pushes the vector in a direction that minimizes the error.
    - `new_user_vector = user_vector + alpha * (error * item_vector - lambda * user_vector)`

The parameters are:
-   `alpha` (Learning Rate): Controls how large of a step to take in updating the vector.
-   `lambda` (Regularization): A parameter that prevents the user's vector from growing too large and overfitting to recent items.

This method is more powerful than simple averaging because it's a true learning rule that actively builds a predictive model of a user's taste.

## 4. Recommendation Generation: A Hybrid Approach

The engine uses a hybrid strategy that explicitly combines exploration and exploitation to ensure the feed is both relevant and surprising.

-   **Exploration (20% Chance)**: With a 20% probability on any given swipe, the system enters **"discovery mode."** It bypasses the complex recommendation logic and instead fetches a completely random item that the user has never seen before. This is crucial for serendipity, preventing the user from getting stuck in a "filter bubble" and keeping the experience fresh.

-   **Exploitation (80% Chance)**: For the other 80% of cases, the system **exploits the user's learned preferences**. It takes the newly updated `user_vector` and queries the Pinecone vector database for the **top 150 items** that are most similar. It then filters this list to remove any items the user has already swiped on, guaranteeing the recommended item is new to them. Using a large search pool (`top_k=150`) makes this process highly robust and ensures a virtually infinite feed of personalized content.

## 5. Preference Balancing: Long-Term Style vs. Short-Term Swipes

The system is designed to learn broad preferences without overreacting to a single action.

-   **Short-Term Adaptability**: A swipe right on a teal mini-dress will immediately influence the `user_vector`, increasing the likelihood of seeing similar dresses.
-   **Long-Term Learning**: One "dislike" on a red dress won't banish the color forever. However, as the user consistently dislikes red items, the SGD learning rule will continuously update the `user_vector`, pushing it away from the "red" region of the vector space and making such recommendations less frequent over time.

## 6. Future Enhancements & Innovation

The current design serves as a powerful foundation, with several planned improvements to enhance its sophistication further:

-   **Dynamic Learning Rate**: Adjusting `alpha` based on user history (e.g., higher for new users, lower for established users).
-   **Separate Like/Dislike Vectors**: Maintaining two separate vectors for a user's likes and dislikes to model their preferences with greater nuance.
-   **Time Decay**: Giving more weight to recent swipes and gradually "forgetting" older interactions to keep the profile fresh and relevant.
-   **Diversity Constraints**: Ensuring the feed doesn't show items that are too visually similar to each other in succession.