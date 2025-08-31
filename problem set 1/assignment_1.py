portion_down_payment = 0.25
current_savings = 0.0
r = 0.04  # annual investment return

annual_salary = float(input("Enter your annual salary:\n"))
portion_saved = float(input("Enter the portion of salary to be saved:\n"))
total_cost = float(input("Enter the house cost:\n"))

monthly_salary = annual_salary / 12
down_payment = total_cost * portion_down_payment

number_of_months = 0
while current_savings < down_payment:
    current_savings += current_savings * (r / 12)
    current_savings += monthly_salary * portion_saved
    number_of_months += 1

print(f"Number of months: {number_of_months}")
