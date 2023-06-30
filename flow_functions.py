# This will be the backend python server

from linguist import Linguist
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


def add_task(username, task, team=None):
    if team is None:
        team = cookie_team

    # determine the file location
    file_loc = f"task-allocation-planner/database/{team}/{team}_linguists.pkl"

    # Load all linguists out
    all_linguists = pd.read_pickle(file_loc)

    # First retrieve the current plate
    current_plate = get_attribute(username, "plate", team)

    # See if the plate is empty
    if current_plate == "":
        all_linguists.loc[all_linguists["username"] == username, "plate"] = task
        # Save the file
        all_linguists.to_pickle(file_loc)
    
    else:
        plate_list = current_plate.split(",")
        plate_list.append(task)
        new_plate = ','.join(plate_list)
        all_linguists.loc[all_linguists["username"] == username, "plate"] = new_plate
        # Save the file
        all_linguists.to_pickle(file_loc)
    
    return None

def remove_task(username, task, team=None):
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

# testing part

# kensolo = create_linguist("kensolo", "Ken Solo", "KS")
# print(kensolo.remaining_availability_today)
# add_to_linguist_db(kensolo)

# set_attribute("ffarm", "translation", False)

# remove_task("kensolo", "translation-1-2-3")

# new_name = get_attribute("kensolo", "plate")
# print(new_name)

data = linguist_data_as_list("kensolo")
print(data)