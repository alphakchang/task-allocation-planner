class Linguist:
    """
    A class to represent a linguist.

    Attributes:
        name: The linguist's name.
        locale: The linguist's locale.
        available_hours: The contractual available hours of the linguist
        output: the linguist's own daily output words
        plate: The task(s) assigned to the user, in a dictionary format {"task.name": "task.required_hours"}
    """
    
    def __init__(self, name, locale, available_hours=8, output=2400, plate={}):
        self.name = name
        self.locale = locale
        self.available_hours = available_hours
        self.output = output
        self.plate = plate

    def show_plate(self):
        return self.plate
    
    def show_available_hours(self):
        return self.available_hours
    
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

    def remove_task(self, task_name):
        """
        This function uses the pop method to remove a task from the linguist plate, to get the real_required_hours.
        Then add the hours back to the linguists available hours total
        """
        hours_to_add = self.plate.pop(task_name)
        self.available_hours = self.available_hours + hours_to_add

class Task:
    """
    A class to represent a task.

    Attributes:
        name: The name of the task, including the job number & task number passed from the database.
        locale: The locale of the task.
        required_hours: The required hours calculated using the default output of 2400.
        assignee: Who is this task assgined to.
    """
    
    def __init__(self, name, locale, required_hours, assignee=None):
        self.name = name
        self.locale = locale
        self.required_hours = required_hours
        self.assignee = assignee

    def display_info(self):
        print(f"'{self.name}' for {self.locale}. workload: {self.required_hours}. assignee: {self.assignee}")
