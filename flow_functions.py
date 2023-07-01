# This will be the backend python server

from task import Task
from linguist import Linguist
from workload import Workload
from datetime import datetime, timedelta, time
import pandas as pd
import numpy as np
import os

# Get the team from javascript cookie
cookie_team = "fashion"


def get_team_name(team=None):
    """
    This function simply returns the team name in lower cases.
    The team folder is selected by checking the cookie_team variable.
    """
    if team is None:
        team = cookie_team
    
    with open(f'task-allocation-planner/database/{team}/team_name.txt', 'r') as file:
        team_name = file.read()
    return team_name.lower()


##########
# Linguist functions
##########

def create_linguist(username, name, locale, team=None, contract_hours=8.0, output=2400):
    if team is None:
        team = cookie_team
    
    linguist = Linguist(username, name, locale, team, contract_hours, output)
    return linguist


def add_to_linguist_db(linguist, team=None):
    if team is None:
        team = cookie_team

    # determine the file location
    file_loc = f"task-allocation-planner/database/{team}/{team}_linguists.pkl"

    # First convert the linguist data into a DataFrame
    data = vars(linguist)
    df = pd.DataFrame([data])

    # Check if there is already an existing database
    if os.path.exists(file_loc):
        existing_df = pd.read_pickle(file_loc)

        # Add the whole row of the new linguist DataFrame into the the last row of the existing database
        existing_df.loc[len(existing_df)] = df.iloc[0, :]

        # Save the database
        existing_df.to_pickle(file_loc)

    else: # this is the first linguist, save the database
        df.to_pickle(file_loc)


def create_workload_db(linguist, team=None):
    if team is None:
        team = cookie_team
    
    # determine the file location
    file_loc = f"task-allocation-planner/database/{team}/{linguist.username}_workload.pkl"

    # create the workload class
    linguist_workload = Workload(linguist.username, linguist.contract_hours)

    # create the DataFrame
    data = vars(linguist_workload)
    df = pd.DataFrame([data])
    df.to_pickle(file_loc)


def remove_from_linguist_db(username, team=None):
    if team is None:
        team = cookie_team

    # determine the file location
    file_loc = f"task-allocation-planner/database/{team}/{team}_linguists.pkl"

    # First read the file containing all linguists of the team
    all_linguists = pd.read_pickle(file_loc)

    # Identify the row index of the linguist
    user_index = all_linguists[all_linguists['username'] == username].index

    # Remove the row, hence removing the linguist
    all_linguists.drop(user_index, inplace=True)

    # Save the database
    all_linguists.to_pickle(file_loc)

    return None



def get_attribute(username, attribute, team=None):
    if team is None:
        team = cookie_team

    # determine the file location
    file_loc = f"task-allocation-planner/database/{team}/{team}_linguists.pkl"

    # First read the file containing all linguists of the team
    all_linguists = pd.read_pickle(file_loc)

    # Find the value of the desired attribute
    value = all_linguists.loc[all_linguists["username"] == username, attribute]

    return value.values[0] if len(value) > 0 else None


def set_attribute(username, attribute, new_value, team=None):
    """
    This function is used to set/update basic attributes of a linguist

    Applicable attributes:

    username => str
    name => str
    locale => str
    contract_hours => float
    output => int
    start_time => time e.g. (9,0,0)
    end_time => time e.g. (17,30,0)
    translation => bool
    review => bool
    lso => bool
    client_meeting => bool
    test_translation => bool
    """
    if team is None:
        team = cookie_team
    
    # determine the file location
    file_loc = f"task-allocation-planner/database/{team}/{team}_linguists.pkl"

    # First read the file containing all linguists of the team
    all_linguists = pd.read_pickle(file_loc)

    # Set the value of the desire attribute to the new one
    all_linguists.loc[all_linguists["username"] == username, attribute] = new_value

    # Save the file
    all_linguists.to_pickle(file_loc)

    return None


