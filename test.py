def calculate_total(price, quantity):
    total = price * quantity
    discount = 10
    total = total - discount
    return total


price = 20
quantity = 3

result = calculate_total(price, quantity)
print(result)