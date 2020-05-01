import math


# settings

alfabet = [['q','Q'],['w','W'],['e','E'],['r','R'],
['t','T'],['y','Y'],['u','U'],['i','I'],['o','O'],
['p','P'],['a','A'],['s','S'],['d','D'],['f','F'],
['g','G'],['h','H'],['j','J'],['k','K'],['l','L'],
['z','Z'],['x','X'],['c','C'],['v','V'],['b','B'],
['n','N'],['m','M']]


def num_match_max(num1, num2):
	if num1 > num2:
		return num1
	else:
		return num2

def num_match_min(num1, num2):
	if num1 > num2:
		return num2
	else:
		return num1

def ungreat_match(str1,str2,mkdefolt=0.7,mismatching_chars=5):
	i=0
	lenth1 = len(str1)
	lenth2 = len(str2)
	mk = 0
	min_num = num_match_min(lenth1, lenth2)
	str1 = str1.lower()
	str2 = str2.lower()
	if str1 == str2:
		keys = [str1, 'True']
		return keys
	elif math.fabs(lenth1 - lenth2) > mismatching_chars:
		test = 1
		keys = ['mismatching skills', 'False', test]
		return keys
	else:
		for char in str1:
			if i < min_num:
				if char == str2[i]:
					mk+=1
			i+=1
		if (mk >=  (min_num*mkdefolt)):
			if min_num == lenth1:
				keys = [str1, 'True']
			elif min_num == lenth2:
				keys = [str2, 'True']
			return keys
		else:
			test = 2
			keys = ['mismatching skills', 'False',test]
			return keys
