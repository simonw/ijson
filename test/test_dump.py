import os
import subprocess
import sys
import unittest

from ijson import compat
from test.test_base import JSON


class DumpTests(unittest.TestCase):

    def _test_dump(self, method):
        # Ensure printing works on the subprocess in Windows
        # by using utf-8 on its stdout
        env = None
        if 'win' in sys.platform:
            env = dict(os.environ)
            env['PYTHONIOENCODING'] = 'utf-8'
        cmd = [sys.executable, '-m', 'ijson.dump', '-m', method, '-p', '']
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        out, err = proc.communicate(JSON)
        status = proc.wait()
        self.assertEqual(0, status, "out:\n%s\nerr:%s" % (compat.b2s(out), compat.b2s(err)))

    def test_basic_parse(self):
        self._test_dump('basic_parse')

    def test_parse(self):
        self._test_dump('parse')

    def test_kvitems(self):
        self._test_dump('kvitems')

    def test_items(self):
        self._test_dump('items')