import meteva
import copy
import datetime
import math
import time
import pandas as pd
import numpy as np




def get_time_str_one_by_one(time1,time0 = None,row = 1):
    if row == 2:
        if time0 is None:
            time2 = meteva.base.tool.time_tools.all_type_time_to_datetime(time1)
            if time2.hour == 0 and time2.minute == 0:
                time_str = time2.strftime('%d{d}\n%Y{y}%m{m}').format(y='年', m='月', d='日')
            elif time2.minute == 0:
                time_str = time2.strftime('%H{h}\n%d{d}\n%Y{y}%m{m}').format(y='年', m='月', d='日',h='时')
            else:
                time_str = time2.strftime('%M{mi}\n%H{h}\n%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日',h='时',mi = '分')
        else:
            time00 = meteva.base.tool.time_tools.all_type_time_to_datetime(time0)
            time2 = meteva.base.tool.time_tools.all_type_time_to_datetime(time1)
            if time2.year != time00.year:
                if time2.hour == 0 and time2.minute == 0:
                    time_str = time1.strftime('%d{d}\n%Y{y}%m{m}').format(y='年', m='月', d='日')
                elif time1.minute == 0:
                    time_str = time1.strftime('%H{h}\n%d{d}\n%Y{y}%m{m}').format(y='年', m='月', d='日',h='时')
                else:
                    time_str = time1.strftime('%M{mi}\n%H{h}\n%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日',h='时',mi = '分')
            elif time2.month != time00.month:
                if time2.hour == 0 and time2.minute == 0:
                    time_str = time2.strftime('%d{d}\n%m{m}').format(m='月', d='日')
                elif time2.minute == 0:
                    time_str = time2.strftime('%H{h}\n%m{m}%d{d}').format(m='月', d='日',h='时')
                else:
                    time_str = time2.strftime('%M{mi}\n%H{h}\n%m{m}%d{d}').format(m='月', d='日',h='时',mi = '分')
            elif time2.day != time00.day:
                if time2.hour == 0 and time2.minute == 0:
                    time_str = time2.strftime('%d{d}').format(d='日')
                elif time2.minute == 0:
                    time_str = time2.strftime('%H{h}\n%d{d}').format(d='日',h='时')
                else:
                    time_str = time2.strftime('%M{mi}\n%H{h}\n%d{d}').format(d='日',h='时',mi = '分')
            elif time2.hour != time00.hour:
                if time2.minute == 0:
                    time_str = time2.strftime('%H{h}').format(h='时')
                else:
                    time_str = time2.strftime('%M{mi}\n%H{h}').format(h='时',mi = '分')
            else:
                time_str = time2.strftime("%M分")
    else:
        if time0 is None:
            time2 = meteva.base.tool.time_tools.all_type_time_to_datetime(time1)
            if time2.hour == 0 and time2.minute == 0:

                time_str = time2.strftime('%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日')
            elif time2.minute == 0:
                time_str = time2.strftime('%Y{y}%m{m}%d{d}%H{h}').format(y='年', m='月', d='日', h='时')
            else:
                time_str = time2.strftime('%Y{y}%m{m}%d{d}%H{h}%M{mi}').format(y='年', m='月', d='日', h='时', mi='分')
        else:
            time00 = meteva.base.tool.time_tools.all_type_time_to_datetime(time0)
            time2 = meteva.base.tool.time_tools.all_type_time_to_datetime(time1)
            if time2.year != time00.year:
                if time2.hour == 0 and time2.minute == 0:
                    time_str = time1.strftime('%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日')
                elif time1.minute == 0:
                    time_str = time1.strftime('%Y{y}%m{m}%d{d}%H{h}').format(y='年', m='月', d='日', h='时')
                else:
                    time_str = time1.strftime('%Y{y}%m{m}%d{d}%H{h}%M{mi}').format(y='年', m='月', d='日', h='时', mi='分')
            elif time2.month != time00.month:
                if time2.hour == 0 and time2.minute == 0:
                    time_str = time2.strftime('%m{m}%d{d}').format(m='月', d='日')
                elif time2.minute == 0:
                    time_str = time2.strftime('%m{m}%d{d}%H{h}').format(m='月', d='日', h='时')
                else:
                    time_str = time2.strftime('%m{m}%d{d}%H{h}%M{mi}').format(m='月', d='日', h='时', mi='分')
            elif time2.day != time00.day:
                if time2.hour == 0 and time2.minute == 0:
                    time_str = time2.strftime('%d{d}').format(d='日')
                elif time2.minute == 0:
                    time_str = time2.strftime('%d{d}%H{h}').format(d='日', h='时')
                else:
                    time_str = time2.strftime('%d{d}%H{h}%M{mi}').format(d='日', h='时', mi='分')
            elif time2.hour != time00.hour:
                if time2.minute == 0:
                    time_str = time2.strftime('%H{h}').format(h='时')
                else:
                    time_str = time2.strftime('%H{h}%M{mi}').format(h='时', mi='分')
            else:
                time_str = time2.strftime("%M分")
    return time_str

