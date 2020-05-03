
import dbus
import desktop_notify

CLOSE_REASON_EXPIRED   = 1
CLOSE_REASON_DISMISED  = 2
CLOSE_REASON_CLOSED    = 3
CLOSE_REASON_UNDEFINED = 4

class Server():
	BUS       = 'org.freedesktop.Notifications'
	OBJECT    = '/org/freedesktop/Notifications'
	INTERFACE = 'org.freedesktop.Notifications'

	def __init__(self, app_name):
		self.__mainloop = None
		self.__session_bus = None
		self.__proxy = None
		self.__iface = None

		self.app_name = app_name
		self.shown = {}

	def Notify(self, *args):
		return desktop_notify.Notify(*args)\
			.set_server(self)

	def show(self, notify):
		notify_id = self.iface.Notify(
			self.app_name,
			notify.id,
			notify.icon,
			notify.summary,
			notify.body,
			notify.actions_enumerated,
			notify.hints,
			notify.timeout
		)

		self.shown[notify_id] = notify

		return notify_id

	def close(self, notify):
		self.iface.CloseNotification(
			notify.id
		)

	def __event_closed(self, notify_id, reason):
		notify_id = int(notify_id)

		self.shown[notify_id]._closed(reason)
		del self.shown[notify_id]

	def __event_action(self, notify_id, action_id):
		notify_id = int(notify_id)
		action_id = int(action_id)

		self.shown[notify_id]\
			.action_invoke(action_id)


	@property
	def mainloop(self):
		return self.__mainloop

	@mainloop.setter
	def mainloop(self, mainloop):
		self.__mainloop = mainloop

	def set_mainloop(self, mainloop):
		self.mainloop = mainloop

		return self

	def init_mainloop_glib(self):
		from dbus.mainloop.glib import DBusGMainLoop
		self.__mainloop = DBusGMainLoop()

	def init_mainloop_qt(self):
		from dbus.mainloop.qt import DBusQtMainLoop
		self.__mainloop = DBusQtMainLoop(set_as_default=True)


	@property
	def session_bus(self):
		if (not self.__session_bus):
			self.__session_bus = dbus.SessionBus(
				mainloop = self.mainloop
			)

		return self.__session_bus

	@property
	def proxy(self):
		if (not self.__proxy):
			self.__proxy = self.session_bus.get_object(
				Server.BUS,
				Server.OBJECT
			)

		return self.__proxy

	@property
	def iface(self):
		if (not self.__iface):
			self.__iface = dbus.Interface(
				self.proxy,
				dbus_interface = Server.INTERFACE
			)

			if (self.mainloop):
				self.__iface.connect_to_signal(
					'NotificationClosed',
					self.__event_closed
				)
				self.__iface.connect_to_signal(
					'ActionInvoked',
					self.__event_action
				)

		return self.__iface
