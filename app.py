import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
        index = movies[movies['title'] == movie].index[0]
        distances = similarity[index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])

        names = []
        posters = []
        for i in movies_list[1:6]:
            movie_id = movies.iloc[i[0]].movie_id
            posters.append(fetch_poster(movie_id))
            names.append(movies.iloc[i[0]].title)
        return names,posters

st.header('Movie Recommender System')

movie_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[idx])
            st.image(recommended_movie_posters[idx])

