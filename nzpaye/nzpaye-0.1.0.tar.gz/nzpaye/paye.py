"""
Income Threshold   Rate     PAYE
14000               10.5    1470
48000               17.5    5950
70000               30      6600
70000+              33      x
"""
from nzpaye.exception import ArgumentError

summary = {}

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
    yearly_income = hourly_rate * 40 * 52
    remaining_paye = (33 / 100) * (yearly_income - 70000)
    yearly_paye = 1470 + 5950 + 6600 + remaining_paye
    hourly_paye = yearly_paye / (52 * 40)

    #assuming gst is 15%
    hourly_gst = 0.15 * hourly_rate

    total_income = hours_worked * hourly_rate
    less_witholding_tax = (witholding_tax/100) * total_income
    plus_gst = hours_worked * hourly_gst
    paid_to_account = total_income - less_witholding_tax + plus_gst
    remaining_paye_to_be_paid = (hours_worked * hourly_paye) - less_witholding_tax
    remaining_gst_and_paye_to_be_paid = plus_gst + remaining_paye_to_be_paid
    disposable_income = paid_to_account - remaining_gst_and_paye_to_be_paid

    summary['hours_worked'] = str(hours_worked)
    summary['total_income'] = format(total_income, '.2f')
    summary['less_witholding_tax'] = format(less_witholding_tax, '.2f')
    summary['plus_gst'] = format(plus_gst, '.2f')
    summary['paid_to_account'] = format(paid_to_account, '.2f')
    summary['remaining_paye_to_be_paid'] = format(remaining_paye_to_be_paid, '.2f')
    summary['remaining_gst_and_paye_to_be_paid'] = format(remaining_gst_and_paye_to_be_paid, '.2f')
    summary['disposable_income'] = format(disposable_income, '.2f')

    return summary