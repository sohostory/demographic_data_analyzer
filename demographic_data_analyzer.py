import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df['race'].value_counts()

    # What is the average age of men?
    average_age_men = round(df.loc[df['sex'] == 'Male', 'age'].mean(), 1)

    # What is the percentage of people who have a Bachelor's degree?
    # education = pd.Series(df['education'].value_counts())
    # percentage_bachelors = (education['Bachelors'] / education.sum() * 100).round(1)
    percentage_bachelors = round((df['education'].value_counts(normalize=True)['Bachelors'] * 100), 1)


    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_salary = df[df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])].groupby(['salary'])['salary'].count()

    higher_education = higher_salary.sum()

    lower_salary = df[~df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])].groupby(['salary'])['salary'].count()
    lower_education = lower_salary.sum()

    # percentage with salary >50K
    higher_education_rich = (higher_salary['>50K'] / higher_education * 100).round(1)
    lower_education_rich = (lower_salary['>50K'] / lower_education * 100).round(1)

    # advanced_edu = ['Bachelors', 'Masters', 'Doctorate']
    # higher_education_rich = round((df[(df['education'].isin(advanced_edu)) & (df['salary'] == '>50K')].shape[0] /
    #                                df[df['education'].isin(advanced_edu)].shape[0]) * 100, 1)
    # lower_education_rich = round((df[~df['education'].isin(advanced_edu) & (df['salary'] == '>50K')].shape[0] /
    #                               df[~df['education'].isin(advanced_edu)].shape[0]) * 100, 1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    min_work = df[df['hours-per-week'] == min_work_hours].groupby(['salary'])['salary'].count()
    num_min_workers = min_work['>50K']

    rich_percentage = num_min_workers / min_work.sum() * 100
    # rich_percentage = round((df[(df['hours-per-week'] == min_work_hours) & (df['salary'] == '>50K')].shape[0] /
    #                          df[df['hours-per-week'] == min_work_hours].shape[0]) * 100, 1)

    # What country has the highest percentage of people that earn >50K?
    countries = pd.DataFrame(df.groupby(['native-country'])['salary'].count())
    countries[">50K"] = pd.Series(df[df['salary'] == '>50K'].groupby(['native-country'])['salary'].count())
    countries["<=50K"] = pd.Series(df[df['salary'] == '<=50K'].groupby(['native-country'])['salary'].count())
    countries['percentage'] = countries['>50K'] / countries['salary']

    max_percentage = countries['percentage'].max()

    highest_earning_country = countries[countries['percentage'] == max_percentage].index[0]
    highest_earning_country_percentage = (max_percentage * 100).round(1)

    # country_salary = df.groupby('native-country')['salary'].value_counts(normalize=True).unstack()
    # country_salary['>50K'] = country_salary['>50K'].fillna(0)
    # highest_earning_country = country_salary['>50K'].idxmax()
    # highest_earning_country_percentage = round(country_salary['>50K'].max() * 100, 1)

    # Identify the most popular occupation for those who earn >50K in India.
    india = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')].groupby(['occupation']).count()

    top_IN_occupation = india[india['salary'] == india['salary'].max()].index[0]

    # top_IN_occupation = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')][
    #     'occupation'].value_counts().idxmax()

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count)
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
