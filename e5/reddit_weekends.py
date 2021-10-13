import sys
import pandas as pd
from scipy import stats

counts = pd.read_json(sys.argv[1], lines=True)
weekdays = counts[counts['date'].dt.dayofweek<5]
weekends = counts[counts['date'].dt.dayofweek>=5]

weekdays = weekdays[(weekdays['date'].dt.year == 2012) | (weekdays['date'].dt.year == 2013)]
weekends  = weekends[(weekends ['date'].dt.year == 2012) | (weekends ['date'].dt.year == 2013)]

weekdays = weekdays[weekdays['subreddit'] == 'canada'].reset_index(drop=True)
weekends = weekends[weekends['subreddit'] == 'canada'].reset_index(drop=True)


num_weekdays = len(weekdays) 
num_weekends = len(weekends)






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
