import streamlit as st
import pickle
import pandas as pd
import requests
import bz2file as bz2

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=5ce9ff81f9596d0d9b5d38ec5cdeeef6&language=en-US'.format(movie_id))
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/'+data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity_matrix[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

def decompress_pickle(file):
    data = bz2.BZ2File(file, 'rb')
    data = pickle.load(data)
    return data

similarity_matrix = decompress_pickle('similarity.pbz2')

st.title('Movies Recommender System')
selected_movie_name = st.selectbox('Select a movie',movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    #Please replace st.beta_columns with st.columns. st.beta_columns will be removed after 2021-11-02.
    for i, col in enumerate(st.columns(5)):
        with col:
            st.text(names[i])
            st.image(posters[i])
