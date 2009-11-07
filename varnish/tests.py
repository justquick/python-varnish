from varnish import VarnishManager
import unittest


class VarnishTests(unittest.TestCase):
    def setUp(self):
        self.manager = VarnishManager((raw_input('Varnish Management Address (ip:port): '),))
    
    def test_ping(self):
        result = self.manager.run('ping')[0][0]
        self.assertEqual(len(result), 2)
        self.assert_(map(lambda x: isinstance(x, float), (True,True)))
        
    def test_threading(self):
        self.manager.run(('purge.url', '^/myrandomurl/$'), threaded=True)
        self.assert_(self.manager.run('purge.list')[0][0].endswith('^/myrandomurl/$\n'))
        
    def test_stats(self):
        self.assert_(isinstance(self.manager.run('stats')[0][0], dict))
        
    def test_multiple(self):
        result = self.manager.run(( ('ping',None),('ping',None) ))
        self.assertEqual(result[0][0], result[0][1])
        
    def tearDown(self):
        self.manager.close()
        
if __name__ == '__main__':
    unittest.main()
        