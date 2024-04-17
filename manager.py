import sqlite3
import sys

connection = sqlite3.connect("recipes.db")
db = connection.cursor()


def main():
    selection = options()

    if selection == 1:
        input_recipe()
        connection.commit()
    elif selection == 2:
        output_recipe()
    else:
        sys.exit()


# Ask whether inputting/outputting recipe
def options():
    while True:
        try:
            print("1: Input Recipe")
            print("2: Output Recipe")
            print("3: Exit")

            n = int(input("Selection: "))

            # Make sure input valid
            if n < 1 or n > 3:
                raise ValueError
            else:
                break
        except ValueError:
            pass
        
    return n


# Get input for new recipe to be entered to db
def input_recipe():
    while True:
        try:
            # Get recipe info
            name = input("\nRecipe Name: ").lower().strip()
            cook_time = int(input("Cooking Time (minutes): "))
            serving_size = int(input("Serving Size (one number only): "))

            # Input into table
            db.execute("INSERT INTO recipes (name, cooking_time, serving_size) VALUES (?, ?, ?)", (name, cook_time, serving_size))
            break
        except ValueError:
            pass
        
    while True:
        try:
            ingredients = int(input("\n# of Ingredients: "))
            recipe_id = db.execute("SELECT id FROM recipes WHERE name = ?", (name,)).fetchone()[0]

            # Get every ingredient
            for i in range(ingredients):
                ingredient = input("\nIngredient Name: ")
                quantity = input("Quantity: ")
                
                # Input into table
                db.execute("INSERT INTO ingredients (name, quantity, recipe_id) VALUES (?, ?, ?)", (ingredient, quantity, recipe_id))
            break
        except ValueError:
            pass

    while True:
        try:
            steps = int(input("\n# of Steps: "))

            # Get every step
            for i in range(steps):
                step_number = input("\nStep Number: ")
                instruction = input("Instruction: ")
                
                # Input into table
                db.execute("INSERT INTO instructions (step_number, instruction, recipe_id) VALUES (?, ?, ?)", (step_number, instruction, recipe_id))
            break
        except ValueError:
            pass 


# Output recipe formatted
def output_recipe():
    while True:
        try:
            name = input("\nRecipe Name: ").lower().strip()
            recipe_id = db.execute("SELECT id FROM recipes WHERE name = ?", (name,)).fetchone()[0]

            break
        except TypeError:
            pass
    
    cook_time = db.execute("SELECT cooking_time FROM recipes WHERE name = ?", (name,)).fetchone()[0]
    serving_size = db.execute("SELECT serving_size FROM recipes WHERE name = ?", (name,)).fetchone()[0]
    
    print(f"\nCooking Time: {cook_time} minutes")
    print(f"Serving Size: {serving_size}")

    ingredients = db.execute("SELECT * FROM ingredients WHERE recipe_id = ?", (recipe_id,))

    print("\nIngredients: \n")

    for ingredient in ingredients:
        ingredient_name = ingredient[1]
        quantity = ingredient[2]

        print(f"{quantity} of {ingredient_name}")

    instructions = db.execute("SELECT * FROM instructions WHERE recipe_id = ?", (recipe_id,))

    print("\nInstructions: \n")

    for step in instructions:
        step_number = step[1]
        instruction = step[2]

        print(f"{step_number}. {instruction}")

if __name__ == "__main__":
    main()