def availability_check(username, task, team=None):
    """
    This function checks if a linguist has enough availability to fit in a task.

    The availability of the linguist should be checked first by looking at the required_hours of the task, converting it to the required hours for the linguist
    based on the ratio difference between the default rate and linguist's own output rate, then use the deadline of the task to determine which day to check first,
    starting from the deadline day, then work backwards. 

    If the linguist has enough availability, returns start_datetime and end_datetime
    Otherwise, returns False

    """

    if team is None:
        team = cookie_team

    # determine the task DB file location
    task_db_file_loc = f"task-allocation-planner/database/{team}/{team}_tasks.pkl"
    
    # Load the task DB
    all_tasks = pd.read_pickle(task_db_file_loc)

    # Get the default required hours, default rating, deadline
    default_required_hrs = all_tasks.loc[all_tasks["name"] == task, "required_hours"].values[0]
    default_rate = all_tasks.loc[all_tasks["name"] == task, "default_rate"].values[0]
    deadline = all_tasks.loc[all_tasks["name"] == task, "deadline"].values[0] # The deadline is currently a numpy.datetime64 object
    deadline_date = np.datetime64(deadline, 'D').astype(str) # This extracts just the date, and change it into a string

    # determine the linguist DB file location
    linguist_db_file_loc = f"task-allocation-planner/database/{team}/{team}_linguists.pkl"

    # Load the linguist DB
    all_linguists = pd.read_pickle(linguist_db_file_loc)

    # Get the linguist output rate & end_time
    linguist_output_rate = all_linguists.loc[all_linguists["username"] == username, "output"].values[0]
    print(f"linguist output: {linguist_output_rate}")
    linguist_end_time = all_linguists.loc[all_linguists["username"] == username, "end_time"].values[0] # Type is currently a numpy.datetime64
    print(f"linguist_end_time = {linguist_end_time}")
    # linguist_end_time_dt = pd.Timestamp(linguist_end_time).to_pydatetime() # This is now a datetime type

    # calculate the ratio between default and linguist's own output rate, then calculate the linguist required hours by applying the ratio to the default figure
    ratio = default_rate / linguist_output_rate
    print(f"ratio: {ratio}")
    linguist_required_hrs = default_required_hrs * ratio
    print(f"linguist_required_hrs: {linguist_required_hrs}")

    # Load the workload DB and check the columns to see if the deadline date exist
    workload_db_file_loc = f"task-allocation-planner/database/{team}/{username}_workload.pkl"
    linguist_workload = pd.read_pickle(workload_db_file_loc)


    ### Now start to check availability ###

    # First check if the deadline date is today
    now = datetime.now()
    # now_time = now.time()
    # print(f"now_time = {now_time}")
    today_date = now.strftime('%Y-%m-%d') # Create today's date in string
    print(f"today_date = {today_date}")

    # Obtain the already occupied hours for today
    occupied_today = occupied_hours(today_date, username)
    print(f"occupied_today = {occupied_today}")

    # Calculate today's remaining availability
    linguist_end_time_today = datetime.combine(datetime.today(), linguist_end_time)
    today_remaining_availability = ((linguist_end_time_today - now).total_seconds() / 3600) - occupied_today
    print(f"today_remaining_availability = {today_remaining_availability}")

    if deadline_date == today_date:
        if linguist_required_hrs < today_remaining_availability: # linguist has enough availability
            end_datetime = linguist_end_time_today - timedelta(hours=occupied_today)
            print(f"end_datetime = {end_datetime}")
            start_datetime = end_datetime - timedelta(hours=linguist_required_hrs)
            print(f"start_datetime = {start_datetime}")

            return start_datetime, end_datetime, linguist_required_hrs
        else:
            return False
    else: # deadline is not today
        print("testing")
        pass


    # first check if the deadline date is today, if yes, create a variable that equals to datetime.now(), and calculate the remaining availability
    # if remaining availability > linguist_required_hrs, then the linguist has time to do this task, otherwise no time.
    # If the deadline date is not today.
    # While linguist_required_hrs > 0, check if workload DB has the column for deadline date,
    # if it doesn't (first job for that day) then create a column with the deadline date, and make the value the same as contractual_hours.
    # Then deduct the linguist_required_hrs from contractual_hours, if contractual_hours becomes less than 0 (meaning the required hours is larger than available hours for that day)
    # In this case, keep a temp_note for the end_datetime, which is the same as the deadline, then deduct contractual_hours from linguistic_required_hrs
    # 
    return None


def occupied_hours(date, username, team=None):
    """
    This function returns the sum of occupied hours on a specific date for a linguist
    """
    if team is None:
        team = cookie_team

    # determine the file location and open it
    task_db_file_loc = f"task-allocation-planner/database/{team}/{team}_tasks.pkl"
    all_tasks = pd.read_pickle(task_db_file_loc)

    # Make deadline column into datetime format, then convert to date only, then to string
    all_tasks['deadline'] = pd.to_datetime(all_tasks['deadline'])
    deadline_dates = all_tasks['deadline'].dt.date.astype(str)

    # Create the condition for filtering
    condition = (deadline_dates == date) & (all_tasks["assignee"] == username)

    # Calculate the sum of assignee_required_hours that meets the condition
    sum_hrs = all_tasks[condition]["assignee_required_hours"].sum()

    return sum_hrs



