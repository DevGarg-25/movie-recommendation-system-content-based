''' importing libraries we will require in this project'''
import pandas as pd
import numpy as np
import ast
import pickle



'''creating dataframes from our csv dataset'''

movies = pd.read_csv('tmdb_5000_movies.csv')

'''we can check if our dataframe is created successfully using the command:'''

# print(movies.head()) 

credits = pd.read_csv('tmdb_5000_credits.csv')

# print(credits.head())

'''Now I am merging both of my dataframes into one based on title'''

movies = movies.merge(credits,on='title')

# print(movies.head()) 

'''Selecting only useful columns for movie recommendation'''

movies = movies[['title','genres','id','keywords','overview','popularity','release_date','runtime','vote_average','vote_count','cast','crew']]

# print(movies.head()) 

''' Check if there is any empty slots in our data'''

# print(movies.isnull().sum())

'''since the missing data is very less we will drop '''

movies.dropna(inplace=True)

'''check for empty slots again, just to be sure that there is no more empty slots'''

# print(movies.isnull().sum())

# print(movies['genres'][0])

'''
Now we have some columns in weird dictionary format, we need them in string format
as we can see that the genres we require are in the name
So, writing a function to extract the genres
'''

def convert(obj):
    L=[]
    for i in ast.literal_eval(obj):
        L.append(i['name'].lower())
    return L

movies['genres'] = movies['genres'].apply(convert)

'''Now we can see that all the genres are extracted successfully'''

# print(movies['genres'][0])

'''Doing the same for keywords'''

movies['keywords'] = movies['keywords'].apply(convert)

# print(movies['keywords'][0])

# print(movies['crew'][0])

'''
FOR the project I want only dirctor in the crew and only top 5 main actor/actress in the cast
making a function to extract director from crew
As we can see that here we need name for the job Director
So, let's define a function to extract Director from the crew data
'''

def director(obj):
    L=[]
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            L.append(i['name'].lower())
            break
    return L

movies['crew'] = movies['crew'].apply(director)

# print(movies['crew'][0])

'''
job done successfully
Now for Cast , I want top 5 members' name
'''

def actors(obj):
    L=[]
    counter = 0
    for i in ast.literal_eval(obj):
        if counter < 5 :
            L.append(i['name'].lower())
            counter+=1
        else:
            break
    return L

movies['cast'] = movies['cast'].apply(actors)

# print(movies['cast'][0])
# job done successfully

'''now in overview, we will create tags of every one word , so that they can be easily accible'''
movies['overview'] = movies['overview'].apply(lambda x:x.split())

'''  Now remove spaces and join all to make tags in a different Data frame'''

movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew'] = movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['overview'] = movies['overview'].apply(lambda x:[i.replace(" ","") for i in x])
movies['tags'] = movies['cast']+movies['crew']+movies['genres']+movies['keywords']+movies['overview']

# print(movies.head(0))

content_movie = movies[['id','title','tags']]
content_movie['tags'] = content_movie['tags'].apply(lambda x:" ".join(x))

# print(content_movie['tags'][0])

'''
New dataframe content_movie is created successfully
Now let's do text vectorization
for this we are going to use a prebuilt library from sklearn
many words with same meaning repeat in the dataframe so, let's stem them
For this function we will use nltk library functions
'''
from nltk import PorterStemmer
ps = PorterStemmer()

def stem(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

content_movie['tags'] = content_movie['tags'].apply(stem)

'''Stemming is complete now lets make and store vectors in an array'''

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 10000, stop_words = 'english')

vectors = cv.fit_transform(content_movie['tags']).toarray()

# print(cv.get_feature_names())

'''Now let's calculate similarity between the vectors to recommend movie, for this we will use cosine_similarity from sklearn '''

from sklearn.metrics.pairwise import cosine_similarity

similarity = cosine_similarity(vectors)

'''We need both recommended movies and the movie posters so let's make a function to get poster from the tmdb api'''

# import requests

# def fetch_poster(movie_id):
#     response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=4c68244fc74f2be4d90ad4ef780672e4&language=en-US'.format(movie_id))
#     data = response.json()
#     link = "https://image.tmdb.org/t/p/w500"+ data['poster_path']
#     return link

''' Now let's finally define a function to recommend movies based on content '''

def recommend(movie):
    movie_index = content_movie[content_movie['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x:x[1])[1:11]

    movie_on_content = []
    # posters_on_content = []

    for i in movies_list:
        movie_id = content_movie.iloc[i[0]].id
        movie_on_content.append(movies.iloc[i[0]].title)
        # posters_on_content.append(fetch_poster(movie_id))
    return movie_on_content,#posters_on_content


# print(recommend('Batman'))
'''Add an overview column to the Content_movie dataframe so that we can show that overview under our movies'''
content_movie['overview'] = movies['overview'].apply(lambda x:" ".join(x))

# print(content_movie['overview'][0])
'''Share the final products one is a content_movie data frame and other is our similarity matrix'''
pickle.dump(content_movie.to_dict(),open('movie_dict.pkl','wb'))
pickle.dump(similarity,open('similarity.pkl','wb'))

'''Now we have just made a complete content based movie recommendation system '''
