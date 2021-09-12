import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = ['chicago', 'washington', 'new york city']

months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

day_of_week = ['all','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

#Asks the user for input and filters by day, month or over all months
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

# get user input for city (chicago, new york city, washington)
    while True:

        city = input('\nWhat city would you like to explore? ').lower()

        if city in cities:
            print('You have chosen {}'.format(city.title()))
            break
        else:
            print('Please enter a valid city response')

    # get user input for month (all, january, february, ... , june)
    while True:

        month = input('\nWhat month would you like to explore? ').lower()

        if month in months:
            print('You have chosen {}'.format(month.title()))
            break
        else:
            print('Please enter a valid month response')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:

        day = input('\nWhat day would you like to explore? ').lower()

        if day in day_of_week:
            print('You have chosen {}'.format(day.title()))
            break
        else:
            print('Please enter a valid day response')

    print('-'*40)
    return city, month, day

# Generate the DataFrame
def load_data(city, month, day):

    # city yields dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert Start Time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # call the month and day
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create new DF
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print("Most common month is ", common_month)

    # display the most common day of week
    common_day = df['day'].mode()[0]
    print("Most common day of the week is ", common_day)

    # display the most common start hour
    common_hour = df['Start Time'].dt.hour.mode()[0]
    print("Most common start hour is ", common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    Common_start = df['Start Station'].sort_values().mode()[0]
    print('Most common start station is', Common_start)

    # display most commonly used end station
    print('Most common end station is', df['End Station'].sort_values().mode()[0])

    # display most frequent combination of start station and end station trip
    df['Common_station'] = df['Start Station'] + ' to ' + df['End Station']

    print('Most frequent combination station is', df['Common_station'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""


    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    Time = df['Trip Duration'].sum()
    day1 = Time//86400
    hour1 = Time//3600
    minute = Time//60
    print('Total travel time in seconds is', Time)
    print('\nTotal travel time in days = {} in hours = {} and in minutes = {}\n'.format(day1, hour1, minute))

    # display mean travel time
    print('Mean travel time is ', df['Trip Duration'].mean())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    cities_extra = ['new york city', 'chicago']
    if city in cities_extra:
        print('\nNumber of User Types are: \n', df.groupby(['User Type'])['Gender'].count())

    # Display counts of gender
    cities_extra = ['new york city', 'chicago']
    if city in cities_extra:
        print('\nNumber of gender types are: \n', df.groupby(['Gender'])['Gender'].count())

    # Display earliest, most recent, and most common year of birth
    if city in cities_extra:
        print('Earliest birth year is', df['Birth Year'].min())
        print('Most recent birth year is', df['Birth Year'].max())
        print('Most common birth year is', df['Birth Year'].mode()[0])

    print("This took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    pd.set_option('max_rows',400)
    df = df.reset_index(drop = False)
    row_index = 0
    while True:

        raw_data = str(input("Would you like to see the first 5 lines of the raw data?"))
        if raw_data.lower() != 'yes':
            break
        else:
            print(df[row_index: row_index + 5])
            row_index += 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
