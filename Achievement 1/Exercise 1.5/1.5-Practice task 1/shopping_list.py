class ShoppingList:
    def __init__(self, list_name):
        self.list_name = (list_name,)
        self.shopping_list = []

    def add_item(self, item):
        if not item in self.shopping_list:
            self.shopping_list.append(item)

    def remove_item(self, item):
        if not item in self.shopping_list:
            self.shopping_list.remove(item)

    def view_lsit(self):
        print(self.shopping_list)


pet_store_list = ShoppingList(list_name="Pet Store Shopping List")
pet_store_list.add_item("Dog Food")
pet_store_list.add_item("Frisbee")
pet_store_list.add_item("Bowl")
pet_store_list.add_item("Collars")
pet_store_list.add_item("Flea Collars")

pet_store_list.remove_item("Flea Collars")

pet_store_list.add_item("Frisbee")

pet_store_list.view_lsit()
