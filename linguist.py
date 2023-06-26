class Linguist:
    """
    A class to represent a linguist.

    Attributes:
        <String attributes>
        name: string - The name of the linguist.
        locale: string - The primary locale that the linguist translates into. e.g. de-DE
        team: string - The strategic team in Alpha that the linguist belongs to. e.g. Nexus

        <Number attributes>
        available_hours: float - The contractual available hours of the linguist, default is 8.0
        output: int - The linguist's own daily output word rate, default is 2400
        keep_deadlines: int - The ability to keep deadlines, a score rating from 1 to 10, default is 10
        
        <Set attributes>
        expertise: set - The area(s) of expertise of the linguist, default is an empty set
        client_exp: set = The client(s) that the linguist has experience working on, default is an empty set

        <Dict attributes>
        client_feedback: dict = The feedback received from any client, in a dictionary format {"client": "feedback"}, default is an empty dict
        plate: dict - The task(s) assigned to the linguist, in a dictionary format {"task.name": "task.required_hours"}, default is an empty dict

        <Task type attributes (all boolean and all yes by default)>
        translation
        review
        lso
        client_meeting
        test_translation

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
    
    def __init__(self, name: str, locale: str, team: str,
                 available_hours: float=8.0, output: int=2400, keep_deadlines: int=10,
                 client_exp: set={}, expertise: set={},
                 client_feedback: dict={}, plate: dict={},
                 translation: bool=True, review: bool=True, lso: bool=True, client_meeting: bool=True, test_translation: bool=True):
        # <String attributes>
        self.name = name
        self.locale = locale
        self.team = team

        # <Number attributes>
        self.available_hours = available_hours
        self.output = output
        self.keep_deadlines = keep_deadlines

        # <Set attributes>
        self.client_exp = client_exp
        self.expertise = expertise

        # <Dict attributes>
        self.client_feedback = client_feedback
        self.plate = plate

        # <Task type attributes>
        self.translation = translation
        self.review = review
        self.lso = lso
        self.client_meeting = client_meeting
        self.test_translation = test_translation


    def get_attribute(self, attr_name):
        """
        Returns the value of the attribute, if no such attribute exists, returns None
        """
        attr = attr_name.lower()
        if hasattr(self, attr):
            if attr is self.client_exp or self.expertise: # check if the attribute is one of the set attributes, if yes, return the sorted value of the attribute
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


    def set_set_attribute(self, attr_name, value, action=None):
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
            if isinstance(attr_value, set) and action:
                if action == 'add':
                    attr_value.add(value)
                elif action == 'remove':
                    if value in attr_value:
                        attr_value.remove(value)
                    else:
                        print(f"Can't find {value} in the list")
                else:
                    print("Unknown action, please enter 'add' or 'remove'")
            else:
                print("Action needed, please enter 'add' or 'remove'")
        else:
            print(f"No attribute named {attr_name}")


    def set_dict_attribute(self, attr_name, key_name, value):
        """
        Update an attribute with datatype dict. Provide the attribuate name, key & value.

        Applicable attribute names:
        client_feedback
        plate

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
        plate

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
