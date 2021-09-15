import pandas as pd
import sys
import gzip
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import datetime 

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
    reddit = gzip.open(reddit_counts, 'rt', encoding = 'utf-8')
    reddit="reddit-counts.json.gz"
    counts = pd.read_json(reddit, lines=True)
    # counts = counts[counts['date'] >= datetime.datetime(2012,1,1)]
    # counts = counts[counts['date'] <= datetime.datetime(2013,12,31)]
    # counts = counts[counts['subreddit'] == 'canada'].reset_index(drop=True)
    # counts
    counts = counts[((counts['date'].dt.year == 2012) | (counts['date'].dt.year == 2013))]
    counts= counts[(counts['subreddit'] =='canada')].reset_index(drop=True)
    
    weekend=counts[counts['date'].map(lambda x: datetime.date.isoweekday(x)==6)|counts['date'].map(lambda x: datetime.date.isoweekday(x)==7)].reset_index(drop=True)
    weekday=counts[counts['date'].map(lambda x: datetime.date.isoweekday(x)!=6)&counts['date'].map(lambda x: datetime.date.isoweekday(x)!=7)].reset_index(drop=True)

    #t-test
    ttest=stats.ttest_ind(weekend['comment_count'], weekday['comment_count'])
    weekend_p=stats.normaltest(weekend['comment_count']).pvalue
    weekday_p=stats.normaltest(weekday['comment_count']).pvalue
    levene_p=stats.levene(weekend['comment_count'], weekday['comment_count']).pvalue
    #weekday is normally, weekend is not.
    
    plt.hist(weekend['comment_count'])
    plt.figure()
    plt.hist(weekday['comment_count'])
    #Fix 1 because is right skew, choose np.log, np.sqrt
    # ya_transf = np.log(weekend['comment_count'])
    # yb_transf = np.log(weekday['comment_count'])
    # print(stats.normaltest(ya_transf).pvalue)
    # print(stats.normaltest(yb_transf).pvalue)
    # plt.hist(ya_transf)
    # plt.figure()
    # plt.hist(yb_transf)
    ya_transf = np.sqrt(weekend['comment_count'])
    yb_transf = np.sqrt(weekday['comment_count'])
    weekend_trans_p=stats.normaltest(ya_transf).pvalue
    weekday_trans_p=stats.normaltest(yb_transf).pvalue
    trans_levene_p=stats.levene(ya_transf, yb_transf).pvalue
    plt.hist(ya_transf)
    plt.figure()
    plt.hist(yb_transf)
    #Fix 2
    date1 = weekday['date'].apply(datetime.date.isocalendar).apply(pd.Series)
    date1 = date1[[0, 1]] 
    date1.columns=['Year', 'Week'] 
    weekday = pd.concat([weekday, date1], axis=1)
    weekday_grouped = weekday.groupby(['Year', 'Week']).aggregate('mean')

    date2 = weekend['date'].apply(datetime.date.isocalendar).apply(pd.Series)
    date2 = date2[[0, 1]] 
    date2.columns=['Year', 'Week'] 
    weekend = pd.concat([weekend, date2], axis=1)
    weekend_grouped = weekend.groupby(['Year', 'Week']).aggregate('mean')

    weekend_grouped_p=stats.normaltest(weekend_grouped['comment_count']).pvalue
    weekday_grouped_p=stats.normaltest(weekday_grouped['comment_count']).pvalue
    levene_grouped_p=stats.levene(weekend_grouped['comment_count'], weekday_grouped['comment_count']).pvalue
    grouped_ttest_p=stats.ttest_ind(weekend_grouped['comment_count'], weekday_grouped['comment_count'])

    #Fix 3
    u_test = 2*stats.mannwhitneyu(weekday['comment_count'], weekend['comment_count']).pvalue

    print(OUTPUT_TEMPLATE.format(
        initial_ttest_p=ttest.pvalue,
        initial_weekday_normality_p=weekday_p,
        initial_weekend_normality_p=weekend_p,
        initial_levene_p=levene_p,

        transformed_weekday_normality_p=weekday_trans_p,
        transformed_weekend_normality_p=weekend_trans_p,
        transformed_levene_p=trans_levene_p,

        weekly_weekday_normality_p=weekday_grouped_p,
        weekly_weekend_normality_p=weekend_grouped_p,
        weekly_levene_p=levene_grouped_p,
        weekly_ttest_p=grouped_ttest_p.pvalue,
        utest_p=u_test,
    ))


    

    print(OUTPUT_TEMPLATE.format(
        initial_ttest_p=0,
        initial_weekday_normality_p=0,
        initial_weekend_normality_p=0,
        initial_levene_p=0,
        transformed_weekday_normality_p=0,
        transformed_weekend_normality_p=0,
        transformed_levene_p=0,
        weekly_weekday_normality_p=0,
        weekly_weekend_normality_p=0,
        weekly_levene_p=0,
        weekly_ttest_p=0,
        utest_p=0,
    ))


if __name__ == '__main__':
    main()