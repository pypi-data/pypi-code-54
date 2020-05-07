import os

import libtmux

server = libtmux.Server()


def execute(
    cmd,
    session,
    window=None,
    pane=None,
    reset_window=False,
    reset_pane=False,
    dry=False,
):
    session_ = get_session(session)
    window_ = get_window(session_, window_name=window, reset=reset_window)
    pane_ = get_pane(window_, pane_id=pane, reset=reset_pane)
    pane_.cmd("send-keys", change_dir(cmd, dir))
    if not dry:
        pane_.cmd("send-keys", "enter")


def execute_prev(
    session,
    window=None,
    pane=None,
    reset_window=False,
    reset_pane=False,
    cursor_up=1,
    dry=False,
):
    session_ = get_session(session)
    window_ = get_window(session_, window_name=window, reset=reset_window)
    pane_ = get_pane(window_, pane_id=pane, reset=reset_pane)
    for _ in range(cursor_up):
        pane_.cmd("send-keys", "up")
    if not dry:
        pane_.cmd("send-keys", "enter")


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


def get_pane(window, pane_id=None, reset=False):
    assert pane_id is None
    if pane_id is None:
        pane = window.attached_pane
        if not reset:
            return pane
        else:
            new_pane = window.split_window(target=pane.id)
            pane.cmd("kill-pane")
            return new_pane


def change_dir(cmd, dir=None):
    if dir is not None:
        cmd = "cd " + os.path.dirname(os.path.abspath(dir)) + "; " + cmd
    return cmd
