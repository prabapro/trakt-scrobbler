import logging
import sys
from utils import config

logger = logging.getLogger('trakt_scrobbler')

APP_NAME = 'Trakt Scrobbler'
enable_notifs = config['general']['enable_notifs']

if enable_notifs:
    if sys.platform == 'win32':
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
    else:
        import subprocess as sp


def notify(body, title=APP_NAME, timeout=5, stdout=False):
    global enable_notifs
    if stdout or not enable_notifs:
        print(title, body)
    if not enable_notifs:
        return
    if sys.platform == 'win32':
        toaster.show_toast(title, body, duration=timeout, threaded=True)
    elif sys.platform == 'darwin':
        osa_cmd = f'display notification "{body}" with title "{title}"'
        sp.run(["osascript", "-e", osa_cmd])
    else:
        try:
            sp.run(["notify-send", "-a", title, "-t", str(timeout * 1000), body])
        except FileNotFoundError:
            logger.exception("Unable to send notification")
            enable_notifs = False  # disable all future notifications until app restart
