import json
Input = r"PagingInput"
file = open(Input , "r")

command = []
for line in file:
    if line.startswith("Dump:"):
        #print(line[5:])
        command.append(line[5:])
for i in command:
    i = i.strip(" ")
    i = i.strip("\n")
    notepad = open(r"C:\Users\rsingh\Documents\GitHub\Cets-Developement\output\%s" % i, "w")
    #notepad = open(r"C:\Users\rsingh\Documents\GitHub\Cets-Developement\output\%s" % i, "a")
    notepad.write(("############################################# \n##\n## TOOL: CETS - CMM ELEMENT TROUBLESHOOTING \n## Version: 2.4\n## Local Time: Tue Aug 27 12:50:36 IST 2019\n## UTC: Tue Aug 27 07:20:36 UTC 2019\n## COMMAND: {0} \n##\n#############################################\n\n\n~~~~~~~~~~~~~~~~~~~~START~~~~~~~~~~~~~~~~~~~~").format(i))

file1 = open(Input , "r")

for line in file1:
    if line.startswith("{"):
        liner = line.replace("false" , '"False"')
        a = json.loads(liner)
        for clas in a:
            #print("\n"+clas+"\n")
            extract_file = open(r"C:\Users\rsingh\Documents\GitHub\Cets-Developement\output\%s" % clas, "a")
            extract_file.write("\n")
            for i,j in a[clas].items():
                extract_file.write("\n")
                extract_file.write("{0} : {1}".format(i, j))
