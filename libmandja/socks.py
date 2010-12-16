import socket
import struct
import sys
from libmandja.common import isint
from libmandja.common import isipaddr

class Proxy(object):
    _socksip = '127.0.0.1'
    _socksport = 9050
    _socksver = 4
    
    def __init__(self, socksip = None, socksport = None, socksver = None):
        err_wrong_socksver = "Wrong socks version: '{ver}'"\
                             .format(ver = socksver)
        
        if isipaddr(socksip):
            self._socksip = socksip
        
        if isint(socksport):
            self._socksport = socksport
        
        if socksver in (4,5):
            self._socksver = socksver
        elif socksver == None:
            pass
        else:
            raise ValueError(err_wrong_socksver)
    
    @staticmethod
    def socks4ResolveRequest(hostname, username = ''):
        version = 4
        command = 0xF0
        port = 0
        addr = 0x0000001
        usrnm = username
        request_header = struct.pack("!BBHL", version, command, port, addr)
        
        return "%s%s\x00%s\x00"%(request_header, usrnm, hostname)
    
    @staticmethod
    def socks4AParseResponse(response):
        RESPONSE_LEN = 8
        
        if len(response) < RESPONSE_LEN:
            return None
        
        assert len(response) >= RESPONSE_LEN
        version,status,port = struct.unpack("!BBH",response[:4])
        assert version == 0
        assert port == 0
        if status == 90:
            return "%d.%d.%d.%d"%tuple(map(ord, response[4:]))
        else:
            err_socks4_error_response = "Socks4 error response: status {st}"\
                                        .format(st = status)
            raise ValueError(err_socks4_error_response)
    
    @staticmethod
    def socks5Hello():
        return "\x05\x01\x00"
    
    @staticmethod
    def socks5CheckHello(response):
        err_bizarre_response = "Bizarre socks5 hello response: {resp}"\
                               .format(resp = repr(response))
        
        if response != "\x05\x00":
            raise ValueError(err_bizarre_response)
        else:
            return True
    
    @staticmethod
    def socks5ResolveRequest(hostname, username = ''):
        version = 5
        command = 0xF0
        rsv = 0
        port = 0
        atype = 0x03
        reqheader = struct.pack("!BBBB",version, command, rsv, atype)
        portstr = struct.pack("!H",port)
        
        return "%s%s\0%s"%(reqheader,hostname,port)
    
    @staticmethod
    def socks5ParseResponse(response):
        err_overlong_response = "Overlong socks5 reply"
        err_unable_ipv6 = "Handling IPv6 is not implemented"
        
        if len(response) < 8:
            return None
        
        version, reply, rsv, atype = struct.unpack("!BBBB",response[:4])
        
        assert version==5
        assert rsv==0
        
        if reply != 0x00:
            err_wrong_reply_type = "Wrong socks5 reply type: {rpl}"\
                               .format(rpl = repr(reply))
            raise ValueError(err_wrong_reply_type)
        
        assert atype in (0x01,0x04)
        
        expected_len = 4 + ({1:4,4:16}[atype]) + 2
        
        if len(response) < expected_len:
            return None
        elif len(response) > expected_len:
            raise ValueError(err_overlong_response)
        
        addr = response[4:-2]
        
        if atype == 0x01:
            return "%d.%d.%d.%d"%tuple(map(ord,addr))
        else:
            # not really the right way to format IPv6
            # return "IPv6: %s"%(":".join([hex(ord(c)) for c in addr]))
            raise ValueError(err_unable_ipv6)
    
    
    def getHostByName(self, hostname):
        if self._socksver == 4:
            fmt = self.socks4ResolveRequest
            parse = self.socks4AParseResponse
        else:
            fmt = self.socks5ResolveRequest
            parse = self.socks5ParseResponse
        
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sckt.connect((self._socksip,self._socksport))
        
        if self._socksver == 5:
            sckt.send(self.socks5Hello())
            self.socks5CheckHello(sckt.recv(2))
        
        sckt.send(fmt(hostname))
        answer = sckt.recv(8)
        
        result = parse(answer)
        while result is None:
            more = sckt.recv(1)
            if not more:
                # Connection closed; dying
                return None
            answer += more
            result = parse(answer)
        m = sckt.recv(1)
        
        return result
