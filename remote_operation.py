#encoding:utf-8

import zmq
import json
import socket
import sys

RHOST='192.168.8.99'
#RHOST='10.0.6.45'
#RHOST='172.21.64.129'
PROXY=None

class RemoteProxy(object):
    def __init__(self, rhost):
        self.rhost = rhost
        self.zctx = zmq.Context()
        self.services = {}
        for _name, _port in ('log', 3579), ('dump', 3580):
            _s = self.zctx.socket(zmq.SUB)
            _s.connect('tcp://%s:%d' % (self.rhost, _port))
            _s.setsockopt(zmq.SUBSCRIBE, '')
            self.services[_name] = {'sock':_s, 'rtic': 0, 'dat': {}}

    def trigger(self, tag, ttl=60):
        if len(tag) == 0 or len(tag) > 60:
            print >>sys.stderr, "wrong tag length" 
            return
        try:
            tag.decode('utf-8')
        except UnicodeDecodeError:
            print >>sys.stderr, "wrong tag encoding", tag.encode('hex')
            return
        _s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _s.sendto(('%s %d' % (str(tag), int(ttl))), (self.rhost, 3600))
        print >>sys.stderr, self.rhost, ('%s %d' % (str(tag), int(ttl)))

    def update(self):
        _fail = 1
        for _name, _body in self.services.iteritems():
            _dat = None
            while 1:
                try:
                    _dat = _body['sock'].recv(zmq.NOBLOCK)
                except zmq.error.Again:
                    break
            if _dat:
                _body['rtic'] = 13
                _body['dat'] = json.loads(_dat)
                _fail = 0
            else:
                _r = _body['rtic']
                _r = max(_r - 1, 0)
                _body['rtic'] = _r
                if _r > 0:
                    _fail = 0
        return _fail == 0

# 需要修改任何显示的状态信息，只需要对这个变量修改。
# 在ConnectionJudge返回True的情况下，程序会立即响应修改，显示修改后的内容
state_info = []
# 在ConnectionJudge返回为False的情况下，会显示下面字符串
non_connection = "未连接上远程主机"

def ConnectionJudge(rhost=RHOST):
    '''
    判断是否和远程主机连接成功，如果是返回True否则返回False
    '''
    global PROXY
    if not PROXY:
        PROXY = RemoteProxy(rhost)
    return PROXY.update()

def GetState():
    '''
    如果ConnectionJudge返回True，程序会调用这个函数将远程主机的信息
    以元组(key-value)的格式放入state_info。例如:[('主机名':'Iphone'), ('磁盘大小':'200GB')]
    这个函数不返回任何的值
    注意：key-value都需要是字符串，请处理后存放。最终state_info的内容都会显示在UI界面
    '''
    _proxy = PROXY
    if not _proxy:
        return non_connection
    _log_dat = _proxy.services['log']['dat']
    _dump_dat = _proxy.services['dump']['dat']
    _rlist = []
    _rlist.append((u'会话ID', _log_dat.get('stub', '??')))
    _rlist.append((u'运存余量', _log_dat.get('bmem', '?G')))
    _rlist.append((u'硬盘余量', _dump_dat.get('bspace', '?G')))
    if not _dump_dat.get('busy', 0):
        _rlist.append((u'\n挂载信息', _dump_dat.get('bmount', '??')))
    else:
        _rlist.append((u'\n触发编号', _dump_dat['trig']['tag']))
        _rlist.append((u'进度倒计', str(_dump_dat['busy'])))
    #print(_rlist)
    return _rlist

def Trigger(timeline = ""):
    '''
    接管或者未接管不满意之后，按下确定按钮会执行一次这个函数
    timeline 时间字符串 示例: "2018-05-21 15:35:18"
    没有返回值
    '''
    if PROXY:
        PROXY.trigger(timeline.replace(' ', 'T'))