def get_time_str_list(time_list,row = 1):
    str1 = get_time_str_one_by_one(time_list[0],None,row)
    time_str_list = [str1]
    for i in range(1,len(time_list)):
        time_str_list.append(get_time_str_one_by_one(time_list[i],time_list[i-1],row))
    return time_str_list

def get_save_path(save_dir,method,group_by,group_list,model_name,type,discription = None):

    if discription is None:
        discription = ""
    else:
        discription ="_"+discription
    if save_dir is None:
        save_path = None
    else:
        save_dir = save_dir.replace("\\", "/")
        if group_by is None:
            save_path = save_dir + "/"+method.__name__+"_" +model_name+discription+type
        else:
            save_path = save_dir + "/" +method.__name__+"_" + model_name + "_"+ group_by + str(group_list)+discription+type
    return save_path

def get_title_from_dict(method,s,g,group_list,model_name,title = None):
    if title is not None:
        title1 = title
    else:
        method_str =  method.__defaults__[-1]
        s_str = ""
        if s is not None:

            r = dict(s)
            if "drop_last" in r.keys():
                del r["drop_last"]
            if "member" in r.keys():
                del r["member"]

            if "grid" in r.keys():
                grid0 = r["grid"]
                del r["grid"]
                grid_str = "grid:[" + str(grid0.slon)+"-"+str(grid0.elon)+"°E, " + str(grid0.slat) + "-" + str(grid0.elat)+"°N]"
                if len(r.keys())>0:
                    s_str = str(r)+""
                    s_str = s_str.replace("{","").replace("}","")
                    s_str +=","+grid_str
                    s_str = "\n{" + s_str+"}"
                else:
                    s_str ="\n{" + grid_str +"}"
            else:
                if len(r.keys())>0:
                    s_str = "\n"+str(r)+""


        group_name = ""
        if g is not None:
            group_name = "\n("+g+"="
            if not isinstance(g,list):
                group_list = [group_list]
            g_num = len(group_list)
            if g in ["time","ob_time","day","ob_day"]:
                #判断是否等间距
                if g_num == 1:
                    time_str = get_time_str_one_by_one(group_list[0])
                    group_name += time_str
                elif g_num == 2:
                    time_str1 = get_time_str_one_by_one(group_list[0])
                    time_str2 = get_time_str_one_by_one(group_list[1],group_list[0])
                    group_name += time_str1+"|"+time_str2
                elif g_num == 3:
                    time_str1 = get_time_str_one_by_one(group_list[0])
                    time_str2 = get_time_str_one_by_one(group_list[1],group_list[0])
                    time_str3 = get_time_str_one_by_one(group_list[2], group_list[1])
                    group_name += time_str1+"|"+time_str2 +"|"+time_str3
                else:
                    #判断时间是否等间距
                    time_str1 = get_time_str_one_by_one(group_list[0])
                    time_str2 = get_time_str_one_by_one(group_list[-1],group_list[0])
                    group_name += time_str1 + "至" + time_str2
            else:

                if g_num < 5:
                    for i in range(g_num):
                        loc = group_list[i]
                        if type(loc) == str:
                            group_name += loc
                        else:
                            group_name += str(loc)

                        if i < len(group_list) - 1:
                            group_name += "|"
                else:
                    loc = group_list[0]
                    if type(loc) == str:
                        group_name += loc +"|"+ group_list[1]+"|...|"+group_list[-1]
                    else:
                        group_name += str(loc)+"|"+ str(group_list[1])+"|...|"+str(group_list[-1])
            group_name = group_name + ")"
        if model_name is not None:
            model_name = "(" + model_name + ")"
        else:
            model_name = ""
        title1 = method_str + model_name + s_str +group_name
    return title1

