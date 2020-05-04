'''
example
'''

import os

from git2gitee.login import GiteeLogin, Cross


if __name__ == '__main__':
    username = 'mikele'
    password = os.getenv('GITEE_PWD')
    print(password)
    gitee = GiteeLogin(username, password)
    if gitee.login():
        print('登陆成功')
    cross = Cross('toyourheart163/git2gitee', username, gitee.token, gitee.sess, gitee.headers)
    cross.import_to_gitee()
    # cross.clone()
    # cross.rename_config_repo_url()
