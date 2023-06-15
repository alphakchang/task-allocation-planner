from objects import Linguist, Task

ken = Linguist("Ken", "TW", 7, 1200)
task1 = Task("review", "TW", 3)

ken.add_task(task1)
print(ken.show_plate())
print(ken.show_available_hours())

ken.remove_task("review")
print(ken.show_plate())
print(ken.show_available_hours())