def assign_task_to_linguist(username, task, team=None):
    """
    This function assigns an existing task to a linguist.

    Parameters:
    username => string - The username of the linguist
    task => string - The name of the task
    team => string - The team that the linguist is in

    3 Things need to happen when assigning a task to a linguist
        
        1. Check the availability using the availability_check() function

            If the availability result is false, the linguist has no availability,
            otherwise we should receive start_datetime, end_datetime & linguist_required_hrs

        1. Linguist DB update
        The plate attribute of the linguist should be updated by having the task name added to it

        2. workload DB update
        Use the function availability_check() first.
        If the linguist has enough availability, the task can be assigned, and will occupy the availability of the
        linguist for the day(s) and hours that it occupies. If the linguist doesn't have enough availability after working from the deadline backwards up to the current
        day, then the task will not be assigned to the linguist.

        3. Task DB update
        The Task DB will receive 4 updates when a task is assigned to a linguist
            - assignee attribute changed to the linguist's username
            - status attribute changed to "assigned"
            - start_datetime changed to the starting datetime of the task
            - end_datetime changed to the end datetime of the task

    """
    if team is None:
        team = cookie_team

    ### 1. Check availability ###

    available = availability_check(username, task)

    if not available:
        print("Linguist does not have enough availability")
        return False

    else: ### 2. Update Linguist DB

        # determine the file location
        ling_db_file_loc = f"task-allocation-planner/database/{team}/{team}_linguists.pkl"

        # Load all linguists out
        all_linguists = pd.read_pickle(ling_db_file_loc)

        # First retrieve the current plate
        current_plate = get_attribute(username, "plate", team)

        # See if the plate is empty
        if current_plate == "":

            # If the plate is empty, this is the first task, simply update and save the database
            all_linguists.loc[all_linguists["username"] == username, "plate"] = task
            all_linguists.to_pickle(ling_db_file_loc)
        
        else:
            # Change the current plate from string to a list
            plate_list = current_plate.split(",")

            # Add the new task to the list
            plate_list.append(task)

            # Change the list back into a string
            new_plate = ','.join(plate_list)

            # Update and save the database
            all_linguists.loc[all_linguists["username"] == username, "plate"] = new_plate
            all_linguists.to_pickle(ling_db_file_loc)
    

        ### 3. Task DB Update ###

        # determine the file location
        task_db_file_loc = f"task-allocation-planner/database/{team}/{team}_tasks.pkl"

        # Load all tasks out
        all_tasks = pd.read_pickle(task_db_file_loc)

        # Assign the task to the linguist and save database
        all_tasks.loc[all_tasks["name"] == task, "assignee"] = username
        all_tasks.loc[all_tasks["name"] == task, "start_datetime"] = available[0] # start_datetime
        all_tasks.loc[all_tasks["name"] == task, "end_datetime"] = available[1] # end_datetime
        all_tasks.loc[all_tasks["name"] == task, "assignee_required_hours"] = available[2] # linguist_required_hrs

        all_tasks.to_pickle(task_db_file_loc)

        ### 4. workload DB Update ###

        workload_db_file_loc = f"task-allocation-planner/database/{team}/{username}_workload.pkl"
        linguist_workload = pd.read_pickle(workload_db_file_loc)

        date_to_record = available[1].strftime('%Y-%m-%d') # Get the date of end_datetime as string
        print(f"original date: {date_to_record}")
        hours_to_allocate = available[2]
        print(f"original hours to allocate: {hours_to_allocate}")

        while hours_to_allocate > 0:
            if date_to_record in linguist_workload.columns:
                workload_so_far = linguist_workload.at[0, date_to_record]
                print(f"date found in DB, workload so far: {workload_so_far}")
                still_available = linguist_workload.at[0, "contractual_availability"] - workload_so_far
                print(f"still available = {still_available}")
                if still_available >= hours_to_allocate:
                    linguist_workload.at[0, date_to_record] = workload_so_far + hours_to_allocate
                    print(f"new total workload: {linguist_workload.at[0, date_to_record]}")
                    hours_to_allocate = 0
                    linguist_workload.to_pickle(workload_db_file_loc) # Save the file

                else: # not enough availability to cover hours to allocate
                    linguist_workload.at[0, date_to_record] = linguist_workload.at[0, "contractual_availability"] # Fill the day to max
                    print(f"day should be filled: {linguist_workload.at[0, date_to_record]}")
                    hours_to_allocate = hours_to_allocate - still_available # reduce hours to allocate by the time allocated to this day
                    print(f"remaining hours_to_allocate: {hours_to_allocate}")

                    # Move the date backwards by 1 day
                    date_datetime = datetime.strptime(date_to_record, '%Y-%m-%d')
                    previous_date = date_datetime - timedelta(hours=24)
                    date_to_record = previous_date.strftime('%Y-%m-%d')
                    print(f"new date: {date_to_record}")

                    linguist_workload.to_pickle(workload_db_file_loc) # Save the file
            
            else: # The workload DB doesn't have today's date
                if linguist_workload.at[0, "contractual_availability"] > hours_to_allocate:
                    linguist_workload[date_to_record] = hours_to_allocate
                    print(f"today's date not in DB, now added date and workload: {date_to_record}, {linguist_workload.at[0, date_to_record]}")
                    hours_to_allocate = 0
                    linguist_workload.to_pickle(workload_db_file_loc) # Save the file
                
                else: # The availability this day cannot cover the hours_to_allocate
                    linguist_workload.at[0, date_to_record] = linguist_workload.at[0, "contractual_availability"] # Fill the day to max
                    hours_to_allocate = hours_to_allocate - linguist_workload.at[0, "contractual_availability"] # reduce hours to allocate by the time allocated to this day

                    # Move the date backwards by 1 day
                    date_datetime = datetime.strptime(date_to_record, '%Y-%m-%d')
                    previous_date = date_datetime - timedelta(hours=24)
                    date_to_record = previous_date.strftime('%Y-%m-%d')

                    linguist_workload.to_pickle(workload_db_file_loc) # Save the file

        return True


