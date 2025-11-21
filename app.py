import streamlit as st
import pickle
import pandas as pd
import requests

api_key = "e6a3b3102116d11e80b4c820ba9356a5"

movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie_name, api_key):
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}"
    response = requests.get(search_url)
    data = response.json()
    if data['results']:
        poster_path = data['results'][0]['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500" + poster_path
        return full_path
    else:
        return None

def recommend(movie, topk=5):
    if movie not in movies['title'].values:
        return []
    idx = movies[movies['title'] == movie].index[0]
    distances = similarity[idx]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1: topk+1]
    recs = [movies.iloc[i[0]].title for i in movie_list]
    return recs

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide",
)

st.markdown(
    "<h1 style='font-family: Roboto, sans-serif; font-weight:700; font-size:50px; text-align:center;'>🎬 Movie Recommender System</h1>",
    unsafe_allow_html=True
)

option = st.selectbox('Choose a movie 🎬', movies['title'].values)

if st.button('Recommend'):
    recommendations = recommend(option)
    
    if recommendations:
        st.markdown(
            "<h2 style='font-family: Roboto, sans-serif; font-weight:700; font-size:30px;'>Top Recommendations:</h2>",
            unsafe_allow_html=True
        )
        
        cols = st.columns(len(recommendations))
        for idx, movie in enumerate(recommendations):
            poster = fetch_poster(movie, api_key)
            rating = movies[movies['title'] == movie]['vote_average'].values[0]
            with cols[idx]:
                if poster:
                    st.image(poster, use_container_width=True)
                st.markdown(
                    f"<p style='font-family: Roboto, sans-serif; font-weight:400; font-size:16px; text-align:center;'>{movie} ⭐ {rating}</p>",
                    unsafe_allow_html=True
                )
    else:
        st.info("No recommendations found.")
