from datetime import datetime

class Task:
    """
    A class to represent a task.

    Attributes:

        name => str: The name of the task, including the job number & task number passed from the database
        locale => str: The locale of the task
        task_type => string: The type of task, options = translation, review, lso, client_meeting, test_translation
        deadline => datetime: The deadline of the task
        default_rate => int: The default rate set by TradeWind
        required_hours => float: The required hours calculated using the default rate
        assignee_required_hours => float: The required hours calculated using the assignee's output rate
        team => string: The team this task is in
        assignee => string: The username of the person who has this task on plate
        status => string: The status of the task - Open - Assigned - In Progress - Completed
        completion_date => datetime: The datetime that the task was completed
        start_datetime => datetime: The datetime that the task is scheduled to start
        end_datetime => datetime: The datetime that the task is scheduled to end
        
    """
    
    def __init__(self, name: str, locale: str, task_type: str, deadline: datetime,
                 default_rate: int, required_hours: float, team: str,
                 assignee: str = None, assignee_required_hours: float = None, status: str = None,
                 completion_date: datetime = None, start_datetime: datetime = None, end_datetime: datetime = None):
        
        self.name = name
        self.locale = locale
        self.task_type = task_type
        self.deadline = deadline
        self.default_rate = default_rate
        self.required_hours = required_hours
        self.assignee_required_hours = assignee_required_hours
        self.team = team
        self.assignee = assignee

        if status is None:
            status = "Open"

        self.status = status
        self.completion_date = completion_date
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        