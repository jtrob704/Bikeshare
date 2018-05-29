import time
import calendar
import pandas as pd
import numpy as np
from click._compat import raw_input

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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = raw_input("Please choose one of the following cities  (Chicago, New York City, or Washington): ").lower()

    # get user input for month (all, january, february, ... , june)
    month = raw_input("Please enter the month of the bikeshare data to view (January, February, March, April, May, June or all): ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = raw_input("Please enter the day of the week of the bikeshare data to view (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all): ").lower()

    print('-'*40)
    return city, month, day


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
    try:
        df = pd.read_csv(CITY_DATA[city])
    
        df['city'] = city
        # convert the Start Time column to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])

        # extract month and day of week from Start Time to create new columns
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

    except:
        print('\nInvalid data entered. Please enter data that matches given criteria\n')
        get_filters()


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # extract month from the Start Time column to create a month column and convert month in to month name
    df['month'] = df['Start Time'].dt.month.apply(lambda x: calendar.month_name[x])

    # find the most common month
    common_month = df['month'].mode()[0]     
    
    print('Most common month: ', common_month)
    
    # extract day from the Start Time column to create a day column
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # find the most common day of the week
    common_day = df['day_of_week'].mode()[0]

    # display the most common day of the week
    print('Most common day: ', common_day)

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most common hour
    common_hour = df['hour'].mode()[0]

    # display the most common start hour
    print('Most Common Start Hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # extract month from the Start Station column to create a station column
    df['start_station'] = df['Start Station'] 

    # find the most common Start Station
    common_start = df['start_station'].mode()[0]

    # display most commonly used start station
    print('Most common start station', common_start)

    # extract month from the End Station column to create a station column
    df['end_station'] = df['End Station']

    # find the most commonly used end station
    common_end = df['end_station'].mode()[0]

    # display most commonly used start station
    print('Most common end station', common_end)

    # display most frequent combination of start station and end station trip
    freq_comb = df.groupby(['start_station', 'end_station']).size().sort_values(ascending=False).head(1)

    print('The most frequent combination of start station and end station is: \n', freq_comb)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # extract duration from the Trip Duration column to create a trip_duration column
    df['trip_duration'] = df['Trip Duration']

    # display total travel time
    total_duration = df['trip_duration'].sum()
    print("The total trip duration is: ", total_duration)

    # display mean travel time
    avg_duration = df['trip_duration'].mean()
    print("The average trip duration is: ", avg_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nTotal number of users by type: \n', user_types)

    # Display counts of gender
    if df['city'].all() == 'washington':
        print('\nGender and birth year statistics are not avaiable for Washington')
        
    else:
        gender = df['Gender'].value_counts()
        print('\nTotal number of users by gender: \n', gender)   


        # Display earliest, most recent, and most common year of birth
        earliest_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        common_year = df['Birth Year'].value_counts().idxmax()

        print('\nThe earliest birth year of users is: ', int(earliest_year))
        print('\nThe most recent birth year of users is: ', int(recent_year))
        print('\nThe most common birth year of users is: ', int(common_year))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
