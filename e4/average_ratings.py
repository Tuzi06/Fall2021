import pandas as pd
import numpy as np
import sys
import difflib


movie_list= open(sys.argv[1]).readlines()
rating = pd.read_csv(sys.argv[2])

# print (movie_list)

movie = difflib.get_close_matches('Man on Fire',movie_list)

print(movie)