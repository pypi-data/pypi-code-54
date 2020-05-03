"""
Income Threshold   Rate     PAYE
14000               10.5    1470
48000               17.5    5950
70000               30      6600
70000+              33      x
"""
from nzpaye.exception import ArgumentError

summary = {}
INCOME_THRESHOLD_A = 14000
INCOME_THRESHOLD_B = 48000
INCOME_THRESHOLD_C = 70000
HOURS_IN_A_WEEK = 40
WEEKS_IN_A_YEAR = 52
GST_RATE = 0.15

def validate_params(hourly_rate, hours_worked, witholding_tax):
    if hours_worked <= 0:
        raise ArgumentError("Enter a valid value for hours worked")
    if hourly_rate <= 0 :
        raise ArgumentError("Enter a valid value for hourly rate")
    if not(witholding_tax == 10 or witholding_tax == 20):
        raise ArgumentError("Enter a valid value for witholding tax")
    return True

def income_summary(hourly_rate, hours_worked, witholding_tax=10):
    # assuming working each week for 40 hours each year
    validate_params(hourly_rate, hours_worked, witholding_tax)
    yearly_income = hourly_rate * HOURS_IN_A_WEEK * WEEKS_IN_A_YEAR
    yearly_paye = calculate_yearly_paye(yearly_income)

    hourly_paye = yearly_paye / (WEEKS_IN_A_YEAR * HOURS_IN_A_WEEK)

    #assuming gst is 15%
    hourly_gst = GST_RATE * hourly_rate

    total_income = hours_worked * hourly_rate
    total_paye = hours_worked * hourly_paye
    less_witholding_tax = (witholding_tax/100) * total_income
    plus_gst = hours_worked * hourly_gst
    paid_to_account = total_income - less_witholding_tax + plus_gst
    remaining_paye_to_be_paid = (hours_worked * hourly_paye) - less_witholding_tax
    remaining_gst_and_paye_to_be_paid = plus_gst + remaining_paye_to_be_paid
    disposable_income = paid_to_account - remaining_gst_and_paye_to_be_paid

    summary['hours_worked'] = str(hours_worked)
    summary['total_income'] = format(total_income, '.2f')
    summary['total_paye'] = format(total_paye, '.2f')
    summary['less_witholding_tax'] = format(less_witholding_tax, '.2f')
    summary['plus_gst'] = format(plus_gst, '.2f')
    summary['paid_to_account'] = format(paid_to_account, '.2f')
    summary['remaining_paye_to_be_paid'] = format(remaining_paye_to_be_paid, '.2f')
    summary['remaining_gst_and_paye_to_be_paid'] = format(remaining_gst_and_paye_to_be_paid, '.2f')
    summary['disposable_income'] = format(disposable_income, '.2f')

    return summary


def calculate_yearly_paye(yearly_income):
    yearly_paye = 0
    if yearly_income > 0 and yearly_income <= INCOME_THRESHOLD_A:
        yearly_paye = yearly_paye + (0.105 * yearly_income)

    if yearly_income > INCOME_THRESHOLD_A and yearly_income <= INCOME_THRESHOLD_B:
        yearly_paye = yearly_paye + 1470
        yearly_paye = yearly_paye + (0.175 * (yearly_income - INCOME_THRESHOLD_A))

    yearly_paye = check_and_apply_ietc(yearly_income, yearly_paye)

    if yearly_income > INCOME_THRESHOLD_B and yearly_income <= INCOME_THRESHOLD_C:
        yearly_paye = yearly_paye + 1470 + 5950
        yearly_paye = yearly_paye + (0.3 * (yearly_income - INCOME_THRESHOLD_B))

    if yearly_income > INCOME_THRESHOLD_C:
        yearly_paye = yearly_paye + 1470 + 5950 + 6600
        yearly_paye = yearly_paye + (0.33 * (yearly_income - INCOME_THRESHOLD_C))

    return round(yearly_paye, 2)


def check_and_apply_ietc(yearly_income, yearly_paye):
    if yearly_income >= 24000 and yearly_income <= 44000:
        yearly_paye = yearly_paye - 520
    if yearly_income > 44000 and yearly_income <= 48000:
        yearly_paye = yearly_paye - (520 - (0.13 * (yearly_income - 44000)))
    return yearly_paye