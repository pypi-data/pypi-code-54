import pythoncom
import win32com.client

class SessionEvents:
    def __init__(self):
        self.connected = False

    def OnLogin(self, code, msg):
        # print(code, msg)
        if code == '0000':
            self.connected = True

class Session:
    def __init__(self):
        self.com = win32com.client.DispatchWithEvents("XA_Session.XASession", SessionEvents)
        
    def login(self, id, pwd, cert):
        self.com.ConnectServer("hts.ebestsec.co.kr", 20001)
        self.com.Login(id, pwd, cert, 0, False)
        while not self.com.connected:
            pythoncom.PumpWaitingMessages()

    @property
    def accounts(self):
        num_acc = self.com.GetAccountListCount()
        accounts = {}
        for i in range(num_acc):
            account = {}
            account['계좌번호'] = self.com.GetAccountList(i)
            account['계좌이름'] = self.com.GetAccountName(i)
            account['계좌별명'] = self.com.GetAcctNickname(i)
            account['계좌상세'] = self.com.GetAcctDetailName(i)
            accounts[i] = account
        return accounts