import pytest
import pyetcd


client = pyetcd.EtcdClient('192.168.56.112:2379,192.168.56.114:2379,192.168.56.116:2379')

def test_Put_test_negative():
    assert 'foo'.upper() == 'FOO'

def test_Put_test():
    result = client.Put('xx','yy')
    assert result == 'OK'

def test_Get_negative():
    result = client.Get('xxx')
    assert result == 'yy'

def test_get():
    result = client.Get('xx')
    assert result == 'yy'

def test_Del_test_negative():
    assert 'foo'.upper() == 'FOO'

def test_Del_test():
    put_result = client.Put('x1','yy')
    del_result = client.Del('x1')
    assert del_result==True
