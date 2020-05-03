
import desktop_notify

server = desktop_notify.Server('keeprofi')

def Notify(*args):
	return server.Notify(*args)
