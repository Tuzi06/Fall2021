import sys
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

OUTPUT_TEMPLATE = (
    '"Did more/less users use the search feature?" p-value:  {more_users_p:.3g}\n'
    '"Did users search more/less?" p-value:  {more_searches_p:.3g} \n'
    '"Did more/less instructors use the search feature?" p-value:  {more_instr_p:.3g}\n'
    '"Did instructors search more/less?" p-value:  {more_instr_searches_p:.3g}'
)


def main():
    searchdata_file = sys.argv[1]

    # ...
    #all people
    search = pd.read_json(searchdata_file, orient='records', lines=True)
    
    new = search[search['uid']%2 ==1]
    old = search[search['uid']%2 ==0]
    
    old_nosearch = len(old[old['search_count']==0])
    old_hassearch = len(old[old['search_count']>0])
    new_nosearch = len(new[new['search_count']==0])
    new_hassearch = len(new[new['search_count']>0])
    
   
    # Did more users use the search feature? (More precisely: did a different fraction of users have search count > 0?) 
    chi2_1,p1,dof1,expected1 = stats.chi2_contingency([[new_nosearch,new_hassearch],[ old_nosearch,old_hassearch]])
    # Did users search more often? (More precisely: is the number of searches per user different?) 
    mannwhiteneyu1 =2* stats.mannwhitneyu(old['search_count'],new['search_count']).pvalue

    #instructor only
    instructors = search[search['is_instructor'] == True]
    
    new = instructors[instructors['uid']%2 ==1]
    old = instructors[instructors['uid']%2 ==0]
    
    old_nosearch = len(old[old['search_count']==0])
    old_hassearch = len(old[old['search_count']>0])
    new_nosearch = len(new[new['search_count']==0])
    new_hassearch = len(new[new['search_count']>0])
    
    
    # Did more users use the search feature? (More precisely: did a different fraction of users have search count > 0?) 
    chi2_2,p2,dof2,expected2 = stats.chi2_contingency([[new_nosearch,new_hassearch],[old_nosearch,old_hassearch]])
    # Did users search more often? (More precisely: is the number of searches per user different?) 
    mannwhiteneyu2 =2* stats.mannwhitneyu(old['search_count'],new['search_count']).pvalue
    
    # Output
    print(OUTPUT_TEMPLATE.format(
        more_users_p=p1,
        more_searches_p=mannwhiteneyu1,
        more_instr_p=p2,
        more_instr_searches_p=mannwhiteneyu2,
    ))


if __name__ == '__main__':
    main()