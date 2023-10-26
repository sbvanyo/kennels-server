import sqlite3
import json
from models import Animal, Location, Customer

ANIMALS = [
    {
        "id": 1,
        "name": "Snickers",
        "species": "Dog",
        "locationId": 1,
        "customerId": 4,
        "status": "Admitted"
    },
    {
        "id": 2,
        "name": "Roman",
        "species": "Dog",
        "locationId": 1,
        "customerId": 2,
        "status": "Admitted"
    },
    {
        "id": 3,
        "name": "Blue",
        "species": "Cat",
        "locationId": 2,
        "customerId": 1,
        "status": "Admitted"
    }
]

# def get_all_animals():
#     """Fetch all animals"""
#     return ANIMALS


# # Function with a single parameter
# def get_single_animal(id):
#     """Fetch single animal"""
#     # Variable to hold the found animal, if it exists
#     requested_animal = None

#     # Iterate the ANIMALS list above. Very similar to the
#     # for..of loops you used in JavaScript.
#     for animal in ANIMALS:
#         # Dictionaries in Python use [] notation to find a key
#         # instead of the dot notation that JavaScript used.
#         if animal["id"] == id:
#             requested_animal = animal

#     return requested_animal

# def create_animal(animal):
#     """Adds an animal to the list"""
#     # Get the id value of the last animal in the list
#     max_id = ANIMALS[-1]["id"]

#     # Add 1 to whatever that number is
#     new_id = max_id + 1

#     # Add an `id` property to the animal dictionary
#     animal["id"] = new_id

#     # Add the animal dictionary to the list
#     ANIMALS.append(animal)

#     # Return the dictionary with `id` property added
#     return animal

# def delete_animal(id):
#     """Removes an animal from the list"""
#     # Initial -1 value for animal index, in case one isn't found
#     animal_index = -1

#     # Iterate the ANIMALS list, but use enumerate() so that you
#     # can access the index value of each item
#     for index, animal in enumerate(ANIMALS):
#         if animal["id"] == id:
#             # Found the animal. Store the current index.
#             animal_index = index

#     # If the animal was found, use pop(int) to remove it from list
#     if animal_index >= 0:
#         ANIMALS.pop(animal_index)


# def update_animal(id, new_animal):
#     """Updates the value of a list item"""
#     # Iterate the ANIMALS list, but use enumerate() so that
#     # you can access the index value of each item.
#     for index, animal in enumerate(ANIMALS):
#         if animal["id"] == id:
#             # Found the animal. Update the value.
#             ANIMALS[index] = new_animal
#             break



def get_all_animals():
    """Fetches all animals"""
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
            SELECT
                a.id,
                a.name,
                a.breed,
                a.status,
                a.location_id,
                a.customer_id,
                l.name location_name,
                l.address location_address,
                c.name customer_name,
                c.address customer_address,
                c.email customer_email,
                c.password customer_password
            FROM Location l
            JOIN Animal a
                ON l.id = a.location_id
            JOIN Customer c
                ON a.customer_id = c.id
        """)

        # Initialize an empty list to hold all animal representations
        animals = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        for row in dataset:
            # Create an animal instance from the current row
            animal = Animal(row['id'], row['name'], row['breed'], row['status'],
                            row['customer_id'], row['location_id'])

            # Create a Location instance from the current row
            location = Location(row['id'], row['location_name'], row['location_address'])
            
            # Create a Location instance from the current row
            customer = Customer(row['id'], row['customer_name'], row['customer_address'], row['customer_email'], row['customer_password'])

            # Add the dictionary representation of the location to the animal
            animal.location = location.__dict__
            animal.customer = customer.__dict__

            # Add the dictionary representation of the animal to the list
            animals.append(animal.__dict__)

    return animals



def get_single_animal(id):
    """Fetches one animal"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.customer_id,
            a.location_id
        FROM animal a
        WHERE a.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        animal = Animal(data['id'], data['name'], data['breed'],
                            data['status'], data['customer_id'],
                            data['location_id'])

        return animal.__dict__




        
def get_animal_by_location_id(location_id):
    """Fetches the animal whose location id matches the location id passed in"""

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            c.id,
            c.name,
            c.breed,
            c.status,
            c.customer_id,
            c.location_id
        from Animal c
        WHERE c.location_id = ?
        """, ( location_id, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(row['id'], row['name'], row['breed'], row['status'] , row['customer_id'], row['location_id'])
            animals.append(animal.__dict__)

    return animals


def get_animal_by_status(status):
    """Fetches the animal whose location id matches the status passed in"""

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            c.id,
            c.name,
            c.breed,
            c.status,
            c.customer_id,
            c.location_id
        from Animal c
        WHERE c.status = ?
        """, ( status, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(row['id'], row['name'], row['breed'], row['status'] , row['customer_id'], row['location_id'])
            animals.append(animal.__dict__)

    return animals


def delete_animal(id):
    """Removes an animal from the list"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM animal
        WHERE id = ?
        """, (id, ))
        


def update_animal(id, new_animal):
    """Updates an animal row"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Animal
            SET
                name = ?,
                breed = ?,
                status = ?,
                customer_id = ?,
                location_id = ?
        WHERE id = ?
        """, (new_animal['name'], new_animal['breed'],
              new_animal['status'], new_animal['customer_id'],
              new_animal['location_id'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    # return value of this function
    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True


def create_animal(new_animal):
    """Adds new animal to the list"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Animal
            ( name, breed, status, customer_id, location_id )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_animal['name'], new_animal['breed'],
              new_animal['status'], new_animal['customerId'],
              new_animal['locationId'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_animal['id'] = id


    return new_animal
