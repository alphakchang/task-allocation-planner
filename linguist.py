from datetime import datetime, time

class Linguist:
    """
    A class to represent a linguist.

    Attributes:
        <string attributes>
        username: string - The Alpha username of the linguist.
        name: string - The name of the linguist.
        locale: string - The primary locale that the linguist translates into. e.g. de-DE
        team: string - The strategic team in Alpha that the linguist belongs to. e.g. Nexus

        <number attributes>
        contract_hours: float - The contractual available hours of the linguist, default is 8.0
        output: int - The linguist's own daily output word rate, default is 2400
        keep_deadlines: int - The ability to keep deadlines, a score rating from 1 to 10, default is 10

        <datetime attributes>
        start_time: datetime - The start time of the linguist on the day, default is 9am e.g. datetime(2023, 6, 27, 9, 0)
        end_time: datetime - The end time of the linguist on the day

        <list attributes>
        plate: list - A list of all the tasks assigned to the linguist, each task is an instance of class Task, default is an empty list.

        <set attributes>
        client_exp: set - The client(s) that the linguist has experience working on, default is an empty set
        expertise: set - The area(s) of expertise of the linguist, default is an empty set
        client_redflag: set - Any clients that this linguist shouldn't work on, default is an empty set

        <Task type attributes (all boolean and all yes by default)>
        translation
        review
        lso
        client_meeting
        test_translation


    Properties:
        <Availability property>
        remaining_availability_today: float - The remaining availability for the linguist today.
    
    Methods:
        <Attribute related>
        get_attribute(attr_name) - returns the value of the attribute, param = attribute name
        set_attribute(attr_name, new_value) - updates the value of an attribute
        set_set_attribute(self, attr_name, value, action=None) - updates the value of an attribute with datatype set
        set_dict_attribute(self, attr_name, key_name, value) - updates the value of an attribute with datatype dict
        remove_key_from_dict_attribute(self, attr_name, key_name) - removes the key & value pair from a dict

        <Task related>
        add_task(self, task) - add a task to plate
        remove_task(self, task) - removes a task from plate
    """
    
    def __init__(self, username: str, name: str, locale: str, team: str,
                 contract_hours: float, output: int, keep_deadlines: int = 10,
                 start_time: time = None, end_time: time = None,
                 plate = None,
                 client_exp = None, expertise = None, client_redflag = None,
                 translation: bool = True, review: bool = True, lso: bool = True,
                 client_meeting: bool = True, test_translation: bool = True):
        
        # <string attributes>
        self.username = username
        self.name = name
        self.locale = locale
        self.team = team

        # <number attributes>
        self.contract_hours = contract_hours
        self.output = output
        self.keep_deadlines = keep_deadlines

        # <datetime attributes>
        if start_time is None:
            start_time = time(9, 0, 0)
        self.start_time = start_time

        if end_time is None:
            end_time = time(17, 0, 0)
        self.end_time = end_time

        # <list attributes>
        if plate is None:
            plate = ""
        self.plate = plate

        # <set attributes>
        if client_exp is None:
            client_exp = ""
        self.client_exp = client_exp

        if expertise is None:
            expertise = ""
        self.expertise = expertise

        if client_redflag is None:
            client_redflag = ""
        self.client_redflag = client_redflag

        # <Task type attributes>
        self.translation = translation
        self.review = review
        self.lso = lso
        self.client_meeting = client_meeting
        self.test_translation = test_translation


    @property
    def remaining_availability_today(self):
        # The remaining_availability_today of a linguist is constantly changing since time is constantly moving forward, this attribute will be calculated by:
        # finding the time_passed since start_time, then deduct contract_hours by time_passed, and all the task values in plate due today
        time_passed = datetime.now() - self.start_time
        return self.contract_hours - (time_passed.total_seconds() / 3600)


    def get_attribute(self, attr_name):
        """
        Returns the value of the attribute, if no such attribute exists, returns None
        """
        attr = attr_name.lower()
        if hasattr(self, attr):
            if attr is self.client_exp or self.expertise or self.client_redflag: # check if the attribute is one of the set attributes, if yes, return the sorted value of the attribute
                print(f"{attr_name}: {sorted(getattr(self, attr))}")
                return sorted(getattr(self, attr))
            else: # if the attribute is not one of the set attributes, return the value of the attribute
                print(f"{attr_name}: {getattr(self, attr)}")
                return getattr(self, attr)
        else:
            print(f"No attribute named {attr_name}")
            return None


    def set_attribute(self, attr_name, new_value):
        """
        Updates an attribute to a new given value, if no such attribute exists, nothing happens
        This method is applicable to all attributes when the datatype is not set or dict
        """
        attr = attr_name.lower()
        if hasattr(self, attr):
            setattr(self, attr, new_value)
            print(f"{attr_name}: is now set to {getattr(self, attr)}")
        else:
            print(f"No attribute named {attr_name}")


    def set_set_attribute(self, attr_name, value, action: str = None):
        """
        Update an attribute with datatype set. Provide the attribute name, the value, and the action.

        Applicable attribute names:
        client_exp
        expertise

        Applicable actions:
        add
        remove

        If the attribute doesn't exist or no action is given, nothing will happen
        """
        attr = attr_name.lower()
        if hasattr(self, attr):
            attr_value = getattr(self, attr)
            if isinstance(attr_value, set):
                if action is None:
                    print("Action needed, please enter 'add' or 'remove'")
                elif action == 'add':
                    attr_value.add(value)
                elif action == 'remove':
                    if value in attr_value:
                        attr_value.remove(value)
                    else:
                        print(f"Can't find {value} in the list")
                else:
                    print("Unknown action, please enter 'add' or 'remove'")
                
                setattr(self, attr, attr_value)
                # if action == 'add':
                #     attr_value.add(value)
                # elif action == 'remove':
                #     if value in attr_value:
                #         attr_value.remove(value)
                #     else:
                #         print(f"Can't find {value} in the list")
                # else:
                #     print("Unknown action, please enter 'add' or 'remove'")
            else:
                print("Not a set")
        else:
            print(f"No attribute named {attr_name}")


    def set_dict_attribute(self, attr_name, key_name, value):
        """
        Update an attribute with datatype dict. Provide the attribuate name, key & value.

        Applicable attribute names:
        client_feedback

        Both the key and value must be provided, otherwise nothing will happen
        """
        attr = attr_name.lower()
        key = key_name.lower()
        if hasattr(self, attr):
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, dict):
                attr_value[key] = value  # update dict
            else:
                print("Unknown action, please provide both key & value pair")
        else:
            print(f"No attribute named {attr_name}")

    
    def remove_key_from_dict_attribute(self, attr_name, key_name):
        """
        Removes the key & value pair from a dictionary. Provide the key name.

        Applicable attribute names:
        client_feedback

        Key name must be provided, otherwise nothing will happen
        """
        attr = attr_name.lower()
        key = key_name.lower()
        if hasattr(self, attr):
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, dict):
                if key in attr_value:
                    del attr_value[key]  # remove key-value pair from dict
                else:
                    print(f"{key_name} is not found in the dictionary")
            else:
                print(f"{attr_name} is not a dictionary")
        else:
            print(f"No attribute named {attr_name}")


    def to_dict(self):
        """Convert the Linguist object's data to a dictionary."""
        # return {
        #     'name': self.name,
        #     'locale': self.locale,
        #     'team': self.team,
        #     'start_time': self.start_time,
        #     'end_time': self.end_time,
        #     'contract_hours': self.contract_hours,
        #     'output': self.output,
        #     'keep_deadlines': self.keep_deadlines,

        #     <datetime attributes>
        # start_time: datetime - The start time of the linguist on the day, default is 9am e.g. datetime(2023, 6, 27, 9, 0)
        # end_time: datetime - The end time of the linguist on the day

        # <number attributes>
        # contract_hours: float - The contractual available hours of the linguist, default is 8.0
        # output: int - The linguist's own daily output word rate, default is 2400
        # keep_deadlines: int - The ability to keep deadlines, a score rating from 1 to 10, default is 10
        
        # <Availability attribute>
        # remaining_availability_today: float - The remaining availability for the linguist today.

        # <list attributes>
        # plate: list - A list of all the tasks assigned to the linguist, each task is an instance of class Task, default is an empty list.

        # <set attributes>
        # expertise: set - The area(s) of expertise of the linguist, default is an empty set
        # client_exp: set = The client(s) that the linguist has experience working on, default is an empty set

        # <dict attributes>
        # client_feedback: dict = The feedback received from any client, in a dictionary format {"client": "feedback"}, default is an empty dict

        # <Task type attributes (all boolean and all yes by default)>
        # translation
        # review
        # lso
        # client_meeting
        # test_translation
        # }
        pass
    

    def total_workload_until_datetime(self, datetime):
        # for task in self.plate:
        pass


    def availability_until_deadline():
        pass


    def add_task(self, task):
        """
        This function adds the task to the linguist's plate, it will add: 
            task_name being the key and real_required_hours being the value together as a dictionary pair.
            real_required_hours is the product of required hours and the ratio between
            linguist output and default output of 2400.
        
        Once the task is added, the linguist's available hours will go down by the amount of real_required_hours.
        """
        task_name = task.name # corresponding to task's name attribute
        required_hours = task.required_hours # corresponding to task's required_hours attribute
        real_required_hours = required_hours * (2400 / self.output)
        self.plate[task_name] = real_required_hours
        self.available_hours = self.available_hours - real_required_hours


    def remove_task(self, task):
        """
        This function uses the pop method to remove a task from the linguist plate, to get the real_required_hours.
        Then add the hours back to the linguists available hours total
        """
        task_name = task.name
        hours_to_add = self.plate.pop(task_name)
        self.available_hours = self.available_hours + hours_to_add

