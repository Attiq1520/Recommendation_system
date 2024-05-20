import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import imagehash
import os

# Load MovieLens dataset
movies = pd.read_csv(r'C:\Users\AaR\PycharmProjects\Recommendation_finalproject\pythonProject2\polls\ml-25m\movies.csv')
links = pd.read_csv(r'C:\Users\AaR\PycharmProjects\Recommendation_finalproject\pythonProject2\polls\ml-25m\links.csv')

# Set the directory containing poster images
poster_dir = r'C:\Users\AaR\PycharmProjects\MLP-20M\MLP-20M'


# Genre-Based Similarity
def genre_based_similarity(movie_id):
    movie_genres = movies[movies['movieId'] == movie_id]['genres'].values[0]
    similar_movies = movies[movies['genres'].str.contains(movie_genres)]
    return similar_movies['movieId'].values[:5]


# Director-Based Similarity
def director_based_similarity(movie_id):
    movie_director = movies[movies['movieId'] == movie_id]['director'].values[0]
    similar_movies = movies[movies['director'] == movie_director]
    return similar_movies['movieId'].values[:5]


# Actor-Based Similarity
def actor_based_similarity(movie_id):
    movie_actors = movies[movies['movieId'] == movie_id]['actors'].values[0]
    similar_movies = movies[movies['actors'].str.contains(movie_actors)]
    return similar_movies['movieId'].values[:5]


# Plot Description Similarity
def plot_based_similarity(movie_id):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies['plot'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    idx = movies.index[movies['movieId'] == movie_id][0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    movie_indices = [i[0] for i in sim_scores[1:6]]
    return movies['movieId'].iloc[movie_indices].values


# Poster Image Similarity
def poster_based_similarity(movie_id):
    # Construct the path to the poster image of the given movie
    movie_poster_path = os.path.join(poster_dir, f'{movie_id}.jpg')
    movie_poster = Image.open(movie_poster_path)
    movie_hash = imagehash.average_hash(movie_poster)

    similarities = []
    for file in os.listdir(poster_dir):
        if file.endswith('.jpg'):
            poster_id = int(file.split('.')[0])
            poster_path = os.path.join(poster_dir, file)
            poster = Image.open(poster_path)
            hash_ = imagehash.average_hash(poster)
            similarity = 1 - (movie_hash - hash_) / len(movie_hash.hash) ** 2
            similarities.append((poster_id, similarity))

    similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
    return [sim[0] for sim in similarities[:5]]

# Example usage:
# print(genre_based_similarity(1))
# print(director_based_similarity(1))
# print(actor_based_similarity(1))
# print(plot_based_similarity(1))
# print(poster_based_similarity(1))
