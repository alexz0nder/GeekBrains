from fabric.api import local


def server():
    local('python server')


def client(mode='w'):
    local(f'python client -m {mode}')


def kill_clients():
    local("if [ $(sudo ps -fA | grep -v grep | grep 'python client') ]; "
          "then sudo ps -fA | grep -v grep | grep 'python client' | awk '{print $2}' | xargs kill -9; fi")


def kill_server():
    local("if [ $(sudo ps -fA | grep -v grep | grep 'python server') ]; "
          "then sudo ps -fA | grep -v grep | grep 'python client' | awk '{print $2}' | xargs kill -9; fi")


def kill_them_all():
    local("if [ $(sudo ps -fA | grep -v grep | grep 'python client') ]; "
          "then sudo ps -fA | grep -v grep | grep 'python client' | awk '{print $2}' | xargs kill -9; fi")
    local("if [ $(sudo ps -fA | grep -v grep | grep 'python server') ]; "
          "then sudo ps -fA | grep -v grep | grep 'python client' | awk '{print $2}' | xargs kill -9; fi")

#
# def test():
#     local('pytest --cov-report term-missing --cov server --cache-clear')

def test():
    local('pytest --cov server --cache-clear')
