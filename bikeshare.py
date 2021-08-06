import time
import datetime
import pandas as pd
import numpy as np
import calendar as cl

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
    print('Hello! Let\'s explore some US Bikeshare data!\n')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = CITY_DATA.keys()
    print("Select from this list of Bikeshare cities:\n")
    while True:
        for city_key, value in CITY_DATA.items():
            print("> {}".format(city_key).title())    
        city = input("\nEnter a city:  ")
        if city.lower() in cities:
            break
        

    # TO DO: get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'june']
    while True:
        month = input("\nEnter a month from January to June, or enter 'all':  ").lower()
        if month == 'all' or month in months:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input("\nEnter a day of the week, or enter 'all':  ").lower()
        if day == 'all' or day in weekdays:
            break

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    #print(df)

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
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # TO DO: display the most common month
    df['month'] = df['Start Time'].dt.month
    most_common_month_number = df['month'].value_counts().idxmax()
    print("Most common month: {}".format(cl.month_name[most_common_month_number]))

    # TO DO: display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    most_common_day = df['day_of_week'].value_counts().idxmax()
    print("Most common day of the week: {}".format(most_common_day))

    # TO DO: display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['start_hour'].value_counts().idxmax()
    print("Most common start hour: {}".format(datetime.time(most_common_start_hour).strftime("%I:00 %p")))

    print("\nCompleted in %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts().idxmax()
    print("Most common start station: {}".format(most_common_start_station))
    
    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].value_counts().idxmax()
    print("Most common end station: {}".format(most_common_end_station))    

    # TO DO: display most frequent combination of start station and end station trip
    df['Start End'] = df['Start Station'] + '  ===>  ' + df['End Station']
    most_common_start_end_station = df['Start End'].value_counts().idxmax()
    print("Most common stations to start and end a trip: {}".format(most_common_start_end_station))  

    print("\nCompleted in %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    travel_time_total_seconds = int(df['Trip Duration'].sum())
    travel_time_total = datetime.timedelta(seconds = travel_time_total_seconds)
    print("The total travel time is {} hours, minutes and seconds.".format(travel_time_total))

    # TO DO: display mean travel time
    travel_time_mean = df['Trip Duration'].mean() // 60
    print("The mean travel time is {} minutes.".format(travel_time_mean))

    print("\nCompleted in %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type_count = df.groupby(['User Type'])['User Type'].count()
    print("\nThe count by {}\n".format(user_type_count))
    
    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df.groupby(['Gender'])['Gender'].count()
        print("\nThe count by {}\n".format(gender_count))

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        year_of_birth_earliest = df['Birth Year'].min()
        year_of_birth_latest = df['Birth Year'].max()
        year_of_birth_common = df['Birth Year'].value_counts().idxmax()
        print("\nThe oldest rider was born in {}.".format(int(year_of_birth_earliest)))
        print("\nThe youngest rider was born in {}.".format(int(year_of_birth_latest)))
        print("\n{} is the most common birth year.\n".format(int(year_of_birth_common)))

    print("\nCompleted in %s seconds." % (time.time() - start_time))
    print('-'*40)

   
def view_data_file(df):
    """View the raw data file 5 rows as a time."""
    
    print('\nViewing Raw Data...\n')
        
    i = 0
    pd.set_option('display.max_columns', 50)
    view_data = 'yes'
    while view_data == 'yes':         
        print(df[i:i+5])
        view_data = input('\nWould you like to see the next 5 rows? Enter yes or no.\n').lower()
        i += 5 
        
    print('-'*40)      
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        view_raw_data = input('\nWould you like to view the raw data?  Enter yes or no.\n')
        if view_raw_data.lower() == 'yes':
            view_data_file(df)
            
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
            print("Thank you for your interest in Bikeshare!")



if __name__ == "__main__":
	main()
