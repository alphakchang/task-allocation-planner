from linguist import Linguist
# from task import Task
# import datetime

# ken = Linguist("Ken", "TW", "Nexus")
# task1 = Task("review", "TW", 3)

# ken.get_attribute("client_feedback")
# ken.get_attribute("output")

# ken.set_dict_attribute("client_feedback", key_name="burb", value="ddd")
# ken.get_attribute("client_feedback")
# ken.set_dict_attribute("client_feedback", key_name="burb", value="good")
# ken.get_attribute("client_feedback")
# ken.remove_key_from_dict_attribute("client_feedback", key_name="burb")
# ken.get_attribute("client_feedback")
# ken.set_dict_attribute("plate", key_name="burb", value=5.5)
# ken.get_attribute("plate")
# ken.remove_key_from_dict_attribute("plate", key_name="burb")
# ken.get_attribute("plate")

# now = datetime.time.now()
# print(now)

# start = datetime.time(9, 30)
# print(start)
# passed = now - start
# print(passed)

# ken.get_attribute("client_exp")

# from datetime import datetime, time

# # Get the current datetime
# now = datetime.now()

# # Define the earlier time
# earlier_time = time(hour=9, minute=30)

# # Create a datetime object for the earlier time, using the current date
# earlier_time_today = datetime.combine(now.date(), earlier_time)

# # Check if the current time is before or after 9:30 AM
# if now >= earlier_time_today:
#     # If it's after 9:30 AM, subtract the earlier time from the current time
#     time_difference = now - earlier_time_today
# else:
#     # If it's before 9:30 AM, calculate the time from 9:30 AM to midnight of the previous day,
#     # and add the time that has passed today
#     time_difference = (datetime.combine(now.date(), time.max) - earlier_time_today) + (now - datetime.combine(now.date(), time.min))

# # Print the time difference
# print(f"{time_difference.seconds // 3600} hours, {(time_difference.seconds // 60) % 60} minutes and {time_difference.seconds % 60} seconds")


# ken = Linguist("Ken", "tw", "nexus", contract_hours=5.0)
farm = Linguist("farm", "zh", "a-team")

# print(ken.get_attribute("start_time"))
print(farm.get_attribute("remaining_availability_today"))