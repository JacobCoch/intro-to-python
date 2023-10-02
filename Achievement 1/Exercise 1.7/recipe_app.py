from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Integer, String, Column

# Create an engine object
engine = create_engine("mysql://cf-python:password@localhost/my_database")
# Create a connection object


# Base is a class from which all mapped classes should inherit
Base = declarative_base()


# Create a sessionmaker object that connects to the database
Session = sessionmaker(bind=engine)
session = Session()


# Create a Recipe class that inherits from Base
class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return (
            "<Recipe ID: "
            + str(self.id)
            + ", name: "
            + self.name
            + ", difficulty: "
            + self.difficulty
            + ">"
        )

    def __str__(self):
        return f"""
        Name: {self.name}
        Ingredients: {self.ingredients}
        Cooking Time: {self.cooking_time} minutes
        {self.difficulty}
        """


# This creates the table
Base.metadata.create_all(engine)


# Create a function that calculates the difficulty of a recipe based on its cooking time and ingredients
def calc_difficulty(cooking_time, ingredients):
    difficulty_levels = {
        "Easy": "Easy 😄",
        "Medium": "Medium 😅",
        "Intermediate": "Intermediate 😓",
        "Hard": "Hard 😰",
    }

    if (cooking_time < 10) and (len(ingredients) < 4):
        difficulty = "Easy"
    elif (cooking_time < 10) and (len(ingredients) >= 4):
        difficulty = "Medium"
    elif (cooking_time >= 10) and (len(ingredients) < 4):
        difficulty = "Intermediate"
    elif (cooking_time >= 10) and (len(ingredients) >= 4):
        difficulty = "Hard"
    else:
        print("Something bad happened, please try again")

    return difficulty_levels.get(difficulty)


def create_recipe():
    """
    This function creates a new recipe by prompting the user for the recipe name, cooking time, number of ingredients,
    and the name of each ingredient. It then calculates the recipe's difficulty level and saves the recipe to the database.
    """
    # Initialize an empty list to store the ingredients
    ingredients = []

    # Prompt the user for the recipe name and cooking time
    name = str(input("Enter the name of the recipe: ").title().strip())
    while True:
        cooking_time = input("Enter the cooking time (minutes): ")
        if cooking_time.isnumeric():
            cooking_time = int(cooking_time)
            break
        else:
            print("Invalid input. Please try again.")

    # Prompt the user for the number of ingredients
    while True:
        num_ingredients = input("Enter the number of ingredients: ")
        if num_ingredients.isnumeric():
            num_ingredients = int(num_ingredients)
            break
        else:
            print("Invalid input. Please try again.")

    # Prompt the user for the name of each ingredient and add it to the ingredients list
    for i in range(num_ingredients):
        ingredient = (
            input(f"Enter an ingredient ({i+1}/{num_ingredients}): ").title().strip()
        )
        ingredients.append(ingredient)

    # Join the ingredients list into a comma-separated string
    recipe_ingredients = ", ".join(ingredients)

    # Calculate the recipe's difficulty level using the calc_difficulty function
    difficulty = calc_difficulty(cooking_time, recipe_ingredients)

    # Create a new Recipe object with the user's input and the calculated difficulty level
    recipe_entry = Recipe(
        name=name,
        cooking_time=cooking_time,
        ingredients=recipe_ingredients,
        difficulty=difficulty,
    )

    # Add the new recipe to the database and commit the changes
    session.add(recipe_entry)
    session.commit()

    # Print a confirmation message
    print("Recipe saved in the database.", recipe_entry)


