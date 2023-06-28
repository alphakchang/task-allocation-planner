from linguist import Linguist
import pandas as pd
import os

# This module contains the functions required for the workflow

# The below global variable should go to main.py
cookie_team = "nexus"


def get_team_name():
    """
    This function simply returns the team name in lower cases.
    The team folder is selected by checking the cookie_team variable.
    """
    with open(f'task-allocation-planner/database/{cookie_team}/team_name.txt', 'r') as file:
        team_name = file.read()
    return team_name.lower()


def create_linguist(username, name, locale, team=cookie_team, contract_hours=8.0, output=2400):
    linguist = Linguist(username, name, locale, team, contract_hours, output)
    return linguist


def linguist_data_as_list(linguist):
    pass



def add_to_linguist_db(linguist):

    # determine the file name
    file_loc = f"task-allocation-planner/database/{cookie_team}/{get_team_name()}_linguists.pkl"

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




# testing part
ken = create_linguist("kchang", "ken", "tw")
print(ken.remaining_availability_today)

# add_to_linguist_db(ken)

# farm = create_linguist("ffarm", "farmbro", "tw", "nexus")
# print(farm.remaining_availability_today)

add_to_linguist_db(ken)

# kensolo = create_linguist("ksolo", "ken solo", "ks", "nexus")
# add_to_linguist_db(kensolo)

# team_name = get_team_name()
# print(team_name)