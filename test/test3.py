class MakeClass:
    def __init__(self, id, name, price, purchase_price):
        self.id = id
        self.name = name
        self.price = price
        self.purchase_price = purchase_price

    def calculate_profit(self):
        profit = self.price - self.purchase_price
        return profit

cool_tshirt = MakeClass("A0001", "Cool T-shirt", 5000, 2250)
print(cool_tshirt.calculate_profit())