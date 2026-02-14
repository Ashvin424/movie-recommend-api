import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
ratings = pd.read_csv("data/ratings.csv")
movies = pd.read_csv("data/movies.csv")

df = pd.merge(ratings, movies, on="movieId")

# Filter popular movies
ratings_count = df.groupby('title')['rating'].count()
popular_movies = ratings_count[ratings_count >= 20].index
filtered_df = df[df['title'].isin(popular_movies)]

# Create matrix
movies_matrix = filtered_df.pivot_table(
    index='title',
    columns='userId',
    values='rating'
)

movies_matrix_filled = movies_matrix.fillna(0)

# Compute similarity
similarity = cosine_similarity(movies_matrix_filled)

# Compute top popular movies (by rating count)
top_popular = ratings_count.sort_values(ascending=False).head(20).index.tolist()

with open("artifacts/popular.pkl", "wb") as f:
    pickle.dump(top_popular, f)


# Save model
with open("artifacts/similarity.pkl", "wb") as f:
    pickle.dump(similarity, f)

with open("artifacts/movie_index.pkl", "wb") as f:
    pickle.dump(movies_matrix.index.tolist(), f)

print("Model saved successfully!")