def get_title(method,group_by,group_list,model_name,title = None,discription_uni = ""):

    if group_by is None:
        if(title is None):
            title1 = method.__defaults__[-1] + "(" + model_name  + ")" + discription_uni
        else:
            title1 = title+ "(" + model_name  + ")"
    else:
        group_name = group_by + "="

        if not isinstance(group_list,list):
            group_list = [group_list]
        g_num = len(group_list)
        if group_by in ["time","ob_time","day","ob_day"]:
            #判断是否等间距
            if g_num == 1:
                time_str = get_time_str_one_by_one(group_list[0])
                group_name += time_str
            elif g_num == 2:
                time_str1 = get_time_str_one_by_one(group_list[0])
                time_str2 = get_time_str_one_by_one(group_list[1],group_list[0])
                group_name += time_str1+"|"+time_str2
            elif g_num == 3:
                time_str1 = get_time_str_one_by_one(group_list[0])
                time_str2 = get_time_str_one_by_one(group_list[1],group_list[0])
                time_str3 = get_time_str_one_by_one(group_list[2], group_list[1])
                group_name += time_str1+"|"+time_str2 +"|"+time_str3
            else:
                #判断时间是否等间距
                time_str1 = get_time_str_one_by_one(group_list[0])
                time_str2 = get_time_str_one_by_one(group_list[-1],group_list[0])
                group_name += time_str1 + "至" + time_str2
        else:

            if g_num < 5:
                for i in range(g_num):
                    loc = group_list[i]
                    if type(loc) == str:
                        group_name += loc
                    else:
                        group_name += str(loc)

                    if i < len(group_list) - 1:
                        group_name += "|"
            else:
                loc = group_list[0]
                if type(loc) == str:
                    group_name += loc +"|"+ group_list[1]+"|...|"+group_list[-1]
                else:
                    group_name += str(loc)+"|"+ str(group_list[1])+"|...|"+str(group_list[-1])

        if title is not None:
            title1 = title + discription_uni
        else:
            title1 = method.__defaults__[-1] + "(" + model_name + ")" + discription_uni +"\n("+group_name+")"
    return title1


