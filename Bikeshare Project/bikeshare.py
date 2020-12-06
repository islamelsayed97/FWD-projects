import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    #make the inial value of month & day is 'all'
    month, day, filter_type = 'all', 'all', None
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for Chicago, New York, or Washington?\n')
        if city.lower() in [ 'chicago', 'new york', 'washington']:
            break
        else:
            print('Oop. Wrong choice, please choose one from the choices carefully')

   # get user input for filter (month, day, both, or none)
    while True:
        filter_type = input('Would you like to filter the data by month, day, both, or not at all? type "none" for no time filters\n')
        if filter_type.lower() in ['month', 'day', 'both', 'none']:
            break
        else:
            print('Oop. Wrong choice, please choose one from the choices carefully')

    # get user input for month (january, february, ... , june) if the filter is month or both
    if filter_type.lower() == 'month' or filter_type.lower() == 'both':
        while True:
            month = input('Which month - January, February, March, April, May, or June?\n')
            if month.lower() in [ 'january', 'february', 'march', 'april', 'may', 'june']:
                break
            else:
                print('Oop. Wrong choice, please choose one from the choices carefully')

    # get user input for day of week (monday, tuesday, ... sunday) if the filter is day or both
    if filter_type.lower() == 'day' or filter_type.lower() == 'both':
        while True:
            day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n')
            if day.lower() in [ 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                break
            else:
                print('Oop. Wrong choice, please choose one from the choices carefully')

    print('-'*40)
    return city, month, day, filter_type


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

    # read the dataset of the city passed in the arguments
    df = pd.read_csv(CITY_DATA[city.lower()])
    
    # chicago & new york datasets have missing values, washington don't
    # filling missing values in chicago columns 'Birth year & Gender'
    if city.lower() == 'chicago':
        df['Birth Year'].fillna(method='ffill', inplace=True)
        df['Gender'].fillna(method='ffill', inplace=True)
        
    # filling missing values in new york columns 'User Type, Birth year & Gender'
    elif city.lower() == 'new york':
        df['User Type'].fillna(df['User Type'].mode()[0], inplace=True)
        df['Birth Year'].fillna(method='ffill', inplace=True)
        df['Gender'].fillna(method='ffill', inplace=True)
    else:
        pass
 

    # convert 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # create 'month' column
    df['month'] = df['Start Time'].dt.month

    # create 'day_of_week' column
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month
    if month != 'all':
        # convert the month name to the corresponding number
        months = [ 'january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1

        df = df[df['month'] == month]

    # filter by day
    if day != 'all':

        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, filter_type):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if filter_type != 'month' and filter_type != 'both':
        months = [ 'january', 'february', 'march', 'april', 'may', 'june']
        cmn_month = df['month'].mode()[0]
        cmn_month_name = months[cmn_month-1]
        print('The most common month is: {}, count: {}, filter: {}'.format(cmn_month_name, len(df[df['month'] == cmn_month]) ,filter_type))

    # display the most common day of week
    if filter_type != 'day' and filter_type != 'both':
        cmn_day = df['day_of_week'].mode()[0]
        print('The most common day of week is: {}, count: {}, filter: {}'.format(cmn_day, len(df[df['day_of_week'] == cmn_day]), filter_type))

    # create 'hour' column
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    cmn_hour = df['hour'].mode()[0]
    print('The most common hour is: {}, count: {}, filter: {}'.format(cmn_hour, len(df[df['hour'] == cmn_hour]), filter_type))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, filter_type):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    cmn_start_station = df['Start Station'].mode()[0]
    print('The most common Start Station is: "{}", count: {}'.format(cmn_start_station, len(df[df['Start Station'] == cmn_start_station])))

    # display most commonly used end station
    cmn_end_station = df['End Station'].mode()[0]
    print('The most common End Station is "{}", count: {}, filter: {}'.format(cmn_end_station, len(df[df['End Station'] == cmn_end_station]), filter_type))

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + ' to ' + df['End Station']
    cmn_trip = df['trip'].mode()[0]
    start_station = df[df['trip'] == cmn_trip]['Start Station'].unique()[0]
    end_station = df[df['trip'] == cmn_trip]['End Station'].unique()[0]
    print('The most common trip is start from "{}" and end in "{}", count: {}'.format(start_station, end_station, len(df[df['trip'] == cmn_trip])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, filter_type):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total travel time is: {}, count: {}'.format(df['Trip Duration'].sum(), len(df['Trip Duration'])))

    # display mean travel time
    print('The mean travel time is: {}, filter: {}'.format(df['Trip Duration'].mean(), filter_type))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city, filter_type):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The counts of user types is: ', end='')
    for key, value in dict(df['User Type'].value_counts()).items():
        print('{}: {}'.format(key, value), end=', ')
    print('filter: {}'.format(filter_type))

    # Display counts of gender
    if city.lower() != 'washington':
        print('The counts of gender is: ', end='')
        for key, value in dict(df['Gender'].value_counts()).items():
            print('{}: {}'.format(key, value), end=', ')
        print('filter: {}'.format(filter_type))

    # Display earliest, most recent, and most common year of birth
    if city.lower() != 'washington':
        print('The earliest year of birth is: {}'.format(df['Birth Year'].min()))
        print('The most recent year of birth is: {}'.format(df['Birth Year'].max()))
        print('The most common year of birth is: {}'.format(df['Birth Year'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def chunker(iterable, size):
    """Yield successive chunks from iterable of length size."""
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]
        
def individual_trip_data(df):
    df.drop(['month', 'hour', 'day_of_week', 'trip'], axis=1, inplace=True)
    df.rename({'Unnamed: 0':''}, axis=1, inplace=True)
    index = chunker(list(df.index), 10)
    for ind in index:
        for i in ind:
            for col in df.columns:
                print("'{}': {}".format(col, df.loc[i, col]))
            print('-'*40)
        view_more = input("Would you like to view more individual trip data? Type 'yes' or 'no'.\n")
        if view_more.lower() != 'yes':
            break

def main():
    while True:
        city, month, day, filter_type = get_filters()
        df = load_data(city, month, day)

        time_stats(df, filter_type)
        station_stats(df, filter_type)
        trip_duration_stats(df, filter_type)
        user_stats(df, city, filter_type)
        individual_trip_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
