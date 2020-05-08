
from hehe import he

class Session:


    def open(self):
        # session
        if he.app.conf.onSession and he.hasComponent('hsession'):
            session = he.getBean('hsession')
            sessId = he.app.getRequest().getCookie(session.getName());
            if sessId:
                session.setSessionId(sessId)
            session.open()

        return ;

    def close(self):

        # session
        if he.app.conf.onSession and he.hasComponent('hsession'):
            session = he.getBean('hsession')
            sessionHandler = session.getSessionHandler()
            response = he.app.getRespone()
            response.addCookie(sessionHandler.getName(), sessionHandler.buildHttpCookie())
            session.close()

        return ;