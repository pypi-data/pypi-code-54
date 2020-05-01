
day = 24
minets = 60
month = 30
#input for moeny
money_get_in = input("how much money earned montly:")
float(money_get_in)
#input for how much money get by walebeing
money_get_out_life = input('how much money you spent on living a month:')
float(money_get_out_life)
#input how much money you want to save
money_saved_a_month = input("how much money are you wanting to save a month:")
float(money_saved_a_month)
# making a trantision from stg to int or float


#math
money_sum = float(money_get_in) - (float(money_get_out_life) + float(money_saved_a_month))
print("thats how much money your have to spent for a month after your saving money")
print(money_saved_a_month)

#day math
money_a_day = money_sum/month
print("thats how much money you have for a day:")
print(money_a_day)