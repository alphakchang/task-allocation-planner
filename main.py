from linguist import Linguist
from task import Task

ken = Linguist("Ken", "TW", "Nexus")
task1 = Task("review", "TW", 3)

ken.get_attribute("client_feedback")
ken.get_attribute("output")

ken.set_dict_attribute("client_feedback", key_name="burb", value="ddd")
ken.get_attribute("client_feedback")
ken.set_dict_attribute("client_feedback", key_name="burb", value="good")
ken.get_attribute("client_feedback")
ken.remove_key_from_dict_attribute("client_feedback", key_name="burb")
ken.get_attribute("client_feedback")
ken.set_dict_attribute("plate", key_name="burb", value=5.5)
ken.get_attribute("plate")
ken.remove_key_from_dict_attribute("plate", key_name="burb")
ken.get_attribute("plate")

# ken.get_attribute("client_exp")