def get_unique_coods(sta):
    begin = time.time()
    nline = len(sta.index)
    #print(nline)
    discription = ""
    if sta["level"].values[0] == sta["level"].values[-1]:
        repete = len(sta["level"].drop_duplicates().index)
        if repete == 1:
            discription += "level=" + str(sta["level"].values[0]) +" "
    #print("level")
    #print(time.time() - begin)
    #判断空间的一致性
    not_unique = True
    if sta["id"].values[0] == sta["id"].values[-1]:
        repete = len(sta["time"].drop_duplicates().index)
        if repete == 1:
            discription += "id=" + str(sta["id"].values[0])+" "
            not_unique = False
    #print("id")
    #print(time.time() - begin)

    time0 = meteva.base.time_tools.all_type_time_to_datetime(sta["time"].values[0])
    time_1 =  meteva.base.time_tools.all_type_time_to_datetime(sta["time"].values[-1])

    #判断时间的一致性
    not_unique = True
    if time0 == time_1:
        repete = len(sta["time"].drop_duplicates().index)
        if repete == 1:
            print(sta["time"].values[0])
            discription += "time=" + get_time_str_one_by_one(sta["time"].values[0])+" "
            not_unique = False
    #print("time")
    #print(time.time() - begin)
    if not_unique:
        #判断是否是同一fo_hour
        if time0.hour == time_1.hour:

            times = pd.Series(0, sta["time"])
            if len(times.index.hour.drop_duplicates()) == 1:
                discription += "hour=" + str(times.index.hour[0])+" "
                not_unique = False

        #print("hour")
        #print(time.time() - begin)

        day_unique = False
        if not_unique:
            #判断是否是同一fo_dayofyear
            #dayofyears = sta['time'].map(lambda x: x.dayofyear)
            if time0.timetuple().tm_yday == time_1.timetuple().tm_yday:
                times = pd.Series(0, sta["time"])
                if len(times.index.dayofyear.drop_duplicates())==1:
                    discription += "dayofyear=" + str(times.index.dayofyear[0])+" "
                    day_unique = True

        #print("day")
        #print(time.time() - begin)
        #如果日期是一致的，就不用判断年月了
        month_unique = False
        if not day_unique:
            #判断是否是同一fo_month
            if time0.month == time_1.month:
                times =  pd.Series(0,sta["time"])
                if len(times.index.month.drop_duplicates())==1:
                    discription += "month=" + str(times.index.month[0])+" "
                    month_unique = True
        #print("month")
        #print(time.time() - begin)
        if not month_unique:
            #判断是否是同一fo_year
            if time0.year == time_1.year:
                times  = pd.Series(0,sta["time"])
                if len(times.index.year.drop_duplicates()) == 1:
                    discription += "year=" + str(times.index.year[0])+" "
    #print(time.time() - begin)
    if discription != "":
        discription = "\n("+discription[0:-1]+")"
    return discription


def get_group_name(group_list_list):
    if group_list_list is None:
        return ["all"]
    group_name = []
    group_list0 = group_list_list[0]
    if isinstance(group_list0,list):
        group0 = group_list0[0]
    else:
        group0 = group_list0
    if isinstance(group0,datetime.datetime):
        #判断是否都为单个时刻
        islist = False
        for group_list in group_list_list:
            if isinstance(group_list,list):
               islist
        if not islist:
            group_name = get_time_str_list(group_list_list,row=2)
        else:
            for i in range(len(group_list_list)):
                group_name.append("tg"+str(i))
    else:
        for group_list in group_list_list:
            if isinstance(group_list,list):
                str1 = str(group_list)
                if len(str1)<10:
                    str2 = str1
                else:
                    str2 = str1[0:3]+"..."+str1[-3:]
            else:
                str2 = str(group_list)
            group_name.append(str2)
    return group_name

def get_x_label(groupy_by):
    if groupy_by =="time":
        return "时间(预报起报时间)"
    elif groupy_by == "level":
        return "层次"
    elif groupy_by=="year":
        return "年份(预报起报时间)"
    elif groupy_by=="month":
        return "月份(预报起报时间)"
    elif groupy_by=="day":
        return "日期(预报起报时间)"
    elif groupy_by=="dayofyear":
        return "日期在一年中的排序(预报起报时间)"
    elif groupy_by=="hour":
        return "小时数(预报起报时间)"
    elif groupy_by =="ob_time":
        return "观测时间"
    elif groupy_by=="ob_year":
        return "年份(观测时间)"
    elif groupy_by=="ob_month":
        return "月份(观测时间)"
    elif groupy_by=="ob_day":
        return "日期(观测时间)"
    elif groupy_by=="ob_dayofyear":
        return "日期在一年中的排序(观测时间)"
    elif groupy_by=="ob_hour":
        return "小时数(观测时间)"
    elif groupy_by == "dtime":
        return "时效"
    elif groupy_by == "dday":
        return "预报时效包含的天数"
    elif groupy_by == "dday":
        return "预报时效整除24小时后的余数"
