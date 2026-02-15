from fastapi import FastAPI
from .model import recommend, find_closest_movie
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Movie Recommendation API Running"}


@app.get("/search")
def search_movie(query: str):
    result = find_closest_movie(query)
    if result is None:
        return {"message": "No movie found"}
    return {"matched_movie": result}


@app.get("/recommend")
def recommend_movie(movie: str):
    result = recommend(movie)
    if result is None:
        return {"message": "Movie not found"}
    return result
