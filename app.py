import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import os

# ========== Download similarity.pkl from Google Drive if not present ==========
file_id = "10zEYCuuQr3fEZKAUrt2Njbq4TRIbwGck"
output_path = "similarity.pkl"
url = f"https://drive.google.com/uc?export=download&id={file_id}"
if not os.path.exists(output_path):
    gdown.download(url, output_path, quiet=False)

# ========== Load similarity and movie_dict ==========
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))  # This will now exist

movies = pd.DataFrame(movie_dict)

# ========== Functions ==========
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

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
    return names, posters

# ========== Streamlit App ==========
st.header('Movie Recommender System')
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[idx])
            st.image(recommended_movie_posters[idx])
