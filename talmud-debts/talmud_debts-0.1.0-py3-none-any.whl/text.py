### Talmud Debts Function
def debts(Estate, Debt_arr):
    from collections import OrderedDict

    #   # Helper Functions
    ## Generate Functions for adding to dictionary
    def add_one(d):
        for key, value in d.items():
            d[key] += 1 
        return(d)

    def add_float(d, remaining, creditors):
        percentage = remaining/float(creditors)
        for key, value in d.items():
            d[key] += percentage 
        return(d)


    def getKeysByValues(d, value):
        keys = list()
        items = d.items()
        for item in items:
            if item[1] == value:
                keys.append(item[0])
                
        return(keys)

    
    ## Order the debts from lowest to highest
    Debt_arr.sort()

    ## Divide the Estate equally among all parties until lowest creditor recieve 1/2 of claim
    Number_of_Creditors = len(Debt_arr)
    Amount_of_Debts = sum(Debt_arr)
    if Estate >= Amount_of_Debts:
        #print("Enough in Estate for all debts")
        return("Enough in Estate for all debts")


    ## Assign equally until lower receives half
    Amount_Recieved = OrderedDict()
    for i, x in enumerate(Debt_arr):
        Creditor = Debt_arr[i]
        Amount_Recieved[str(i)+'_'+str(Creditor)] = 0



    Creditor_Payout = Amount_Recieved.copy()

    for item in range(len(Creditor_Payout)):
        while True:
            if Estate <= 0:
                break
            if Estate < len(Amount_Recieved):
                add_float(Amount_Recieved, Estate, len(Amount_Recieved))
                Estate = 0
                break
            else:
                s = list(Amount_Recieved)
                if Amount_Recieved.get(s[0]) > (float(s[0].split("_")[1])/2)-1:
                    break
                Estate -= len(Amount_Recieved)
                add_one(Amount_Recieved)
        
        Creditor_Payout.update(Amount_Recieved)
        q = Amount_Recieved.popitem(last=False)
    
    ## Give highest claim until loss equals loss of next highest claim
    while True:
        if Estate <= 0:
            print("Estate is empty")
            break
        else:
            values = []
            loss_values = dict()
            for key, value in Creditor_Payout.items():
                values.append(int(key.split("_")[1])-value)
                loss_values[key] = int(key.split("_")[1])-value

            values = list(set(values))
            greatest_loss = values[-1]
            if len(values) > 1:
                second_loss = values[-2]
                difference = greatest_loss - second_loss
                loss_duplicates = sum(x == greatest_loss for x in loss_values.values())
                diff_amount = difference*loss_duplicates
                if Estate-diff_amount>=0:
                    ## Update to make losses of highest equal to second highest
                    x = getKeysByValues(loss_values, greatest_loss)
                    for item in x:
                        Creditor_Payout[item] += difference
                        Estate -= difference
                else:
                    ## Update when by one so losses are equal
                    wanted_keys = getKeysByValues(loss_values, greatest_loss)
                    Amount_Recieved = dict((k, Creditor_Payout[k]) for k in wanted_keys if k in Creditor_Payout)
                    while True:
                        if Estate < len(Amount_Recieved):
                            add_float(Amount_Recieved, Estate, len(Amount_Recieved))
                            Estate = 0
                            break
                        else:
                            s = list(Amount_Recieved)
                            Estate -= len(Amount_Recieved)
                            add_one(Amount_Recieved)
                        
                    Creditor_Payout.update(Amount_Recieved)
                    break       
            else:
                ## Update when all losses are equal
                wanted_keys = getKeysByValues(loss_values, greatest_loss)
                Amount_Recieved = dict((k, Creditor_Payout[k]) for k in wanted_keys if k in Creditor_Payout)
                while True:
                    if Estate < len(Amount_Recieved):
                        add_float(Amount_Recieved, Estate, len(Amount_Recieved))
                        Estate = 0
                        break
                    else:
                        s = list(Amount_Recieved)
                        Estate -= len(Amount_Recieved)
                        add_one(Amount_Recieved)
                            
                Creditor_Payout.update(Amount_Recieved)
                break

    return(Creditor_Payout)
