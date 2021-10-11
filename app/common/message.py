class DBError(ValueError):
    def __init__(self, msg=None):
        self.message = "[ 数据错误, 传入无效参数 ]"
        if msg != None:
            self.message = msg
    
    def __str__(self):
        return self.message


def Errors(_err):
    return {'status': 'failed', 'data':'%s' %_err}


def responseJson(status_code='ok', _message='ok'):
    if status_code == 'ok':
        return {'status': 'ok', 'data': '%s' %_message}
    else:
        return {'status': 'failed', 'data': '%s' %_message}
