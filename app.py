import pickle
import streamlit as st
import requests
import pandas as pd

def fetch_poster(id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=c538a540191056048a994da95ba8a11e".format(id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

# Define your custom CSS
css ="""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500&display=swap');
* {
  box-sizing: border-box;
  font-family: 'Poppins', sans-serif;
}
.container {
  width: 100%;
  height: 10vh;
  display: flex;
  align-items: center;
  justify-content: center;  
}
nav {
  background: linear-gradient(to bottom, #D3D3D3, #A9A9A9);
  padding: 2px;
  border-radius:8px;
}
nav ul {
  padding: 0px;
  display: flex;
  justify-content: center;
}
nav ul li {
  display: inline-block;
  list-style: none;
  font-size: 1rem;
  cursor: pointer;
  position: relative;
  top:5px;
}
nav ul li:after {
  content: '';
  width: 0;
  height: 2px;
  background: #2192ff;
  position: absolute;
  bottom: -5px;
  display:block;
  transition: 0.5s;
}
nav ul li:hover::after {
  width: 100%;
}
.stButton button {
    background: linear-gradient(to bottom, #4CAF50, #2E7D32);
    border: none;
    color: white;
    padding: 10px 24px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 26px;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 8px;
    transition: background-color .3s, transform .3s;
}
.stButton button:hover {
    background-color: #004d99;
    transform: scale(1.05);
}
.stSelectbox div {
    font-family: 'Arial', sans-serif;
    font-size: 18px;
}
.stText {
    color: #0066cc;
    font-size: 14px;
    font-family: 'Arial', sans-serif;
}
.movie-container {
    text-align: center;
    font-family: 'Arial', sans-serif;
    font-weight: bold;
    margin: 10px 5px;
    display: inline-block;
    transition: transform .3s, color .3s;
    width:100%;    
}
.movie-container:hover .movie-poster {
    transform: scale(1.1);
}
.movie-container:hover .movie-name {
    color: white;
    transform: scale(1.1);
    }
.movie-poster {
    border: 1px solid #cccccc;
    border-radius: 12px;
    box-shadow: 2px 2px 8px #aaaaaa;
    width:100%;
    transition: transform .3s;
}
.movie-column {
    padding: 10px;
}
.header {
    position: relative;
    padding: 60px;
    text-align: center;
    font-size: 30px;
    font-family:  'Poppins', sans-serif;
    font-weight:bold;
    text-shadow: 5px 2px 5px rgba(0, 0, 0, 0.7);
    color: white;
    border-radius: 12px;
    margin-bottom: 30px;
    background-image: url('https://miro.medium.com/v2/resize:fit:732/1*O0Yw5NAmnMGxcYkEXZ-L5Q.jpeg');
    background-size: cover;
    background-position: center;
    background: linear-gradient(to right, #000000, rgba(0, 0, 0,0)),url('https://miro.medium.com/v2/resize:fit:732/1*O0Yw5NAmnMGxcYkEXZ-L5Q.jpeg');
}
.movie-name {
    margin-top: 10px;
    font-size: 16px;
    color: #696969;
}
.footer {
    position: relative;
    top:450px;
    width: 100%;
    text-align: center;
    padding: 3px;
    font-family: 'Arial', sans-serif;
    font-size: 14px;
}
.footer a {
    color: white;
    text-decoration: none;
    margin: 0 10px;
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)
# Header section
st.markdown("<div class='header'>Movie Recommendation System</div>", unsafe_allow_html=True)

movies = pd.read_pickle("movies_list.pkl")
similarity = pd.read_pickle("similarity.pkl")

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)
    for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
        with col:
            st.markdown(
                f"<div class='movie-container'><img src='{poster}' class='movie-poster'/><div class='movie-name'>{name}</div></div>",
                unsafe_allow_html=True)
# Footer section
st.markdown("""
<div class='footer'>
    <nav>
        <ul>
            <li><a href='#'>About</a></li>
            <li><a href='#'>Contact</a></li>
            <li><a href='#'>Privacy Policy</a></li>
            <li><a href='#'>feedback</a></li>
        </ul>
    </nav>
</div>
""", unsafe_allow_html=True)