def remove_task_from_linguist(username, task, team=None):
    if team is None:
        team = cookie_team

    # determine the file location
    file_loc = f"task-allocation-planner/database/{team}/{team}_linguists.pkl"

    # Load all linguists out
    all_linguists = pd.read_pickle(file_loc)

    # First retrieve the current plate
    current_plate = get_attribute(username, "plate", team)

    plate_list = current_plate.split(",")
    plate_list.remove(task)
    new_plate = ','.join(plate_list)
    all_linguists.loc[all_linguists["username"] == username, "plate"] = new_plate
    # Save the file
    all_linguists.to_pickle(file_loc)

    return None


# Function 2B written for client_exp, expertise, client_redflag
def function_2b_written():
    pass

# Not sure if required
def linguist_data_as_list(username, team=None):
    if team is None:
        team = cookie_team
    
    # First read the file containing all linguists of the team
    all_linguists = pd.read_pickle(f'task-allocation-planner/database/{team}/{team}_linguists.pkl')

    # Find the linguist by using the username provided
    target_linguist = all_linguists[all_linguists["username"] == username]

    # Start to create the list
    target_linguist_data = []
    for column in all_linguists.columns:
        target_linguist_data.append(target_linguist[column].values[0])


    return target_linguist_data


##########
# Task functions
##########

def create_task(name, locale, task_type, deadline, default_rate, required_hours, team=None, assignee=None):
    
    if team is None:
        team = cookie_team

    task = Task(name, locale, task_type, deadline, default_rate, required_hours, team, assignee)
    return task


def add_to_task_db(task, team=None):
    if team is None:
        team = cookie_team

    # determine the file location
    file_loc = f"task-allocation-planner/database/{team}/{team}_tasks.pkl"

    # First convert the task data into a DataFrame
    data = vars(task)
    df = pd.DataFrame([data])

    # Check if there is already an existing database
    if os.path.exists(file_loc):
        existing_df = pd.read_pickle(file_loc)

        # Add the whole row of the new task DataFrame into the the last row of the existing database
        existing_df.loc[len(existing_df)] = df.iloc[0, :]

        # Save the database
        existing_df.to_pickle(file_loc)

    else: # this is the first task, save the database
        df.to_pickle(file_loc)


def remove_from_task_db(task_name, team=None):
    if team is None:
        team = cookie_team

    # determine the file location
    file_loc = f"task-allocation-planner/database/{team}/{team}_tasks.pkl"

    # First read the file containing all tasks of the team
    all_tasks = pd.read_pickle(file_loc)

    # Identify the row index
    user_index = all_tasks[all_tasks['name'] == task_name].index

    # Remove the row
    all_tasks.drop(user_index, inplace=True)

    # Save the database
    all_tasks.to_pickle(file_loc)

    return None



##########
# Testing part
##########

# farm = create_linguist("farm", "farm bro", "fb")
# create_workload_db(farm)
# add_to_linguist_db(farm)

# kensolo = create_linguist("kensolo", "Ken Solo", "ks")
# create_workload_db(kensolo)
# add_to_linguist_db(kensolo)

# end_time = get_attribute("kensolo", "end_time")
# print(end_time)
# print(type(end_time))

# set_attribute("kensolo", "end_time", time(23,0,0))

# remove_task_from_linguist("kensolo", "lso")

# assign_task_to_linguist("kensolo", "review")

# new_name = get_attribute("kensolo", "plate")
# print(new_name)

# data = linguist_data_as_list("kensolo")
# print(data)

# remove_from_linguist_db("ffarm")

# task1 = create_task("translation2", "tw", "review", datetime(2023, 7, 2, 17, 0), 2400, 2)
# add_to_task_db(task1)

# remove_from_task_db("review")

# set_attribute("kensolo", "output", 100000)

decision = assign_task_to_linguist("kensolo", "review")
print(decision)
