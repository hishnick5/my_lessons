number = int(input("Введите число "))
num_sum = 0

while number != 0:
    last_num = number % 10
    num_sum += last_num
    number //= 10

print("num", number, "sum", num_sum)
