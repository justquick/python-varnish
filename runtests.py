from varnish import VarnishManager
import os
import unittest


ADDR = os.getenv('PYTHON_VARNISH_ADDR')
if ADDR is None:
    ADDR = raw_input('Varnish Management Address (ip:port) [localhost:2000]: ')
    if not ADDR: ADDR = 'localhost:2000'

WEB_ADDR = os.getenv('PYTHON_VARNISH_WEB_ADDR')
if WEB_ADDR is None:
    WEB_ADDR = raw_input('Varnish Instance Address (ip:port) [localhost:8080]: ')
    if not WEB_ADDR: WEB_ADDR = 'localhost:8080'

class VarnishTests(unittest.TestCase):
    def setUp(self):
        self.manager = VarnishManager((ADDR,))

    def test_ping(self):
        result = self.manager.run('ping')[0][0]
        self.assertEqual(len(result), 2)
        self.assert_(map(lambda x: isinstance(x, float), (True,True)))

    def test_purge(self):
        resp = self.manager.run(
            'purge.url', 'http://%s/myrandomurl/.*' % WEB_ADDR)[0][0]
        self.assertEqual(resp.status, 200)

    def test_ban(self):
        regex = '^/banned/*'
        self.manager.run('ban.url', regex)
        self.assert_(regex, str(self.manager.run('ban.list')))

    def test_multiple(self):
        result = self.manager.run(( ('ping',None),('ping',None) ))
        self.assertEqual(result[0][0], result[0][1])

    def tearDown(self):
        self.manager.close()

if __name__ == '__main__':
    unittest.main()
