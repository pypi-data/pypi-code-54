def badword(bw,f):
	user_input=bw
	for filter_word in open(f,encoding='utf-8'):
	    fw=filter_word.rstrip()
	    if fw in user_input:
	        fw_len=len(fw)
	        user_input=user_input.replace(fw,'不'+fw)
	else:
	           user_input=user_input.replace("是不","不是").replace('不不','不').replace('想不','不想')

	return user_input