def search_by_ingredients():
    """
    This function allows the user to search for recipes based on ingredients. It prompts the user to select one or more
    ingredients from a list of all ingredients in the database, and then returns a list of all recipes that contain
    those ingredients.
    """

    # Check if there are any recipes in the database
    if session.query(Recipe).count() == 0:
        print("There are no recipes in the database.")
        return None

    else:
        # Get a list of all ingredients in the database
        results = session.query(Recipe.ingredients).all()
        all_ingredients = []

        # Split the ingredients into individual strings and add them to a list
        for recipe_ingredients_list in results:
            for recipe_ingredients in recipe_ingredients_list:
                recipe_ingredients_split = recipe_ingredients.split(", ")
                all_ingredients.extend(recipe_ingredients_split)

        # Remove duplicates from the list of ingredients
        all_ingredients = list(dict.fromkeys(all_ingredients))

        # Create a list of tuples containing the index and name of each ingredient
        all_ingredients_list = list(enumerate(all_ingredients))

        # Print the list of all ingredients
        print("\nAll ingredients list:")
        print("------------------------")

        for index, tup in enumerate(all_ingredients_list):
            print(str(tup[0] + 1) + ". " + tup[1])

        try:
            # Prompt the user to select one or more ingredients from the list
            ingredient_searched_nber = input(
                "\nEnter the number corresponding to the ingredient you want \nto select from the above list. You can enter several numbers. \nIn this case, numbers shall be separated by a space: "
            )

            # Split the user's input into a list of ingredient numbers
            ingredients_nber_list_searched = ingredient_searched_nber.split(" ")

            # Create a list of the selected ingredients
            ingredient_searched_list = []
            for ingredient_searched_nber in ingredients_nber_list_searched:
                ingredient_searched_index = int(ingredient_searched_nber) - 1
                ingredient_searched = all_ingredients_list[ingredient_searched_index][1]

                ingredient_searched_list.append(ingredient_searched.strip())

            # Print the list of selected ingredients
            print(
                "\nHere are the recipes for the following ingredient(s): ",
                ingredient_searched_list,
            )

            # Create a list of conditions to search for recipes containing the selected ingredients
            conditions = []
            for ingredient in ingredient_searched_list:
                like_term = "%" + ingredient + "%"
                condition = Recipe.ingredients.like(like_term)
                conditions.append(condition)

            # Query the database for recipes containing the selected ingredients
            searched_recipes = session.query(Recipe).filter(*conditions).all()

        except:
            print(
                "An unexpected error occurred. Make sure to select a number from the list."
            )

        else:
            # Print the list of recipes containing the selected ingredients
            for recipe in searched_recipes:
                print(recipe)


def edit_recipe():
    """
    Allows the user to edit a recipe in the database by selecting the recipe ID and the column to update.
    The user can update the name, cooking time, or ingredients of the recipe.
    The function calculates the updated difficulty of the recipe based on the new cooking time and ingredients.
    """

    # Check if there are any recipes in the database
    if session.query(Recipe).count() == 0:
        print("There are no recipes in the database.")
        return None
    else:
        # Display a list of available recipes
        results = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()
        print("\nList of available recipes: ")
        for recipe in results:
            print("\nId: ", recipe[0])
            print("Name: ", recipe[1])

        # Prompt the user to select a recipe ID to edit
        recipe_id_for_edit = int(
            (input("\nEnter the id of the recipe you want to edit: "))
        )

        # Get a list of all recipe IDs in the database
        recipes_id_tup_list = session.query(Recipe).with_entities(Recipe.id).all()
        recipes_id_list = []
        for recipe_tup in recipes_id_tup_list:
            recipes_id_list.append(recipe_tup[0])

        # Check if the selected recipe ID is in the list of recipe IDs
        if recipe_id_for_edit not in recipes_id_list:
            print("Not in the ID list, please try again later.")
        else:
            print("Ok you can continue")

            # Get the recipe object to edit
            recipe_to_edit = (
                session.query(Recipe).filter(Recipe.id == recipe_id_for_edit).one()
            )

            # Display a warning message with the recipe to edit
            print("\nWARNING: You are about to edit the following recipe: ")
            print(recipe_to_edit)

            # Prompt the user to select a column to update
            print("\n1. Name")
            print("2. Cooking Time")
            print("3. Ingredients")
            column_for_update = int(
                input(
                    "\nPlease enter the corresponding number for what you want to update: "
                )
            )

            # Update the name of the recipe
            if column_for_update == 1:
                print("You want to update the name of the recipe")
                updated_value = input("\nEnter the new name for the recipe: ")
                session.query(Recipe).filter(Recipe.id == recipe_id_for_edit).update(
                    {Recipe.name: updated_value}
                )
                session.commit()

            # Update the cooking time of the recipe
            elif column_for_update == 2:
                print("You want to change the cooking time of the recipe")
                updated_value = input("\nEnter the new cooking time for the recipe: ")
                session.query(Recipe).filter(Recipe.id == recipe_id_for_edit).update(
                    {Recipe.cooking_time: updated_value}
                )
                session.commit()

            # Update the ingredients of the recipe
            elif column_for_update == 3:
                print("You have updated the ingredients of the recipe")

                # Collect the updated ingredients from the user
                updated_ingredients = []
                num_updated_ingredients = input("Enter the number of ingredients: ")
                if num_updated_ingredients.isnumeric():
                    num_updated_ingredients = int(num_updated_ingredients)
                else:
                    print("Invalid input. Please try again.")
                for i in range(num_updated_ingredients):
                    updated_ingredient = (
                        input(
                            f"Enter an ingredient ({i + 1}/{num_updated_ingredients}): "
                        )
                        .title()
                        .strip()
                    )
                    updated_ingredients.append(updated_ingredient)

                # Convert the updated ingredients list to a comma-separated string
                updated_value = ", ".join(updated_ingredients)

                # Update the recipe in the database
                session.query(Recipe).filter(Recipe.id == recipe_id_for_edit).update(
                    {Recipe.ingredients: updated_value}
                )
                session.commit()

            else:
                print("Wrong input, please try again.")

            # Calculate the updated difficulty of the recipe based on the new cooking time and ingredients
            updated_difficulty = calc_difficulty(
                recipe_to_edit.cooking_time, recipe_to_edit.ingredients
            )
            print("updated_difficulty: ", updated_difficulty)

            # Update the difficulty of the recipe in the database
            recipe_to_edit.difficulty = updated_difficulty
            session.commit()

            print("Modification done.")


