import libtmux

server = libtmux.Server()


def execute(cmd, session_name, window_name, reset_window=True):
    session = get_session(session_name)
    window = get_window(session, window_name, reset=reset_window)
    pane = get_pane_attached(window)
    pane.cmd("send-keys", cmd)
    pane.cmd("send-keys", "enter")


def execute_prev(session_name, window_name, reset_window=True, cursor_up=1):
    session = get_session(session_name)
    window = get_window(session, window_name, reset=reset_window)
    pane = get_pane_attached(window)

    for _ in range(cursor_up):
        pane.cmd("send-keys", "up")
    pane.cmd("send-keys", "enter")


def get_session(session_name, create=True):
    if server.has_session(session_name):
        session = server.find_where({"session_name": session_name})
    else:
        if create:
            session = server.new_session(session_name)
        else:
            raise RuntimeError(f"Session {session_name} does not exist")
    return session


def get_window(session, window_name=None, reset=False):
    if window_name is None:
        window = session.attached_window
        if reset:
            kill_id = window.id
            window = session.new_window(attach=True)
            session.kill_window(kill_id)
        return window

    for window in session.list_windows():
        if window.name == window_name:
            if not reset:
                return window
            else:
                session.kill_window(window_name)

    window = session.new_window(attach=True, window_name=window_name)

    return window


def get_pane_attached(window):
    return window.attached_pane
