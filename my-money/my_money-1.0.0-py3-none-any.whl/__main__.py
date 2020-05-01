from my_money.logic import calculate_monthly_free_sum
from my_money.presentation import get_input


def run_cli():

    monthly_salary = get_input("Enter your monthly income", type=float)
    monthly_out = get_input("Enter your monthly outcome", type=float)
    monthly_free = calculate_monthly_free_sum(monthly_salary, monthly_out)
    monthly_savings = get_input(f"Enter your monthly saving (Max available for saving: {monthly_free}): ",
                                type=float, max=monthly_free)

    money_sum = monthly_salary - (monthly_out + monthly_savings)
    print(f"money that is used for per day use that you need to keep:{money_sum}")
    month_time = 30
    money_per_day = money_sum/month_time
    print(f"money you can spent per day:{money_per_day}")


if __name__ == '__main__':
    run_cli()

