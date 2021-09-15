import sys
import numpy as np
import pandas as pd
import scipy.stats as stats


OUTPUT_TEMPLATE = (
    '"Did more/less users use the search feature?" p-value:  {more_users_p:.3g}\n'
    '"Did users search more/less?" p-value:  {more_searches_p:.3g} \n'
    '"Did more/less instructors use the search feature?" p-value:  {more_instr_p:.3g}\n'
    '"Did instructors search more/less?" p-value:  {more_instr_searches_p:.3g}'
)


def main():
    searchdata_file = sys.argv[1]
    #searchdata_file="searches.json"
    searchdata=pd.read_json(searchdata_file, orient='records', lines=True)
    
    #oddid is new
    new = searchdata[searchdata['uid']%2 == 1] 
    original = searchdata[searchdata['uid']%2 == 0] 
    
    
    # Did more users use the search feature? (More precisely: did a different fraction of users have search count > 0?)
    new_search=len(new[new['search_count']>0])
    new_zero=len(new[new['search_count']==0])
    original_search=len(original[original['search_count']>0])
    original_zero=len(original[original['search_count']==0])

    # Did users search more often? (More precisely: is the number of searches per user different?) 
    #chi-square
    contingency = [[new_search,new_zero],[original_search,original_zero]]
    chi1, p1, dof1, expected1 = stats.chi2_contingency(contingency)

    mannwhit_p1 =stats.mannwhitneyu(new['search_count'],original['search_count']).pvalue
    #we don't find any effect

    
    #all instructors 
    new_instructor = new[new['is_instructor'] == True]
    original_instructor = original[original['is_instructor'] == True]
    
    # Did more users use the search feature? (More precisely: did a different fraction of users have search count > 0?)
    new_search_instructor=len(new_instructor[new_instructor['search_count']>0])
    new_zero_instructor=len(new_instructor[new_instructor['search_count']==0])
    original_search_instructor=len(original_instructor[original_instructor['search_count']>0])
    original_zero_instructor=len(original_instructor[original_instructor['search_count']==0])

    # Did users search more often? (More precisely: is the number of searches per user different?) 
    #chi-square
    contingency = [[new_search_instructor,new_zero_instructor],[original_search_instructor,original_zero_instructor]]
    chi2, p2, dof2, expected2 = stats.chi2_contingency(contingency)
    mannwhit_p2 =stats.mannwhitneyu(new_instructor['search_count'],original_instructor['search_count']).pvalue


    print(OUTPUT_TEMPLATE.format(
        more_users_p=p1,
        more_searches_p=mannwhit_p1,
        more_instr_p=p2,
        more_instr_searches_p=mannwhit_p2,
    ))

if __name__ == '__main__':
    main()