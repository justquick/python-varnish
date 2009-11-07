"""
Simple Python interface for the Varnish management port.
"""
from telnetlib import Telnet
from threading import Thread

class VarnishHandler(Telnet):
    def __init__(self, host_port_timeout):
        if isinstance(host_port_timeout, basestring):
            host_port_timeout = host_port_timeout.split(':')
        Telnet.__init__(self, *host_port_timeout)
        
    def quit(self): self.close()
        
    def fetch(self, command):
        """
        Run a command on the Varnish backend and return the result
        return value is a tuple of ( (status, length), content )
        """
        self.write('%s\n' % command)
        (status, length), content = map(int, self.read_until('\n').split()), ''
        assert status == 200, 'Bad response code: %s %s' % (status, self.read_until('\n').rstrip())
        while len(content) < length:
            content += self.read_until('\n')
        return (status, length), content
        
    # Service control methods
    def start(self): return self.fetch('start')
    def stop(self): return self.fetch('stop')
    
    # Information methods
    def ping(self, timestamp=None):
        cmd = 'ping'
        if timestamp: cmd += ' %s' % timestamp
        return tuple(map(float, self.fetch(cmd)[1].split()[1:]))
        
    def stats(self):
        stat = {}
        for line in self.fetch('stats')[1].splitlines():
            a = line.split()
            stat['_'.join(a[1:]).lower()] = int(a[0])
        return stat

    def help(self, command=None):
        cmd = 'help'
        if command: cmd += ' %s' % command
        return self.fetch(cmd)[1]

    # VCL methods
    def vcl_load(self, configname, filename):
        return self.fetch('vcl.load %s %s' % (configname, filename))
    
    def vcl_inline(self, configname, vclcontent):
        return self.fetch('vcl.inline %s %s' % (configname, vclcontent))

    def vcl_show(self, configname):
        return self.fetch('vcl.show' % configname)
    
    def vcl_use(self, configname):
        return self.fetch('vcl.use %s' % configname)
    
    def vcl_discard(self, configname):
        return self.fetch('vcl.discard %s' % configname)

    def vcl_list(self):
        vcls = {}
        for line in self.fetch('vcl.list')[1].splitlines():
            a = line.split()
            vcls[a[2]] = tuple(a[:-1])
        return vcls

    # Param methods
    def param_show(self, param, long=False):
        cmd = 'param.show '
        if long: cmd += '-l '
        return self.fetch(cmd + param)

    def param_set(self, param, value):
        self.fetch('param.set %s %s' % (param, value))

    # Purge methods
    def purge_url(self, regex):
        return self.fetch('purge.url %s' % regex)[1]

    def purge_hash(self, regex):
        return self.fetch('purge.hash %s' % regex)[1]

    def purge_list(self):
        return self.fetch('purge.list')[1]
        
    def purge(self, *args):
        for field, operator, arg in args:
            self.fetch('purge %s %s %s\n' % (field, operator, arg))[1]

class ThreadedRunner(Thread):
    """
    Runs commands on a particular varnish server in a separate thread
    """
    def __init__(self, addr, *commands):
        self.addr = addr
        self.commands = commands
        super(ThreadedRunner, self).__init__()
        
    def run(self):
        handler = VarnishHandler(self.addr)
        for cmd in self.commands:
            if isinstance(cmd, tuple) and len(cmd)>1:
                getattr(handler, cmd[0].replace('.','_'))(*cmd[1:])
            else:
                getattr(handler, cmd.replace('.','_'))()
        handler.close()

def run(addr, *commands):
    """
    Non-threaded batch command runner returning output results
    """
    results = []
    handler = VarnishHandler(addr)
    for cmd in commands:
        if isinstance(cmd, tuple) and len(cmd)>1:
            results.extend([getattr(handler, c[0].replace('.','_'))(*c[1:]) for c in cmd])
        else:
            results.append(getattr(handler, cmd.replace('.','_'))())
    handler.close()
    return results

class VarnishManager(object):
    def __init__(self, servers):
        assert len(servers), 'No servers found, please declare some'
        self.servers = servers
            
    def run(self, *commands, **kwargs):
        if kwargs.pop('threaded', False):
            [ThreadedRunner(server, *commands).start() for server in self.servers]
        else:                
            return [run(server, *commands) for server in self.servers]

    def help(self, command=None): return self.servers[0].help(command)

    def close(self):
        self.run('close', threaded=True)
        self.servers = ()
