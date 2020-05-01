import math
import meteva
from meteva.base.tool.math_tools import lon_lat_to_cartesian
from scipy.spatial import cKDTree
import numpy as np
import copy
import pandas as pd


def accumulate_time(sta_ob,span = 24,step = None,keep_all = False):
    '''观测数据累加'''
    times= sta_ob.loc[:,'time'].values
    times = list(set(times))
    times.sort()
    times = np.array(times)
    dtimes = times[1:] - times[0:-1]
    min_dtime = np.min(dtimes)
    rain_ac = None
    if span is None:
        if step is None:
            print("range or step must be set")
            return
    else:
        dtimes = span * np.timedelta64(1, 'h')
        step = int(dtimes/min_dtime)
    for i in range(step):
        rain1 = sta_ob.copy()
        rain1["time"] = rain1["time"] + min_dtime * i
        rain_ac = meteva.base.add_on_level_time_dtime_id(rain_ac,rain1,how="inner")
    if not keep_all:
        dtimes = times[:] - times[-1]
        dh = (dtimes/min_dtime).astype(np.int32)
        new_times = times[dh%step ==0]
        rain_ac = meteva.base.in_time_list(rain_ac,new_times)
    return rain_ac

def accumulate_dtime(sta_ob,span = 24,step = None,keep_all = False):
    '''观测数据累加'''
    times= sta_ob.loc[:,'time'].values
    times = list(set(times))
    times.sort()
    times = np.array(times)
    dtimes = times[1:] - times[0:-1]
    min_dtime = np.min(dtimes)
    rain_ac = None
    if span is None:
        if step is None:
            print("range or step must be set")
            return
    else:
        dtimes = span * np.timedelta64(1, 'h')
        step = int(dtimes/min_dtime)
    for i in range(step):
        rain1 = sta_ob.copy()
        rain1["time"] = rain1["time"] + min_dtime * i
        rain_ac = meteva.base.add_on_level_time_dtime_id(rain_ac,rain1,how="inner")
    if not keep_all:
        dtimes = times[:] - times[-1]
        dh = (dtimes/min_dtime).astype(np.int32)
        new_times = times[dh%step ==0]
        rain_ac = meteva.base.in_time_list(rain_ac,new_times)
    return rain_ac


def t_rh_to_tw(t,rh):
    '''根据温度和相对湿度计算湿球温度'''
    sta = meteva.base.combine_on_all_coords(t,rh)
    meteva.base.set_stadata_names(sta,["t","rh"])
    T = sta["t"].values
    RH = sta["rh"].values
    Tw = T * np.arctan(0.151977 * np.sqrt(RH + 8.313659)) + np.arctan(T + RH) - np.arctan(
        RH - 1.676331) + 0.00391838 * np.power(RH, 1.5) * np.arctan(0.023101 * RH) - 4.686035

    sta["tw"] = Tw
    sta = sta.drop(["t", "rh"], axis=1)
    return sta

def u_v_to_wind(u,v):
    if isinstance(u,pd.DataFrame):
        sta = meteva.base.combine_on_all_coords(u, v)
        meteva.base.set_stadata_names(sta, ["u", "v"])
        return  sta

    else:
        grid0 = meteva.base.get_grid_of_data(u)
        grid1 = meteva.base.grid(grid0.glon,grid0.glat,grid0.gtime,
                                                  dtime_list= grid0.dtimes,level_list=grid0.levels,member_list=["u","v"])
        wind = meteva.base.grid_data(grid1)
        wind.name = "wind"
        wind.values[0, :, :, :, :, :] = u.values[0, :, :, :, :, :]
        wind.values[1, :, :, :, :, :] = v.values[0, :, :, :, :, :]
        return wind

