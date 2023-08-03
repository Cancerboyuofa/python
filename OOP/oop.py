class Pizza:
    
    price = 12.99    

    def __init__(self, description, toppings, crust):
        self.descriptions = description
        self.toppings = toppings
        self.crust = crust
        

print(Pizza.price)

my_pizza = Pizza("Meat Lovers", ["Peperoni", "Sausage", "Ham"], "Chicago")

print(my_pizza.price)

Pizza.price = 13.99

print(my_pizza.price)

