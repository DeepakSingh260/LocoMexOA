import requests
from django.shortcuts import render
from .models import Movie
from datetime import datetime
def home(request):
    query = request.GET.get('query', '')
    
    if query:
        api_url = f"https://api.themoviedb.org/3/search/movie?api_key=7794df5bb96380f0722ed71cde5e1ba5&query={query}"
        response = requests.get(api_url)
        movies_data = response.json().get('results', [])

      
    else:
        # Retrieve all movies for home page
        api_url = f"https://api.themoviedb.org/3/movie/popular?api_key=7794df5bb96380f0722ed71cde5e1ba5&language=en-US&page=1"
        response = requests.get(api_url)
        movies_data = response.json().get('results', [])
    movies = []
    for data in movies_data:
        try:
            release_date = data.get('release_date')
            if release_date:
                try:
                    release_date = datetime.strptime(release_date, '%Y-%m-%d').date()
                except ValueError:
                    release_date = None  # Handle invalid date format

            # print(release_date)
            movie, created = Movie.objects.get_or_create(
                title=data['title'],
                overview=data['overview'][:100]+"...",
                release_date=release_date,
                poster_path=data.get('poster_path'),
            )
            movies.append(movie)
        except :
            print("something went wrong",data)
    

    return render(request, 'home.html', {'movies': movies, 'query': query})
