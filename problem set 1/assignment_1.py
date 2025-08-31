portion_down_payment = 0.25
current_savings = 0.0
r = 0.04  # annual investment return

# annual_salary = float(input("Enter your annual salary:\n"))
# portion_saved = float(input("Enter the portion of salary to be saved:\n"))
# total_cost = float(input("Enter the house cost:\n"))
# semi_annual_raise = float(input("Enter the semi annual raise:\n"))

annual_salary = 80000
portion_saved = 0.10
total_cost = 800000
semi_annual_raise = 0.03

monthly_salary = annual_salary / 12
down_payment = total_cost * portion_down_payment

number_of_months = 0
while current_savings < down_payment:
    if number_of_months > 0 and number_of_months % 6 == 0:
        annual_salary += annual_salary * semi_annual_raise
        monthly_salary = annual_salary / 12

    current_savings += current_savings * (r / 12)
    current_savings += monthly_salary * portion_saved
    number_of_months += 1

print(f"Number of months: {number_of_months}")
