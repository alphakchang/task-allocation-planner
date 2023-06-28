from linguist import Linguist
import pandas as pd

ken = Linguist("Ken", "TW", "Nexus")
ken.get_attribute("expertise")
ken.set_set_attribute("expertise", value="lambda", action="add")
ken.get_attribute("expertise")

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


# farm = Linguist("farm", "zh", "a-team")

# # print(ken.get_attribute("start_time"))
# print(farm.get_attribute("remaining_availability_today"))