import pandas as pd
import difflib
import sys

movie_list = sys.argv[1]
movie_ratings = sys.argv[2]
output_file = sys.argv[3]

colnames=['title']
movie_list=pd.read_csv(movie_list, header=None, names=colnames)

movie_ratings=pd.read_csv(movie_ratings)

def get_movie_title(word):
    matches = difflib.get_close_matches(word, movie_list['title'], n=500,cutoff=0.6)
    return matches


movie_ratings['title']=movie_ratings['title'].apply(lambda title: get_movie_title(title))
movie_ratings['title']=movie_ratings.title.apply(''.join)

movie_ratings = movie_ratings[movie_ratings.title != ''] 
movie_ratings = movie_ratings.reset_index(drop=True)

movie_ratings = movie_ratings.groupby('title', 0).mean().reset_index()

output = movie_list.merge(movie_ratings, on='title')
output['rating'] = output['rating'].round(2)
output.to_csv(output_file)

