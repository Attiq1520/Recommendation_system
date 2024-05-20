# recommendations/views.py

from django.shortcuts import render, redirect
from .models import Movie
from .similarity_functions import (
    genre_based_similarity,
    director_based_similarity,
    actor_based_similarity,
    plot_based_similarity,
    poster_based_similarity,
)

def search_movie(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            # Find the selected movie based on the search query
            try:
                selected_movie = Movie.objects.get(title__icontains=query)
                # Redirect to the recommendation view with the selected movie ID
                return redirect('recommend', movie_id=selected_movie.id)
            except Movie.DoesNotExist:
                movies = Movie.objects.filter(title__icontains=query)
                return render(request, 'search.html', {'movies': movies, 'error': 'Movie not found'})
        else:
            movies = Movie.objects.all()
            return render(request, 'search.html', {'movies': movies})

def recommend(request, movie_id):
    #movie = Movie.objects.get(movie_id=movie_id)
    #recommendations = {
        #'genre': genre_based_similarity(movie_id),
        #'director': director_based_similarity(movie_id),
        #'actors': actor_based_similarity(movie_id),
        #'plot': plot_based_similarity(movie_id),
        #'poster': poster_based_similarity(movie_id),
    #}
    #return render(request, 'recommend.html', {'movie': movie, 'recommendations': recommendations})
    try:
        selected_movie = Movie.objects.get(id=movie_id)
        recommended_movies = get_recommendations(selected_movie)
        return render(request, 'recommend.html',
                      {'selected_movie': selected_movie, 'recommended_movies': recommended_movies})
    except Movie.DoesNotExist:
        return redirect('search_movie')  # Redirect back to search if movie not found
