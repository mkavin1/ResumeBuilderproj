# Basic Python Script

# Variables
name = "Alice"
age = 25
is_student = True

# Function to greet a person
def greet(person_name):
    print(f"Hello, {person_name}!")

# Function to check if someone is an adult
def is_adult(person_age):
    if person_age >= 18:
        return True
    else:
        return False

# Loop through numbers 1 to 5
for i in range(1, 6):
    print(f"Number: {i}")

# Using the functions
greet(name)

# Check if the person is an adult
if is_adult(age):
    print(f"{name} is an adult.")
else:
    print(f"{name} is not an adult.")

# Working with lists
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(f"I like {fruit}.")
