import streamlit as st
import pickle
import pandas as pd
import requests

# Define a function to to fetch poster from the tmdb api
# My api key is "4c68244fc74f2be4d90ad4ef780672e4&language=en-US"
# We will get our response in Json format , we need to then extract our poster_path from there
# after getting the poster path we add this poster path to the imdb image link

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=4c68244fc74f2be4d90ad4ef780672e4&language=en-US'.format(movie_id))
    data = response.json()
    link = "https://image.tmdb.org/t/p/w500"+ data['poster_path']
    return link

# modify and redefine the recommend function

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x:x[1])[1:11]

    movie_on_content = []
    posters_on_content = []
    overviews = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        movie_on_content.append(movies.iloc[i[0]].title)
        posters_on_content.append(fetch_poster(movie_id))
        overviews.append(movies.iloc[i[0]].overview)

    return movie_on_content,posters_on_content,overviews

# load the data frame from the pkl format


movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

# print(movies.head(0))


# This is the app design we will be using

st.title('A Content Based Movie Recommendation System')

selected_movie_name = st.selectbox(
'Which movie do you like ?',
movies['title'].values)

if st.button('Recommend'):

    st.subheader('So, the movie you liked is :')
    
    movie_index1 = movies[movies['title'] == selected_movie_name].index[0]
    movie_id1 = movies.iloc[movie_index1].id
    
    st.title(selected_movie_name)
    st.image(fetch_poster(movie_id1))
    st.caption(movies.iloc[movie_index1].overview)

    st.title("Some recommended Movies are: ")

    names,posters,overview = recommend(selected_movie_name)

    st.header("Top three recommendations are :")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text(names[0])
        st.image(posters[0])
        st.caption(overview[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])
        st.caption(overview[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])
        st.caption(overview[2])

    st.title(names[3])
    st.image(posters[3])
    st.caption(overview[3])

    st.title(names[4])
    st.image(posters[4])
    st.caption(overview[4])

    st.title(names[5])
    st.image(posters[5])
    st.caption(overview[5])

    st.title(names[6])
    st.image(posters[6])
    st.caption(overview[6])

    st.title(names[7])
    st.image(posters[7])
    st.caption(overview[7])

    st.title(names[8])
    st.image(posters[8])
    st.caption(overview[8])

    st.title(names[9])
    st.image(posters[9])
    st.caption(overview[9])