def speed_angle_to_wind(speed,angle = None):
    if isinstance(speed, pd.DataFrame):
        if angle is not None:
            sta = meteva.base.combine_on_all_coords(speed, angle)
        else:
            sta = speed.copy()
        meteva.base.set_stadata_names(sta, ["speed", "angle"])
        #speed = sta["speed"].values.astype(np.float32)
        #angle = sta["angle"].values.astype(np.float32)
        speed = sta["speed"].values.astype(np.float32)
        angle = sta["angle"].values.astype(np.float32)
        u = -speed * np.sin(angle  * 3.14 / 180)
        v = -speed * np.cos(angle * 3.14 / 180)
        sta["u"] = u
        sta["v"] = v
        sta = sta.drop(["speed", "angle"], axis=1)
        return sta



    else:
        speed_v = speed.values.squeeze()
        angle_v = angle.values.squeeze()

        grid0 = meteva.base.get_grid_of_data(speed)
        grid1 = meteva.base.grid(grid0.glon,grid0.glat,grid0.gtime,
                                                  dtime_list=grid0.dtimes,level_list=grid0.levels,member_list=["u","v"])
        wind = meteva.base.grid_data(grid1)
        wind.name = "wind"
        wind.values[0, :, :, :, :, :] = speed_v[:, :] * np.cos(angle_v[:, :] * math.pi /180)
        wind.values[1, :, :, :, :, :] = speed_v[:, :] * np.sin(angle_v[:, :] * math.pi /180)
        return wind

def t_dtp_to_rh(temp,dtp):
    if isinstance(temp,pd.DataFrame):
        sta = meteva.base.combine_on_all_coords(temp, dtp)
        meteva.base.set_stadata_names(sta, ["t", "dtp"])
        T = sta["t"].values
        if(T[0]>120):
            T -= 273.16
        D = sta["dtp"].values
        if D[0] >120:
            D -= 273.16
        e0 = 6.11 * np.exp(17.15 * T/(235 + T))
        e1 = 6.11 * np.exp(17.15 * D / (235 + D))

        rh = 100 * e1/e0
        sta["rh"] = rh
        sta = sta.drop(["t", "dtp"], axis=1)
        return sta
    else:
        grid0 = meteva.base.get_grid_of_data(temp)

        if temp.values[0,0,0,0,0,0] >120:
            T = temp.values - 273.16
        else:
            T = temp.values
        if dtp.values[0,0,0,0,0,0] >120:
            D = dtp.values - 273.16
        else:
            D = dtp.values

        e0 = 6.11 * np.exp(17.15 * T/(235 + T))
        e1 = 6.11 * np.exp(17.15 * D / (235 + D))

        rh = 100 * e0/e1
        grd = meteva.base.grid_data(grid0,rh)

        return grd

def sta_index_ensemble_near_by_sta(sta_to,nearNum = 100,sta_from = None,drop_frist = False):
    if(sta_to is None):
        return None
    if(sta_from is None):
        sta_from = copy.deepcopy(sta_to)
    xyz_sta0 = lon_lat_to_cartesian(sta_to['lon'].values[:], sta_to['lat'].values[:],R = meteva.base.basicdata.ER)
    xyz_sta1 = lon_lat_to_cartesian(sta_from['lon'].values[:], sta_from['lat'].values[:],R = meteva.base.basicdata.ER)
    tree = cKDTree(xyz_sta0)
    _,indexs = tree.query(xyz_sta1, k=nearNum)
    sta_ensemble = sta_to[meteva.base.get_coord_names()]
    for i in range(nearNum):
        data_name = "data" + str(i)
        sta_ensemble[data_name] = indexs[:,i]
    if drop_frist:
        sta_ensemble = sta_ensemble.drop(columns=['data0'])
    return sta_ensemble

