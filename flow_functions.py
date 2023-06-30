# This will be the backend python server

from task import Task
from linguist import Linguist
from availability import Availability
from datetime import datetime
import pandas as pd
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


def create_availability_db(linguist, team=None):
    if team is None:
        team = cookie_team
    
    # determine the file location
    file_loc = f"task-allocation-planner/database/{team}/{linguist.username}_availability.pkl"

    # create the availability class
    linguist_availability = Availability(linguist.username, linguist.contract_hours)

    # create the DataFrame
    data = vars(linguist_availability)
    df = pd.DataFrame([data])
    df.to_pickle(file_loc)


def remove_from_linguist_db(username, team=None):
    if team is None:
        team = cookie_team

    # determine the file location
    file_loc = f"task-allocation-planner/database/{team}/{team}_linguists.pkl"

    # First read the file containing all linguists of the team
    all_linguists = pd.read_pickle(file_loc)

    # Identify the row index
    user_index = all_linguists[all_linguists['username'] == username].index

    # Remove the row
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


def assign_task_to_linguist(username, task, team=None):
    if team is None:
        team = cookie_team

    ### Linguist DB Part ###

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
    

    ### Task DB Part ###

    # determine the file location
    task_db_file_loc = f"task-allocation-planner/database/{team}/{team}_tasks.pkl"

    # Load all tasks out
    all_tasks = pd.read_pickle(task_db_file_loc)

    # Assign the task to the linguist and save database
    all_tasks.loc[all_tasks["name"] == task, "assignee"] = username
    all_tasks.to_pickle(task_db_file_loc)

    return None


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
# create_availability_db(farm)
# add_to_linguist_db(farm)

# kensolo = create_linguist("kensolo", "farm bro", "fb")
# create_availability_db(kensolo)
# add_to_linguist_db(kensolo)

# set_attribute("ffarm", "translation", False)

# remove_task_from_linguist("kensolo", "lso")

# assign_task_to_linguist("kensolo", "review")

# new_name = get_attribute("kensolo", "plate")
# print(new_name)

# data = linguist_data_as_list("kensolo")
# print(data)

# remove_from_linguist_db("ffarm")

# task1 = create_task("review", "tw", "review", datetime(2023, 6, 30, 17, 0), 2400, 1.5)
# add_to_task_db(task1)

# remove_from_task_db("review")