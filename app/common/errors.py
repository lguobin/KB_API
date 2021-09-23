class DBError(ValueError):
    def __init__(self, msg=None):
        self.message = "[ 数据错误, 传入无效参数 ]"
        if msg != None:
            self.message = msg
    
    def __str__(self):
        return self.message


def Errors(_err):
    return {'status': 'failed', 'error': '错误!操作异常', 'message':'%s' %_err}


# 废弃
def responseAPI(status_code, _message):
    if status_code == 'ok':
        return {'status': 'ok', 'message': '%s' %_message}
    else:
        return {'status': 'failed', 'error': '操作异常', 'message': '%s' %_message}


if __name__ == '__main__':
    pass