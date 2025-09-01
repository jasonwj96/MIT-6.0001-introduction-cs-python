total_cost = 1000000
portion_down_payment = 0.25
down_payment = total_cost * portion_down_payment
annual_return = 0.04
semi_annual_raise = 0.07
months = 36
epsilon = 100

starting_salary = float(input("Enter the starting salary: "))

def savings_after_36_months(savings_rate, salary):
    monthly_salary = salary / 12.0
    savings = 0.0
    current_salary = monthly_salary
    for month in range(1, months + 1):
        savings += savings * (annual_return / 12)
        savings += current_salary * (savings_rate / 10000.0)
        if month % 6 == 0:
            current_salary *= (1 + semi_annual_raise)
    return savings

low = 0
high = 10000
steps = 0
best_rate = None

if savings_after_36_months(10000, starting_salary) < down_payment:
    print("It is not possible to pay the down payment in three years.")
else:
    while low <= high:
        steps += 1
        mid = (low + high) // 2
        current_savings = savings_after_36_months(mid, starting_salary)
        if abs(current_savings - down_payment) <= epsilon:
            best_rate = mid / 10000.0
            break
        elif current_savings < down_payment:
            low = mid + 1
        else:
            high = mid - 1
    print("Best savings rate:", best_rate)
    print("Steps in bisection search:", steps)