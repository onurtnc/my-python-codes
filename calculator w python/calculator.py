def calculate(a, op, b):
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        if b == 0:
            return "Error: cannot divide by 0!"
        return a / b
    if op == "**":
        return a ** b
    if op == "%":
        if b == 0:
            return "Error: cannot take modulo of 0!"
        return a % b
    return "Error: invalid operation!"

print("+========================+")
print("|   PYTHON CALCULATOR     |")
print("+========================+")
print("Operations: +  -  *  /  **  %")
print("Type 'q' to quit")

while True:
    op = input("\nChoose an operation (+,-,*,/,**,%) or q: ").strip()
    if op.lower() == "q":
        print("Exiting...")
        break

    try:
        a = float(input("1st number: "))
        b = float(input("2nd number: "))
    except ValueError:
        print("Error: please enter a number!")
        continue

    result = calculate(a, op, b)
    print("Result:", result)
