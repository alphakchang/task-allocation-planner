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