bank = 0
stock = 0
stock_rate = 1.05
stock_sal = 200000
div_rate = 0.005
sal = 150000

for year in range(1, 11):
    stock += stock_sal
    for month in range(1, 13):
        transfer = stock * div_rate
        bank += transfer
        stock -= transfer
    bank += sal
    print("y%s %d %d %d" % (year, bank, stock, bank+stock))
    stock *= stock_rate
    stock_sal *= 1.1
    sal *= 1.05
