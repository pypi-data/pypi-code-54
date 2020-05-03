import json


file = open("redis-dump.log", "r")

'''list = []
for line in file:
    list.append(line)
file1 = json.dumps(list, separators= ",")
print(file1)'''

file1 = json.load(file)
t = []
for i,j in file1.items():
    #print(r"{%s : %s}" % (i, j), sep = "\n")

    if i.startswith("cmm."):
        l = i.partition(":")
        radis_parsed = open(r"C:\Users\rsingh\Documents\GitHub\Cets-Developement\output\%s" % l[0].replace("cmm.",""), "a")
        radis_parsed.write("\n")
        radis_parsed.write(i)
        for k,l in j.items():
            if type(l) is dict:
                for k, l in l.items():
                    radis_parsed.write("\n")
                    radis_parsed.write(r"%s : %s" % (k, l))
            radis_parsed.write("\n")
                    
    else:
        l = i.partition(".")
        m = ((l[2].partition("."))[0])
        radis_parsed = open(r"C:\Users\rsingh\Documents\GitHub\Cets-Developement\output\%s" % m, "a")
        radis_parsed.write("\n")
        radis_parsed.write(i)
        for k,l in j.items():
            if type(l) is dict:
                for k, l in l.items():
                    radis_parsed.write("\n")
                    radis_parsed.write(r"%s : %s" % (k, l))
        radis_parsed.write("\n")

            




    

