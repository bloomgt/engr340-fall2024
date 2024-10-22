import sys
import pandas as pd
import numpy as np



def parse_nyt_data(file_path=''):
    """
    Parse the NYT covid database and return a list of tuples. Each tuple describes one entry in the source data set.
    Date: the day on which the record was taken in YYYY-MM-DD format
    County: the county name within the State
    State: the US state for the entry
    Cases: the cumulative number of COVID-19 cases reported in that locality
    Deaths: the cumulative number of COVID-19 death in the locality

    :param file_path: Path to data file
    :return: A List of tuples containing (date, county, state, cases, deaths) information
    """
    # data point list
    data=[]

    # open the NYT file path
    try:
        fin = open(file_path)
    except FileNotFoundError:
        print('File ', file_path, ' not found. Exiting!')
        sys.exit(-1)

    # get rid of the headers
    fin.readline()

    # while not done parsing file
    done = False

    # loop and read file
    while not done:
        line = fin.readline()

        if line == '':
            done = True
            continue

        # format is date,county,state,fips,cases,deaths
        (date, county, state, fips, cases, deaths) = line.rstrip().split(",")

        # clean up the data to remove empty entries
        if cases=='':
            cases=0
        if deaths=='':
            deaths=0

        # convert elements into ints
        try:
            entry = (date,county,state, int(cases), int(deaths))
        except ValueError:
            print('Invalid parse of ', entry)

        # place entries as tuple into list
        data.append(entry)


    return data

def first_question(data):
    """
    # Write code to address the following question: Use print() to display your responses.
    # When was the first positive COVID case in Rockingham County?
    # When was the first positive COVID case in Harrisonburg?
    :return:
    """
    # your code here

    # Use pandas to extract data from passed arguments
    df = pd.DataFrame(data, columns = ['date','county','state','cases','deaths'])


    # Filter dataframe for Rockingham county, VA
    rockingham_data = df[(df['state'] == 'Virginia') & (df['county'] == 'Rockingham')]
    # Convert dataframe to numpy array
    rockingham_array = rockingham_data['date'].to_numpy()
    # Identify first case as first item of arrray
    first_rockingham_case = rockingham_array[0]
    # Print Results
    print()
    print('The first case in Rockingham county occured on: ', first_rockingham_case)


    # Repeat previous process for Harrisonburg City
    harrisonburg_data = df[(df['state'] == 'Virginia') & (df['county'] == 'Harrisonburg city')]
    harrisonburg_array = harrisonburg_data['date'].to_numpy()
    first_harrisonburg_case = harrisonburg_array[0]
    print('The first case in Harrisonburg city occured on: ', first_harrisonburg_case)

    return

def second_question(data):
    """
    # Write code to address the following question: Use print() to display your responses.
    # What day was the greatest number of new daily cases recorded in Harrisonburg?
    # What day was the greatest number of new daily cases recorded in Rockingham County?
    :return:
    """
    # your code here
    # Use pandas to extract data from passed arguments
    df = pd.DataFrame(data, columns = ['date','county','state','cases','deaths'])
    #isolate rockingham date and case data
    rockingham_data = df[(df['state'] == 'Virginia') & (df['county'] == 'Rockingham')]
    rockingham_date_array = rockingham_data['date'].to_numpy()
    rockingham_case_array = rockingham_data['cases'].to_numpy()
    #establish diff calculation and index variables
    rockingham_case_diffs = []
    rockingham_max_diffs = 0
    r_max = 0
    #construct array of diff values and identify maximum
    for i in range(1,len(rockingham_case_array)):
        diff = rockingham_case_array[i] - rockingham_case_array[i-1]

        if diff > r_max:
            r_max = diff
            r_index = i

        else:
            continue
    #use max case index to identify date
    rockingham_max_date = rockingham_date_array[r_index]

    print()
    print('The date with the highest increase of cases in Rockingham county occured on:', rockingham_max_date)

    #Repeat process above for harrisonburg data
    harrisonburg_data = df[(df['state'] == 'Virginia') & (df['county'] == 'Harrisonburg city')]
    harrisonburg_date_array = harrisonburg_data['date'].to_numpy()
    harrisonburg_case_array = harrisonburg_data['cases'].to_numpy()

    harrisonburg_case_diffs = list()
    harrisonburg_max_diffs = 0
    h_max = 0

    for i in range(1, len(harrisonburg_case_array)):
        diff = harrisonburg_case_array[i] - harrisonburg_case_array[i - 1]
        if diff > h_max:
            h_max = diff
            h_index = i
        else:
            continue

    harrisonburg_max_date = harrisonburg_date_array[h_index]
    print('The date with the highest increase of cases in Harrisonburg City occured on:', harrisonburg_max_date)

    return rockingham_case_diffs

def third_question(data):
    # Write code to address the following question:Use print() to display your responses.
    # What was the worst 7-day period in either the city and county for new COVID cases?
    # This is the 7-day period where the number of new cases was maximal.

    # your code here
    # Use pandas to extract data from passed arguments
    df = pd.DataFrame(data, columns = ['date','county','state','cases','deaths'])
    #isolate rockingham date and case data
    rockingham_data = df[(df['state'] == 'Virginia') & (df['county'] == 'Rockingham')]
    rockingham_date_array = rockingham_data['date'].to_numpy()
    rockingham_case_array = rockingham_data['cases'].to_numpy()
    #establish diff calculation and index variables
    rockingham_case_diffs = []
    rockingham_max_diffs = 0
    r_max = 0
    #construct array of diff values and identify maximum
    for i in range(1,len(rockingham_case_array)):
        diff = rockingham_case_array[i] - rockingham_case_array[i-1]
        rockingham_case_diffs.append(diff)
        if diff > r_max:
            r_max = diff
        else:
            continue



    seven_day_case_count = list()
    worst_week_index = ()

    for i in range(0,len(rockingham_case_diffs)):

        window = 7
        addsum = 0


        if i < window:
            addsum += rockingham_case_diffs[i]
            seven_day_case_count.append(addsum)
        else:
            addsum += rockingham_case_diffs[i] - rockingham_case_diffs[i-window]
            if addsum > max(seven_day_case_count):
                worst_week_index = i
                seven_day_case_count.append(addsum)
            else:
                seven_day_case_count.append(addsum)


    week_beginning = rockingham_date_array[worst_week_index - window]
    week_ending = rockingham_date_array[worst_week_index]

    print()
    print('The week that experienced the greatest rise in cases within Rockingham county was from', week_beginning, "to", week_ending)

    return

if __name__ == "__main__":
    data = parse_nyt_data('us-counties.csv')

    #for (date, county, state, cases, deaths) in data:
        #print('On ', date, ' in ', county, ' ', state, ' there were ', cases, ' cases and ', deaths, ' deaths')

    # write code to address the following question: Use print() to display your responses.
    # When was the first positive COVID case in Rockingham County?
    # When was the first positive COVID case in Harrisonburg?
    first_question(data)

    # write code to address the following question: Use print() to display your responses.
    # What day was the greatest number of new daily cases recorded in Harrisonburg?
    # What day was the greatest number of new daily cases recorded in Rockingham County?
    second_question(data)

    # write code to address the following question:Use print() to display your responses.
    # What was the worst seven day period in either the city and county for new COVID cases?
    # This is the 7-day period where the number of new cases was maximal.
    third_question(data)


