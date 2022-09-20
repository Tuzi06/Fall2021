import sys
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from datetime import date

def process(input):
    counts = pd.read_json(input, lines=True)
    weekdays = counts[counts['date'].apply(date.weekday)<5]
    weekends = counts[counts['date'].apply(date.weekday)>=5]
    weekdays = weekdays[(weekdays['date'].dt.year == 2012) | (weekdays['date'].dt.year == 2013)]
    weekends  = weekends[(weekends ['date'].dt.year == 2012) | (weekends ['date'].dt.year == 2013)]
    weekdays = weekdays[weekdays['subreddit'] == 'canada'].reset_index(drop=True)
    weekends = weekends[weekends['subreddit'] == 'canada'].reset_index(drop=True)

    num_weekdays = len(weekdays) 
    num_weekends = len(weekends)
   
    return weekdays, weekends

def student_ttest(weekdays, weekends):
    ttest_p = stats.ttest_ind(weekdays['comment_count'],weekends['comment_count']).pvalue
    weekdays_p = stats.normaltest(weekdays['comment_count']).pvalue
    weekends_p = stats.normaltest(weekends['comment_count']).pvalue
    levene_p = stats.levene(weekdays['comment_count'],weekends['comment_count']).pvalue
    
    # plt.hist(weekends['comment_count'])
    # plt.figure()
    # plt.hist(weekdays['comment_count'])
    # plt.show()
    
    return ttest_p,weekdays_p,weekends_p,levene_p


def fix1(weekdays,weekends):
    trans_weekdays = np.sqrt(weekdays['comment_count'])
    trans_weekends = np.sqrt(weekends['comment_count'])
    trans_weekdays_p = stats.normaltest(trans_weekdays).pvalue
    trans_weekends_p = stats.normaltest(trans_weekends).pvalue
    trans_levene_p = stats.levene(trans_weekdays,trans_weekends).pvalue
    
    # plt.hist(trans_weekdays)
    # plt.figure()
    # plt.hist(trans_weekends)
    # plt.show()
    
    return trans_weekdays_p, trans_weekends_p,trans_levene_p

def fix2(weekdays,weekends):
    week1 = weekdays['date'].apply(date.isocalendar).apply(pd.Series)
    week1 = week1[[0,1]]
    week1.columns=['year','week number']
    
    week2 = weekends['date'].apply(date.isocalendar).apply(pd.Series)
    week2 = week2[[0,1]]
    week2.columns=['year','week number']
    
    weekly_weekdays =  pd.concat([weekdays, week1],axis =1).groupby(['year','week number']).mean()
    weekly_weekends =  pd.concat([weekends, week2],axis =1).groupby(['year','week number']).mean()
    
    weekly_weekdays_p = stats.normaltest(weekly_weekdays['comment_count']).pvalue
    weekly_weekends_p = stats.normaltest(weekly_weekends['comment_count']).pvalue
    weekly_levene_p = stats.levene(weekly_weekdays['comment_count'],weekly_weekends['comment_count']).pvalue
    weekly_ttest_p = stats.ttest_ind(weekly_weekdays['comment_count'],weekly_weekends['comment_count']).pvalue
    
    return weekly_ttest_p, weekly_weekdays_p,weekly_weekends_p, weekly_levene_p
    
def fix3 (weekdays,weekends):
    return 2 * stats.mannwhitneyu(weekdays['comment_count'],weekends['comment_count']).pvalue
        
    
OUTPUT_TEMPLATE = (
    "Initial T-test p-value: {initial_ttest_p:.3g}\n"
    "Original data normality p-values: {initial_weekday_normality_p:.3g} {initial_weekend_normality_p:.3g}\n"
    "Original data equal-variance p-value: {initial_levene_p:.3g}\n"
    "Transformed data normality p-values: {transformed_weekday_normality_p:.3g} {transformed_weekend_normality_p:.3g}\n"
    "Transformed data equal-variance p-value: {transformed_levene_p:.3g}\n"
    "Weekly data normality p-values: {weekly_weekday_normality_p:.3g} {weekly_weekend_normality_p:.3g}\n"
    "Weekly data equal-variance p-value: {weekly_levene_p:.3g}\n"
    "Weekly T-test p-value: {weekly_ttest_p:.3g}\n"
    "Mann-Whitney U-test p-value: {utest_p:.3g}"
)

def main():
    reddit_counts = sys.argv[1]
    # ...
    weekdays,weekends = process(reddit_counts)
    ttest_p,weekdays_p,weekends_p,levene_p = student_ttest(weekdays,weekends)
    trans_weekdays_p, trans_weekends_p,trans_levene_p = fix1(weekdays,weekends)
    weekly_ttest_p, weekly_weekdays_p,weekly_weekends_p, weekly_levene_p = fix2(weekdays,weekends)
    utest_p = fix3(weekdays,weekends)
    
    print(OUTPUT_TEMPLATE.format(
        initial_ttest_p=ttest_p,
        initial_weekday_normality_p=weekdays_p,
        initial_weekend_normality_p=weekends_p,
        initial_levene_p=levene_p,
        transformed_weekday_normality_p=trans_weekdays_p,
        transformed_weekend_normality_p=trans_weekends_p,
        transformed_levene_p=trans_levene_p,
        weekly_weekday_normality_p= weekly_weekdays_p,
        weekly_weekend_normality_p=weekly_weekends_p,
        weekly_levene_p=weekly_levene_p,
        weekly_ttest_p=weekly_ttest_p,
        utest_p=utest_p,
    ))


if __name__ == '__main__':
    main()
