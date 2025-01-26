# def fibonacci_series(n):
#     a, b = 0, 1
#     series = []

#     for _ in range(n):
#         series.append(a)
#         a, b = b, a + b

#     return series

# terms = int(input("Enter the number of terms: "))
# print("Fibonacci series:", fibonacci_series(terms))

num = int(input("Enter the number of terms: "))

a = 0
b = 1
fibonacci_series = []

for i in range(num):
    fibonacci_series.append(a)
    a, b = b, a + b

print(fibonacci_series)

# find ascii value
a = "g"

print(ord(a))
