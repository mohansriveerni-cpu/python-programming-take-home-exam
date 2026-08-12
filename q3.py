def scale_recipe(name, servings, *ingredients, unit="g", **options):
    if servings < 1:
        print(f"Error: servings must be at least 1 for {name}.")
        return 0

    print(f"\nShopping list: {name}")
    print(f"Servings: {servings}")

    result = {}

    for ingredient, amount in ingredients:
        scaled_amount = amount * servings
        result[ingredient] = scaled_amount

        print(f"{ingredient}: {scaled_amount}{unit}")

    if options:
        print("Cooking notes:")

        for key, value in options.items():
            print(f"{key}: {value}")

    return result


# Demo
if __name__ == "__main__":

    print(
        scale_recipe(
            "Pancakes",
            2,
            ("flour", 100),
            ("milk", 150),
            ("sugar", 20)
        )
    )

    print(
        scale_recipe(
            "Fresh Juice",
            3,
            ("orange juice", 200),
            ("water", 100),
            unit="ml"
        )
    )

    print(
        scale_recipe(
            "Chocolate Cake",
            4,
            ("flour", 100),
            ("sugar", 50),
            ("butter", 40),
            unit="g",
            oven="180C",
            time="45min"
        )
    )

    print(
        scale_recipe(
            "Invalid Recipe",
            0,
            ("flour", 100)
        )
    )
