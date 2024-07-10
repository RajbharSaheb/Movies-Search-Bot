# © https://t.me/CyniteBackup

import requests
from bs4 import BeautifulSoup
import urllib.parse

API_KEY = "your_api_key"

def search_movies(query):
    try:
        encoded_query = urllib.parse.quote_plus(query)
        url = f"https://185.53.88.104/?s={encoded_query}"
        website = BeautifulSoup(requests.get(url).text, "html.parser")
        movies_list = []
        for movie in website.find_all("a", {'class': 'ml-mask jt'}):
            title = movie.find("span", {'class': 'mli-info'}).text
            link = movie['href']
            movies_list.append({"title": title, "link": link})
        return movies_list
    except Exception as e:
        return f"Error fetching movie data: {str(e)}"

def get_movie_details(movie_link):
    try:
        movie_page = BeautifulSoup(requests.get(movie_link).text, "html.parser")
        title = movie_page.find("div", {'class': 'mvic-desc'}).h3.text
        img = movie_page.find("div", {'class': 'mvic-thumb'})['data-bg']
        links = movie_page.find_all("a", {'rel': 'noopener', 'data-wpel-link': 'internal'})
        final_links = {}
        for link in links:
            shortened_url = requests.get(f"https://shortnerfly.com/api?api={API_KEY}&url={link['href']}").json()
            final_links[link.text] = shortened_url['shortenedurl']
        return {"title": title, "img": img, "links": final_links}
    except Exception as e:
        return f"Error fetching movie details: {str(e)}"

# Example usage:
query = "Inception"
movies = search_movies(query)
if movies:
    first_movie_link = movies[0]["link"]
    movie_details = get_movie_details(first_movie_link)
    print(movie_details)
else:
    print(f"No movies found for query: {query}")