def sta_id_ensemble_near_by_sta(sta_to,nearNum = 100,sta_from = None,drop_frist = False):
    if(sta_to is None):
        return None
    if(sta_from is None):
        sta_from = copy.deepcopy(sta_to)
    xyz_sta0 = lon_lat_to_cartesian(sta_to['lon'].values[:], sta_to['lat'].values[:],R = meteva.base.basicdata.ER)
    xyz_sta1 = lon_lat_to_cartesian(sta_from['lon'].values[:], sta_from['lat'].values[:],R = meteva.base.basicdata.ER)
    tree = cKDTree(xyz_sta0)
    _,indexs = tree.query(xyz_sta1, k=nearNum)
    input_dat = sta_from.ix[:, 'id'].values
    sta_ensemble = sta_to[meteva.base.get_coord_names()]
    for i in range(nearNum):
        data_name = "data" + str(i)
        sta_ensemble[data_name] = input_dat[indexs[:,i]]
    if drop_frist:
        sta_ensemble = sta_ensemble.drop(columns=['data0'])
    return sta_ensemble

def sta_value_ensemble_near_by_sta(sta_to,nearNum = 100,sta_from = None,drop_frist = False):
    if(sta_to is None):
        return None
    if(sta_from is None):
        sta_from = copy.deepcopy(sta_to)
    xyz_sta0 = lon_lat_to_cartesian(sta_to['lon'].values[:], sta_to['lat'].values[:],R = meteva.base.basicdata.ER)
    xyz_sta1 = lon_lat_to_cartesian(sta_from['lon'].values[:], sta_from['lat'].values[:],R = meteva.base.basicdata.ER)
    tree = cKDTree(xyz_sta0)
    _,indexs = tree.query(xyz_sta1, k=nearNum)
    data_name = meteva.base.get_stadata_names(sta_from)[0]
    input_dat = sta_from[data_name].values
    sta_ensemble = sta_to[meteva.base.get_coord_names()]
    for i in range(nearNum):
        data_name = "data" + str(i)
        sta_ensemble[data_name] = input_dat[indexs[:,i]]
    if drop_frist:
        sta_ensemble = sta_ensemble.drop(columns=['data0'])
    return sta_ensemble

def sta_dis_ensemble_near_by_sta(sta_to,nearNum = 100,sta_from = None,drop_frist = False):
    if(sta_to is None):
        return None
    if(sta_from is None):
        sta_from = copy.deepcopy(sta_to)
    xyz_sta0 = lon_lat_to_cartesian(sta_to['lon'].values[:], sta_to['lat'].values[:],R = meteva.base.basicdata.ER)
    xyz_sta1 = lon_lat_to_cartesian(sta_from['lon'].values[:], sta_from['lat'].values[:],R = meteva.base.basicdata.ER)
    tree = cKDTree(xyz_sta0)
    d,_ = tree.query(xyz_sta1, k=nearNum)
    sta_ensemble = sta_to[meteva.base.get_coord_names()]
    for i in range(nearNum):
        data_name = "data" + str(i)
        sta_ensemble[data_name] = d[:,i]
    if drop_frist:
        sta_ensemble = sta_ensemble.drop(columns=['data0'])
    return sta_ensemble

def sta_index_ensemble_near_by_grid(sta, grid,nearNum = 1):
    ER = meteva.base.ER
    members = np.arange(nearNum).tolist()
    grid1 = meteva.base.grid(grid.glon,grid.glat,members=members)
    grd_en = meteva.base.grid_data(grid1)
    xyz_sta =  meteva.base.tool.math_tools.lon_lat_to_cartesian(sta.loc[:,"lon"], sta.loc[:,"lat"],R = ER)
    lon = np.arange(grid1.nlon) * grid1.dlon + grid1.slon
    lat = np.arange(grid1.nlat) * grid1.dlat + grid1.slat
    grid_lon,grid_lat = np.meshgrid(lon,lat)
    xyz_grid = meteva.base.tool.math_tools.lon_lat_to_cartesian(grid_lon.flatten(), grid_lat.flatten(),R = ER)
    tree = cKDTree(xyz_sta)
    value, inds = tree.query(xyz_grid, k=nearNum)
    grd_en.values = inds.reshape((nearNum,1,1,1,grid1.nlat,grid1.nlon))
    return grd_en

