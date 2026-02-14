import pickle
from rapidfuzz import process, fuzz

# Load precomputed model
with open("artifacts/similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

with open("artifacts/movie_index.pkl", "rb") as f:
    movie_titles = pickle.load(f)

with open("artifacts/popular.pkl", "rb") as f:
    popular_movies = pickle.load(f)


def find_closest_movie(query, threshold=55):

    candidates = [
        title for title in movie_titles
        if query.lower() in title.lower()
    ]

    if len(candidates) > 0:
        return candidates[0]

    match = process.extractOne(
        query,
        movie_titles,
        scorer=fuzz.WRatio
    )

    if match and match[1] >= threshold:
        return match[0]

    return None


def recommend(movie_name, top_n=5):

    matched_movie = find_closest_movie(movie_name)

    if matched_movie is None:
        return {
            "matched_movie": None,
            "recommendations": popular_movies[:top_n],
            "note": "Showing popular movies instead"
        }

    movie_index = movie_titles.index(matched_movie)

    similarity_scores = list(enumerate(similarity[movie_index]))

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    recommended_movies = []

    for i in similarity_scores[1:top_n+1]:
        recommended_movies.append(movie_titles[i[0]])

    return {
        "matched_movie": matched_movie,
        "recommendations": recommended_movies
    }
