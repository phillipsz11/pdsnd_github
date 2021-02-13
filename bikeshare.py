import time
import pandas as pd
import numpy as np
from datetime import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    city = ""
    month = ""
    day = ""

    month_list = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    day_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

    while (city.lower() not in CITY_DATA.keys()):
        city = input("Enter a valid city you would like to analyze (Chicago, New York City, or Washington): ")

    while(month.lower() not in month_list):
        month = input("Enter a valid month to filter by (January, February, March, April, May, or June), or type all: ")

    while(day.lower() not in day_list):
        day = input("Enter a valid day to filter by (Monday-Sunday), or type all: ")

    print('-'*40)
    return city.lower(), month.lower(), day.lower()


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print("The most common month is: {}".format(df['month'].mode()[0]))

    print("The most common day of week is: {}".format(df['day_of_week'].mode()[0]))

    df['hour'] = df['Start Time'].dt.hour
    print("The most common start hour is: {}".format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print("The most commonly used Start Station is: {} \n".format(mode_of_column(df['Start Station'])))

    print("The most commonly used End Station is: {} \n".format(mode_of_column(df['End Station'])))


    df['combination'] = df['Start Station'] + " / " + df['End Station']
    print('The most common combination of start station and end station trip is: {}'.format((df['combination'].mode()[0])))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print("Total travel time: {} days\n".format(total_trip_duration(df['Trip Duration'])))

    print("Average travel time: {} minutes\n".format(average_trip_duration(df['Trip Duration'])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    try:
        print("Counts of User Types: \n-----------------------\n{} \n".format(df_value_counts(df['User Type'])))

        print("Counts by Gender: \n-----------------------\n{} \n".format(df_value_counts(df['Gender'])))

        print("Earliest Birth Year: {}".format(int(df['Birth Year'].min())))
        print("Oldest Member Age (if still alive...): {}\n".format(oldest_age(df['Birth Year'])))

        print("Most Recent Birth Year: {}".format(int(df['Birth Year'].max())))
        print("Youngest Member Age: {}\n".format(youngest_age(df['Birth Year'])))

        print("Most Common Birth Year: {}\n".format(int(df['Birth Year'].mode()[0])))


        print("\nThis took %s seconds." % (time.time() - start_time))
    except KeyError:
        print("Some or all user stats are not available in this city.")
    print('-'*40)

def total_trip_duration(trip_duration):
    """Used to calculate the total trip duration"""
    total_time = trip_duration.sum() / 60 / 60 / 24
    return round(total_time,2)

def average_trip_duration(trip_duration):
    """Used to calculate the average trip duration"""
    average_time = trip_duration.mean() / 60
    return round(average_time,2)

def oldest_age(birth_year):
    """Just an extra method to calculate age of oldest user"""
    return int(datetime.now().year - birth_year.min())

def youngest_age(birth_year):
    """Just an extra method to calculate age of the youngest user"""
    return int(datetime.now().year - birth_year.max())

def df_value_counts(df_column):
    return df_column.value_counts()

def mode_of_column(df_column):
    return df_column.mode()[0];

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        i = 0
        while True:
            raw=input('\nWould you like to see 5 rows of raw data? Enter yes or no.\n').lower()
            i=i+5
            if raw=='yes':
                print(df[i:i+5])
                continue
            if raw=='no':
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
