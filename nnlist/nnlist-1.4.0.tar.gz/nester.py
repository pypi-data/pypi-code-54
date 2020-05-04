#movies=['A', 'B', 'C', ['C1', 'C2'], 'D']

#recursive function - print items in nested list
def lol_1(the_list):
	for each_item in the_list:
		if isinstance(each_item):
			lol_1(each_item)
		else:
			print(each_item)
			
#Indent will be added for nested list:
def lol_2(the_list, level):
	for each_item in the_list:
		if isinstance(each_item, list):
			lol_2(each_item, level+1)
		else:
			for tab_stop in range(level):
				print("\t", end='')
			print(each_item)
			
#Indent level will be started from 0 by default:
def lol_3(the_list, level=0):
	for each_item in the_list:
		if isinstance(each_item, list):
			lol_3(each_item, level+1)
		else:
			for tab_stop in range(level):
				print("\t", end='')
			print(each_item)

#Indent will be off by default:			
def lol_4(the_list, indent=False, level=0):
	for each_item in the_list:
		if isinstance(each_item, list):
			lol_4(each_item, indent, level+1)
		else:
			if indent:
				for tab_stop in range(level):
					print("\t", end='')
			print(each_item)
