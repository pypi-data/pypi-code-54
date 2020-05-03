import time
import os


def histurl(url):  # JB
    """Returns the history page url derived from page url argument

    >>> histurl('wiki-page')
    'history/wiki-page_hist'

    :param url: string
    :return: string
    """
    return 'history/' + url + '_hist'


def record_history(path, action, user):  # JB
    r"""Appends an entry composed of action, user, and date
    into history markdown file associated with Riki page path argument.
    Returns the path of history file modified or created. History
    files created in directory content\history with name <page_url>_hist.md

    >>> record_history(r'content\fakepageurl.md', 'action', 'Claude')
    'content/history\\fakepageurl_hist.md'

    :param path: string
    :param action: string
    :param user: string
    :return: string
    """
    htime = time.asctime()
    hpath = path.replace('.md', '_hist.md')
    hpath = hpath.replace('content', 'content/history')
    hparse = path.rsplit('\\', 1)
    hurl = hparse[1].replace('.md', '')
    folder = os.path.dirname(hpath)
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(hpath, 'a', encoding='utf-8') as f:
        if not os.path.getsize(hpath):
            f.write('title: ' + hurl
                    + '\ntags: page history\n\n'
                    + 'Created by ' + user + ' '
                    + htime + '\n')
        else:
            f.write('\n' + action + ' by ' + user + ' ' + htime + '\n')
    return hpath
