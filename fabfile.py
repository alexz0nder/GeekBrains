from fabric.api import local


def server():
    local('python server')


def client(mode='w'):
    local(f'python client --mode {mode}')

#
# def test():
#     local('pytest --cov-report term-missing --cov server --cache-clear')

def test():
    local('pytest --cov server --cache-clear')