def view_all_recipes():
    """
    This function retrieves all recipes from the database and prints them to the console.
    If there are no recipes in the database, it prints a message indicating so.
    """
    all_recipes = []
    all_recipes = session.query(Recipe).all()

    if len(all_recipes) == 0:
        print("There are no recipes in the database.")
        return None
    else:
        print("\nAll recipes:")
        print("------------------------")

        for recipe in all_recipes:
            print(recipe)


def delete_recipe():
    """
    This function deletes a recipe from the database by taking the recipe id as input from the user.
    If there are no recipes in the database, it prints a message and returns None.
    If the recipe id entered by the user is not in the list of available recipe ids, it prints a message and returns None.
    If the recipe id entered by the user is in the list of available recipe ids, it prompts the user for confirmation to delete the recipe.
    If the user confirms the deletion, the recipe is deleted from the database and a message is printed.
    If the user does not confirm the deletion, a message is printed and the recipe is not deleted.
    """
    if session.query(Recipe).count() == 0:
        print("There are no recipes in the database.")
        return None
    else:
        results = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()

        print("\nList of available recipes: ")
        for recipe in results:
            print("\nId: ", recipe[0])
            print("Name: ", recipe[1])

        recipe_id_for_delete = int(
            (input("\nEnter the id of the recipe you want to delete: "))
        )

        recipes_id_tup_list = session.query(Recipe).with_entities(Recipe.id).all()
        recipes_id_list = []

        for recipe_tup in recipes_id_tup_list:
            recipes_id_list.append(recipe_tup[0])

        if recipe_id_for_delete not in recipes_id_list:
            print("Not in the ID list, please try again later.")
        else:
            print("Ok you can continue")

            recipe_to_delete = (
                session.query(Recipe).filter(Recipe.id == recipe_id_for_delete).one()
            )

            print("\nWARNING: You are about to delete the following recipe: ")
            print(recipe_to_delete)

            delete_confirmation = input(
                "\nAre you sure you want to delete this recipe? (y/n): "
            )

            if delete_confirmation == "y":
                session.delete(recipe_to_delete)
                session.commit()
                print("Recipe deleted.")
            elif delete_confirmation == "n":
                print("Recipe not deleted.")
            else:
                print("Invalid input. Please try again.")


def main_menu():
    while True:
        print("\nWelcome to the Recipe Database!")
        print("================================")
        print("\nMain Menu")
        print("================================")
        print("\nWhat would you like to do? Pick a choice!")
        print("1. Create a recipe")
        print("2. Search for a recipe by ingredient")
        print("3. Update an existing recipe")
        print("4. Delete a recipe")
        print("5. View all recipes")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_recipe()
        elif choice == "2":
            search_by_ingredients()
        elif choice == "3":
            edit_recipe()
        elif choice == "4":
            delete_recipe()
        elif choice == "5":
            view_all_recipes()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")


main_menu()
session.close()
