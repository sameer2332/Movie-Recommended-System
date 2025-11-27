import streamlit as st 
import pickle
import pandas as pd
import requests

# Function to fetch poster from TMDb API
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data.get('poster_path', "")
    except Exception as e:
        print(f"Error fetching poster for movie_id {movie_id}: {e}")
        return "https://via.placeholder.com/300x450.png?text=No+Image"

# Function to recommend movies
def recommend(movie_title):
    movie_index = movies[movies['title'] == movie_title].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id  
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    
    return recommended_movies, recommended_movies_poster


movies = pickle.load(open('movie.pkl', 'rb'))       
similarity = pickle.load(open('similarity.pkl', 'rb'))  


st.title('Movie Recommender System')

movie_list = movies['title'].values
selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:',
    movie_list
)

if st.button('Recommend'):
    names, poster = recommend(selected_movie_name)
    
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(poster[0])
    with col2:
        st.text(names[1])
        st.image(poster[1])
    with col3:
        st.text(names[2])
        st.image(poster[2])
    with col4:
        st.text(names[3])
        st.image(poster[3])
    with col5:
        st.text(names[4])
        st.image(poster[4])
