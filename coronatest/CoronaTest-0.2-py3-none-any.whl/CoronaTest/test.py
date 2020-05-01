from pathlib import Path

script_location = Path(__file__).absolute().parent
check_loc = script_location / "CoronaCheck.txt"
sugg_loc = script_location / "suggestions.txt"

with open(check_loc, "r", encoding='utf8') as txt:
    data = txt.read()
    data_list = data.split("\n")
    
with open(sugg_loc, "r", encoding='utf8') as txt:
    suggestions = txt.read()
    suggestions = suggestions.split("\n")
    
def get_prob(data):
    
    Fever103 = 25   #>103
    Fever100 = 20   #>100
    Fever99 = 15    #>=99

    body_hot = 15
    Dry_Cough = 10
    Fatigue   = 7
    Sputum_Production = 7
    Shortness_Breath = 15
    Shortness_Breath_Disease = 7
    Pain = 10
    Smoking = 6
    Sore_throat = 15
    Headache = 7
    Chills = 7
    Vomiting = 6
    Nasal_Congestion = 6
    Diarrhoea = 12
    Past_Disease = 10
    TRAVEL = 5
    day = 20

    sums = 0
    fever_flag=0


    if data[2] > 103:
        sums+=Fever103
        fever_flag=1
    elif data[2]>100:
        sums+=Fever100
        fever_flag=1
    elif data[2]>=99:
        sums+=Fever99
        fever_flag=1
    else:
        sums+=0

    if fever_flag==1 and data[3]==1 and data[4]==0:
        sums+=15
    if fever_flag==1 and data[3]==1 and data[4]==1:
        sums -= 10
    if fever_flag==0 and data[5]==1:
        sums+=body_hot
        
        
        
        
    sums+= \
    data[6]*Dry_Cough+     \
    data[7]*Fatigue+  \
    data[8]*Sputum_Production+    \
    data[9]*Shortness_Breath+ \
    data[10]*Shortness_Breath_Disease+    \
    data[11]*Pain+     \
    data[12]*Smoking+ \
    data[13]*Sore_throat+     \
    data[14]*Headache+    \
    data[15]*Chills+    \
    data[16]*Vomiting+    \
    data[17]*Nasal_Congestion+    \
    data[18]*Diarrhoea+     \
    data[19]*Past_Disease+     \
    data[20]*TRAVEL+    \
    data[21]*day
        
    return sums

import random


    
def pick_ques(index):
    q = data_list[index].split("&&")
    return q[random.randint(0,len(q)-1)]

check_status = True
ans_list = [25, 0, 0, 97, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fev_flag = False
sugg_index = 0
last_ques_index = 0

interrupt_ques = "আপনার করোনা ঝুকি টেস্ট হচ্ছে । আপনি কি টেস্ট করাতে চান না?"
corona_break = "ঠিক আছে আপনার টেস্ট টি স্থগিত করা হলো। তা কি যেনো বলছিলেন?"
sugg_ques = "আপনি কি আপনার করণীয়গুলো জানতে চান?"
yn_ques_map = {
    "yes": ["হ্যাঁ","হ্যা","জ্বী", "আচ্ছা", "আছে", "আছেতো", "অনেক আছে", "অনেক", "আছে", "অল্প আছে", "ইয়েস", "হুম", "হ", "হু", "hm", "hum", "hu", "yes", "Yes" ],
    "no" : ["না", "নাই", "একদম নাই", "নাইতো", "ছিলো", "ছিল" ,"এখন নাই", "নেই", "নেইতো", "ছিলোত", "নো", "ন", "নানা", "no", "na", "never", "নেভার", "নেবার"],
    "male" : ["পুরুষ", "মেইল", "মেল", "মরদ ফুয়া", "ছেলে", "পুলা", "পোয়া", "পোলা", "মদ্দা", "নর" ]
}

def StartTest(i, reply):
    global check_status, ans_list, track_yn_ans, fev_flag, sugg_index, last_ques_index
    
    if i == None:
        i=0
        return  i, pick_ques(i), check_status
    
   

    y_val = sum([s in i.split() for s in reply.lower().split() for i in yn_ques_map["yes"]])
    n_val = sum([s in i.split() for s in reply.lower().split() for i in yn_ques_map["no"]])
    
    if i==0:
        try:
            age = [int(s) for s in reply.split() if s.isdigit()][0]
            ans_list[i] = age
        except:
            pass
        
    elif i==1:
        gen = sum([s in i.split() for s in reply.split() for i in yn_ques_map["male"]])
        if gen:
            ans_list[i] = 1
        else:
            ans_list[i] = 0
    elif i==3:
        try:
            temp = [int(s) for s in reply.split() if s.isdigit()][0]
            ans_list[i] = temp
        except:
            pass
      
    elif i==5 and fev_flag:
        i+=1
        if y_val <  n_val:
            ans_list[i]=0
    elif i==2 and y_val<n_val:
        i+=3
    elif i==2 and y_val>n_val:
        fev_flag = True
    elif i==4 and y_val<n_val:
        i+=2
        ans_list[i]=0
        
    #=============================Last Question===========================
    elif i==22:
        if y_val >  n_val:
            ans_list[i] = 1
        elif y_val <  n_val:
            ans_list[i] = 0
        corona_mat = ans_list[:2]+ans_list[3:]
        result = get_prob(corona_mat)
      
        
        if 0<result<=10:
            sugg_index = 0
        elif 10<result<=25:
            sugg_index = 2
        elif 25<result<=50:
            sugg_index = 4
        elif 50<result<=75:
            sugg_index = 6
        else:
            sugg_index = 8
        i+=1
        return i, suggestions[sugg_index]+" "+sugg_ques, check_status
    #=============================== Get Extra Sugg ========================
    elif i==23:
        if y_val >  n_val:
            sugg_index+=1
            i+=1
            check_status = False
            return i, suggestions[sugg_index], check_status
        elif y_val <  n_val:
            i+=1
            check_status = False
            return i, "ধন্যবাদ", check_status
            
    #======================================Ans of Interrupt Ques==============
    elif i==24:
            if y_val > n_val:
                try:
                    check_status = True
                    return last_ques_index, pick_ques(last_ques_index),check_status
                except:
                    print("Wait Please")
            else:
                check_status = False
                return i, corona_break ,check_status
    #============================== YN Answers and Interrupt Question ========   
        
    else:
        if y_val >  n_val:
            ans_list[i] = 1
        elif y_val <  n_val:
            ans_list[i] = 0
        #============================Interrupt Question=======================
        else:
            last_ques_index = i
            return 24, interrupt_ques, check_status

            

            
    i+=1
    return i, pick_ques(i),check_status