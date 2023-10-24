class Animal():
    """Initializes class for animals"""

      # Class initializer. It has 5 custom parameters, with the
      # special `self` parameter that every method on a class
      # needs as the first parameter.
    def __init__(self, id, name, breed, status, customer_id, location_id):
        self.id = id
        self.name = name
        self.breed = breed
        self.status = status
        self.customer_id = customer_id
        self.location_id = location_id
        

# Classes are instantiated to create an object from its design
new_animal = Animal(1, "Snickers", "Dog", "Recreation", 1, 4)
