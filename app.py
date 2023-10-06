import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from ApI
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

similarity = pickle.load(open('similarity.pkl','rb'))
movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

st.markdown("<h1 style='color: white;'>Movie Recommender System</h1>", unsafe_allow_html=True)

#st.title('Movie Recommender System')
st.markdown(
    """
    <style>
    .main {
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("<h5 style='color: white;'>Enter the name of a movie you like, and we will recommend similar movies for you</h5>", unsafe_allow_html=True)
selected_movie_name = st.selectbox(
'',
movies['title'].values)

custom_css = """
<style>
div.stButton > button {
    color: red; /* Change 'red' to the color of your choice */
}
</style>
"""

# Display the custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])

