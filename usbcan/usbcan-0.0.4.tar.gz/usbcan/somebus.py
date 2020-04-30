# -*- coding: utf-8 -*-
''' somebus.py: Somebus USBCAN-II adaptor driver class.
Copyright (C) 2019 Laigui Qin <laigui@gmail.com>'''

from ctypes import *


class VciInitConfig(Structure):
    """
    INIT_CONFIG结构体定义了初始化CAN的配置
    """
    _fields_ = [("AccCode", c_ulong),           # 验收码，后面是数据类型
                ("AccMask", c_ulong),           # 屏蔽码
                ("Reserved", c_ulong),          # 保留
                ("Filter", c_ubyte),            # 滤波使能。0=不使能，1=使能使能时，/
                # 请参照SJA1000验收滤波器设置验收码和屏蔽码。
                ("Timing0", c_ubyte),           # 波特率定时器0（BTR0）
                ("Timing1", c_ubyte),           # 波特率定时器1（BTR1)
                ("Mode", c_ubyte)]              # 模式。=0为正常模式，=1为只听模式， =2为自发自收模式


class VciCanObj(Structure):
    """
    CAN_OBJ结构体表示帧的数据结构。 在发送函数Transmit和接收函数Receive中被用来传送CAN信息帧。
    """
    _fields_ = [("ID", c_uint),                 # 报文帧ID'''
                ("TimeStamp", c_uint),          # 接收到信息帧时的时间标识
                ("TimeFlag", c_ubyte),          # 是否使用时间标识， 为1时TimeStamp有效
                ("SendType", c_ubyte),          # 发送帧类型。=0时为正常发送,=1时为单次发送（不自动重发)，/
                # =2时为自发自收（用于测试CAN卡是否损坏） ， =3时为单次自发自收（只发送一次， 用于自测试），/
                # 只在此帧为发送帧时有意义。
                ("RemoteFlag", c_ubyte),        # 是否是远程帧。=0时为数据帧，=1时为远程帧。
                ("ExternFlag", c_ubyte),        # 是否是扩展帧。=0时为标准帧（11位帧ID），=1时为扩展帧（29位帧ID）。
                ("DataLen", c_ubyte),           # 数据长度DLC(<=8)， 即Data的长度
                ("Data", c_ubyte * 8),          # CAN报文的数据。 空间受DataLen的约束。
                ("Reserved", c_ubyte * 3)]      # 系统保留


class VciErrInfo(Structure):
    """
    ERR_INFO结构体用于装载VCI库运行时产生的错误信息。 结构体将在ReadErrInfo函数中被填充。
    """
    _fields_ = [("ErrCode", c_uint),            # 错误码。 对应1.2 中的错误码定义。
                ("Passive_ErrData", c_ubyte),   # 当产生的错误中有消极错误时表示为消极错误的错误标识数据
                ("ArLost_ErrData", c_ubyte)]    # 当产生的错误中有仲裁丢失错误时表示为仲裁丢失错误的错误标识数据


class USBCAN():
    """
    GCAN USBCAN adaptor
    """
    STATUS_OK = 1
    STATUS_ERR = 0
    RECEIVE_ERR = 0xFFFFFFFF

    def __init__(self):
        pass

    def OpenDevice(self, nDeviceType, nDeviceInd):
        """

        :param nDeviceType:
        :param nDeviceInd:
        :return:
        """
        dll = windll.LoadLibrary('./ECanVci64.dll')  # 调用dll文件
        nReserved = 0

        return dll.OpenDevice(nDeviceType, nDeviceInd, nReserved)

    def InitCAN(self, DevType, DevIndex, CANIndex, pInitConfig):
        """

        :param DevType:
        :param DevIndex:
        :param CANIndex:
        :param pInitConfig:
        :return:
        """
        dll = windll.LoadLibrary('./ECanVci64.dll')  # 调用dll文件
        return dll.InitCAN(DevType, DevIndex, CANIndex, pInitConfig)

    def StartCAN(self, DevType, DevIndex, CANIndex):
        """
        此函数用以启动USBCAN设备的某一个CAN通道。 如有多个CAN通道时， 需要
        多次调用。 在执行StartCAN函数后， 需要延迟10ms执行Transmit函数。
        :param DevType:
        :param DevIndex:
        :param CANIndex:
        :return:
        """
        dll = windll.LoadLibrary('./ECanVci64.dll')  # 调用dll文件
        return dll.StartCAN(DevType, DevIndex, CANIndex)

    def Transmit(self, DevType, DevIndex, CANIndex, pSend, Len):
        """
        返回实际发送成功的帧数量。
        :param DevType:
        :param DevIndex:
        :param CANIndex:
        :param pSend:
        :param Len:
        :return:
        """
        dll = windll.LoadLibrary('./ECanVci64.dll')  # 调用dll文件
        return dll.Transmit(DevType, DevIndex, CANIndex, pSend, Len)

    def Receive(self, DevType, DevIndex, CANIndex, pReceive, Len, WaitTime):
        """
        此函数从指定的设备CAN通道的缓冲区里读取数据。
        :param DevType:
        :param DevIndex:
        :param CANIndex:
        :param pReceive:
        :param Len:
        :param WaitTime:
        :return:
        """
        dll = windll.LoadLibrary('./ECanVci64.dll')  # 调用dll文件
        return dll.Receive(DevType, DevIndex, CANIndex, pReceive, Len, WaitTime)

    def CloseDevice(self, DevType, DevIndex):
        """
        此函数用于关闭设备。
        :param DevType:
        :param DevIndex:
        :return:
        """
        dll = windll.LoadLibrary('./ECanVci64.dll')  # 调用dll文件
        return dll.CloseDevice(DevType, DevIndex)

    def ClearBuffer(self, DevType, DevIndex, CANIndex):
        """
        此函数用以清空指定CAN通道的缓冲区。
        :param DevType:
        :param DevIndex:
        :param CANIndex:
        :return:
        """
        dll = windll.LoadLibrary('./ECanVci64.dll')  # 调用dll文件
        return dll.ClearBuffer(DevType, DevIndex, CANIndex)

    def ReadErrInfo(self, DevType, DevIndex, CANIndex, pErrInfo):
        """

        :param DevType:
        :param DevIndex:
        :param CANIndex:
        :param pErrInfo:
        :return:
        """
        dll = windll.LoadLibrary('./ECanVci64.dll')  # 调用dll文件
        return dll.ReadErrInfo(DevType, DevIndex, CANIndex, pErrInfo)

    def ReadCanStatus(self, DevType, DevIndex, CANIndex, pCANStatus):
        """

        :param DevType:
        :param DevIndex:
        :param CANIndex:
        :param pCANStatus:
        :return:
        """
        dll = windll.LoadLibrary('./ECanVci64.dll')  # 调用dll文件
        return dll.ReadCanStatus(DevType, DevIndex, CANIndex, pCANStatus)