def mean_of_sta(sta,used_coords = ["member"]):
    sta_mean = sta[meteva.base.get_coord_names()]
    sta_data = sta[meteva.base.get_stadata_names(sta)]
    value = sta_data.values
    mean = np.mean(value,axis=1)
    sta_mean['mean'] =mean
    return sta_mean

def std_of_sta(sta,used_coords = ["member"]):
    sta_std = sta[meteva.base.get_coord_names()]
    sta_data = sta[meteva.base.get_stadata_names(sta)]
    value = sta_data.values
    std = np.std(value, axis=1)
    sta_std['std'] = std
    return sta_std

def var_of_sta(sta,used_coords = ["member"]):
    sta_var = sta[meteva.base.get_coord_names()]
    sta_data = sta[meteva.base.get_stadata_names(sta)]
    value = sta_data.values
    var = np.var(value, axis=1)
    sta_var['var'] = var
    return sta_var

def max_of_sta(sta,used_coords = ["member"]):
    sta_max = sta[meteva.base.get_coord_names()]
    sta_data = sta[meteva.base.get_stadata_names(sta)]
    value = sta_data.values
    max1 = np.max(value, axis=1)
    sta_max['max'] = max1
    return sta_max

def min_of_sta(sta,used_coords = ["member"]):
    sta_min = sta[meteva.base.get_coord_names()]
    sta_data = sta[meteva.base.get_stadata_names(sta)]
    value = sta_data.values
    min1 = np.min(value, axis=1)
    sta_min['min'] = min1
    return sta_min

#获取网格数据的平均值
def mean_of_grd(grd,used_coords = ["member"]):
    grid0 = meteva.base.basicdata.get_grid_of_data(grd)
    grid1 = meteva.base.basicdata.grid(grid0.glon,grid0.glat,grid0.gtime,grid0.dtimes,grid0.levels,member_list=["mean"])
    dat = np.squeeze(grd.values)
    dat = np.mean(dat,axis = 0)
    grd1 = meteva.base.basicdata.grid_data(grid1,dat)
    return grd1

#获取网格数据的方差
def var_of_grd(grd,used_coords = ["member"]):
    grid0 = meteva.base.basicdata.get_grid_of_data(grd)
    grid1 = meteva.base.basicdata.grid(grid0.glon,grid0.glat,grid0.gtime,grid0.dtimes,grid0.levels,member_list=["var"])
    dat = np.squeeze(grd.values)
    dat = np.var(dat,axis = 0)
    grd1 = meteva.base.basicdata.grid_data(grid1,dat)
    return grd1

#获取网格数据的标准差
def std_of_grd(grd,used_coords = ["member"]):
    grid0 = meteva.base.basicdata.get_grid_of_data(grd)
    grid1 = meteva.base.basicdata.grid(grid0.glon,grid0.glat,grid0.gtime,grid0.dtimes,grid0.levels,member_list=["std"])
    dat = np.squeeze(grd.values)
    dat = np.std(dat,axis = 0)
    grd1 = meteva.base.basicdata.grid_data(grid1,dat)
    return grd1

#获取网格数据的最小值
def min_of_grd(grd,used_coords = ["member"]):
    grid0 = meteva.base.basicdata.get_grid_of_data(grd)
    grid1 = meteva.base.basicdata.grid(grid0.glon,grid0.glat,grid0.gtime,grid0.dtimes,grid0.levels,member_list=["min"])
    dat = np.squeeze(grd.values)
    dat = np.min(dat,axis = 0)
    grd1 = meteva.base.basicdata.grid_data(grid1,dat)
    return grd1

#获取网格数据的最大值
def max_of_grd(grd,used_coords = ["member"]):
    grid0 = meteva.base.basicdata.get_grid_of_data(grd)
    grid1 = meteva.base.basicdata.grid(grid0.glon,grid0.glat,grid0.gtime,grid0.dtimes,grid0.levels,member_list=["max"])
    dat = np.squeeze(grd.values)
    dat = np.max(dat,axis = 0)
    grd1 = meteva.base.basicdata.grid_data(grid1,dat)
    return grd1