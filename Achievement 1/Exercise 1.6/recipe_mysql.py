import mysql.connector

conn = mysql.connector.connect(host="localhost", user="cf-python", passwd="password")
cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

cursor.execute("USE task_database")

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS recipes (
        id INT NOT NULL  PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(50),
        ingredients VARCHAR(255),
        cooking_time INT,
        difficulty VARCHAR(20)
    )
    """
)


# Allow user to create a recipe
def create_recipe(conn, cursor):
    recipe_ingredients = []
    name = str(input("Enter the name of the recipe: ").title())
    cooking_time = int(input("Enter the cooking time (minutes): "))
    ingredients_input = input("Enter the ingredients: ")
    # Capitalize each ingredient and remove any whitespace
    ingredients = ", ".join(
        [ingredient.strip().capitalize() for ingredient in ingredients_input.split(",")]
    )

    difficulty = calc_difficulty(cooking_time, ingredients)

    recipe_ingredients.append(ingredients)
    recipe_ingredients_str = ", ".join(recipe_ingredients)

    sql = "INSERT INTO recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)"
    val = (name, recipe_ingredients_str, cooking_time, difficulty)

    try:
        cursor.execute(sql, val)
        conn.commit()
        print("Recipe saved in database.")
    except mysql.connector.Error as err:
        print("Error", err)


# Calculate the difficulty of the recipe
def calc_difficulty(cooking_time, ingredients):
    print("Run the calc_difficulty with: ", cooking_time, ingredients)

    if cooking_time < 10:
        difficulty = "Easy"
    elif (cooking_time < 10) and (len(ingredients) >= 4):
        difficulty = "Medium"
    elif (cooking_time >= 10) and (len(ingredients) < 4):
        difficulty = "Intermediate"
    elif (cooking_time >= 10) and (len(ingredients) >= 4):
        difficulty = "Hard"
    else:
        print("Something bad happened, please try again")

    print("Difficulty level: ", difficulty)
    return difficulty


# Allow user to search for a recipe
def search_recipe(conn, cursor):
    # This prevents duplicate ingredients from being displayed
    unique_ingredients = set()
    all_ingredients = []
    # Get all ingredients from database
    cursor.execute("SELECT ingredients FROM recipes")
    results = cursor.fetchall()
    # This is a list of tuples, so we need to iterate through each tuple
    for recipe in results:
        # Each tuple contains a string of ingredients, so we need to split the string
        for recipe_ingredients in recipe:
            recipe_ingredients = recipe_ingredients.split(", ")
            # Add each ingredient to the all_ingredients list
            unique_ingredients.update(recipe_ingredients)
    # Convert the set to a list
    all_ingredients_list = list(enumerate(unique_ingredients))
    print("\nAll ingredients list:")
    print("------------------------")
    print(all_ingredients_list)
    try:
        searched_ingredients = int(
            input(
                "\nEnter the number corresponding to the ingredient you want to search for: "
            )
        )
        searched_ingredients = all_ingredients_list[searched_ingredients][1]
        print("\nRecipes containing", searched_ingredients, ":")
    except:
        print("Invalid input. Please try again.")

    cursor.execute(
        "SELECT * FROM recipes WHERE ingredients LIKE %s",
        ("%" + searched_ingredients + "%",),
    )
    results = cursor.fetchall()

    for recipe in results:
        print("\nRecipe ID:", recipe[0])
        print("Name:", recipe[1])
        print("Ingredients:", recipe[2])
        print("Cooking time:", recipe[3], "minutes")
        print("Difficulty:", recipe[4])


def update_recipe(conn, cursor):
    # Get all recipes from database
    view_all_recipes(conn, cursor)
    recipe_id = int(input("\nEnter the ID of the recipe you want to update: "))

    # Gets the recipes ID
    cursor.execute("SELECT name FROM recipes WHERE id = %s", (recipe_id,))
    result = cursor.fetchone()

    # handle errors
    if result is None:
        print("Recipe with ID %s does not exist." % recipe_id)
        return
    recipe_name = result[0]

    print("\n1. Name")
    print("2. Ingredients")
    print("3. Cooking Time")
    column_update = int(
        input(
            "\nEnter a number associated with what you want to update in %s."
            % recipe_name
        )
    )

    # Update the name of the recipe
    if column_update == 1:
        new_name = str(input("\nEnter the new name: ").title())
        sql = "UPDATE recipes SET name = %s WHERE id = %s"
        val = (new_name, recipe_id)
        cursor.execute(sql, val)
        conn.commit()
        print("Recipe updated successfully.")

    # Update the ingredients of the recipe
    elif column_update == 2:
        # Ask user for new ingredients
        ingredients_input = input("Enter the new ingredients for %s : " % recipe_name)

        # Capitalize each ingredient and remove any whitespace
        new_ingredients = ", ".join(
            [ingredient.strip().title() for ingredient in ingredients_input.split(",")]
        )

        # Update the ingredients in the database
        sql = "UPDATE recipes SET ingredients = %s WHERE id = %s"
        val = (new_ingredients, recipe_id)
        cursor.execute(sql, val)

        # Update the difficulty in the database
        cursor.execute("SELECT cooking_time FROM recipes WHERE id = %s", (recipe_id,))
        result = cursor.fetchone()
        current_cooking_time = result[0]
        # result is the current cooking time
        new_difficulty = calc_difficulty(current_cooking_time, new_ingredients)
        sql = "UPDATE recipes SET difficulty = %s WHERE id = %s"
        val = (new_difficulty, recipe_id)
        cursor.execute(sql, val)
        conn.commit()
        print("Recipe updated and difficulty calculated.")
    elif column_update == 3:
        # Ask user for new cooking time
        new_cooking_time = int(input("\nEnter the new cooking time (in minutes): "))
        sql = "UPDATE recipes SET cooking_time = %s WHERE id = %s"
        val = (new_cooking_time, recipe_id)
        cursor.execute(sql, val)

        # Update the difficulty in the database
        cursor.execute("SELECT ingredients FROM recipes WHERE id = %s", (recipe_id,))
        result = cursor.fetchone()
        current_ingredients = result[0]
        new_difficulty = calc_difficulty(new_cooking_time, current_ingredients)
        sql = "UPDATE recipes SET difficulty = %s WHERE id = %s"
        val = (new_difficulty, recipe_id)
        cursor.execute(sql, val)
        conn.commit()
        print("Recipe updated successfully.")
    else:
        print("Invalid input. Please try again.")


def delete_recipe(conn, cursor):
    view_all_recipes(conn, cursor)
    recipe_id = int(input("\nEnter the ID of the recipe you want to delete: "))
    sql = "DELETE FROM recipes WHERE id = %s"
    val = (recipe_id,)
    cursor.execute(sql, val)
    conn.commit()


def view_all_recipes(conn, cursor):
    print("\nAll recipes can be found below:")
    print("--------------------------------")

    cursor.execute("SELECT * FROM recipes")
    results = cursor.fetchall()
    for row in results:
        print("\nID: ", row[0])
        print("Name: ", row[1])
        print("Ingredients: ", row[2])
        print("Cooking Time: ", row[3])
        print("Difficulty: ", row[4])


def main_menu(conn, cursor):
    while True:
        print("\nWelcome to the Recipe Database!")
        print("================================")
        print("\nMain Menu")
        print("================================")
        print("\nWhat would you like to do? Pick a choice!")
        print("1. Create a recipe")
        print("2. Search for a recipe")
        print("3. Update a recipe")
        print("4. Delete a recipe")
        print("5. View all recipes")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_recipe(conn, cursor)
        elif choice == "2":
            search_recipe(conn, cursor)
        elif choice == "3":
            update_recipe(conn, cursor)
        elif choice == "4":
            delete_recipe(conn, cursor)
        elif choice == "5":
            view_all_recipes(conn, cursor)
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")


main_menu(conn, cursor)
print("Goodbye!")
