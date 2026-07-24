import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?language=en-US'

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3MDJkZTE4ZDc1Y2RkOTc0OTlkMTA1MTlkM2EwODNlMSIsIm5iZiI6MTc4NDg4MDI0NC4yMDcsInN1YiI6IjZhNjMxYzc0NjY2ZjlmYmM1NWY5YTE0NCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.kqsfuZdmK4NibI6aKcI6qYt5nUgdHTFgsKboKwv5oic"
                          }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()

        if data.get('poster_path'):
            return "https://image.tmdb.org/t/p/w500" + data['poster_path']
        else:
            return "https://via.placeholder.com/300x450"

    except Exception:
        return "https://via.placeholder.com/300x450"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
'Select a Movie',
movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(posters[0], use_container_width=True)
        st.write(names[0])

    with col2:
        st.image(posters[1], use_container_width=True)
        st.write(names[1])

    with col3:
        st.image(posters[2], use_container_width=True)
        st.write(names[2])

    with col4:
        st.image(posters[3], use_container_width=True)
        st.write(names[3])

    with col5:
        st.image(posters[4], use_container_width=True)
        st.write(names[4])
