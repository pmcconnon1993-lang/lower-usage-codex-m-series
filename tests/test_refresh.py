import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch
p=Path(__file__).resolve().parents[1]/'skills/m-series-local-helper/scripts/refresh.py'
spec=importlib.util.spec_from_file_location('refresh',p); refresh=importlib.util.module_from_spec(spec);spec.loader.exec_module(refresh)

class RefreshTests(unittest.TestCase):
    def test_offline_never_calls_network_or_applies_updates(self):
        with patch.object(refresh,'fetch',side_effect=AssertionError('network')):
            r=refresh.check(True)
        self.assertFalse(r['updates_applied']);self.assertEqual(r['models'],[])
    def test_failures_remain_explicit(self):
        with patch.object(refresh,'fetch',side_effect=OSError('secret-bearing path')):
            r=refresh.check(False)
        self.assertEqual(len(r['errors']),11);self.assertNotIn('secret-bearing',str(r));self.assertFalse(r['updates_applied'])
    def test_changes_are_data_not_promotions(self):
        with patch.object(refresh,'fetch',return_value={'sha':'0'*40,'cardData':{'license':'apache-2.0'},'gated':False}):
            r=refresh.check(False)
        self.assertTrue(all(m['changed'] for m in r['models']))
        self.assertTrue(all(m['changed'] for m in r['runtimes'][:-1]))
        self.assertFalse(r['updates_applied'])

if __name__=='__main__':unittest.main()
