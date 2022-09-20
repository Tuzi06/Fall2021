import pandas as pd
import sys
import difflib


# movie_list= open(sys.argv[1]).readlines(0:-1)
movie_list = pd.read_csv(sys.argv[1],sep = '\n', names= ['title'])
rating = pd.read_csv(sys.argv[2])

# print (type(movie_list))
def match(title):
    return difflib.get_close_matches(title,movie_list['title'],n=10000)

rating['true_title']= rating['title'].apply(match)
rating['true_title']= rating.true_title.apply(''.join)
rating= rating[rating['true_title']!='']
rating = rating.reset_index()

output =rating.groupby(['true_title']).mean().reset_index()
output = output.loc[:,output.columns != 'index']
output = output.rename(columns= {'true_title':'title'})

output = movie_list.merge(output, on='title',how ='left')
output['rating'] = output['rating'].round(2)
output = output.fillna(0)

output.to_csv(sys.argv[3],index = False)