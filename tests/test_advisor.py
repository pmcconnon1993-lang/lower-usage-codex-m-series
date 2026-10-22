import importlib.util
from pathlib import Path
import unittest
p=Path(__file__).resolve().parents[1]/'skills/m-series-local-helper/scripts/advisor.py'
spec=importlib.util.spec_from_file_location('advisor',p); advisor=importlib.util.module_from_spec(spec); spec.loader.exec_module(advisor)

class AdvisorTests(unittest.TestCase):
    def rec(self,chip='M5 Ultra',ram=256,os='26.4',space=200,mode='focused'):
        return advisor.recommend(chip,ram,os,space,mode)
    def test_current_recorded_profile_does_not_claim_universal_win(self):
        r=self.rec(); self.assertEqual(r['candidate']['id'],'mlx-community/Qwen3.6-35B-A3B-8bit'); self.assertEqual(r['runtime'],'splash'); self.assertFalse(r['is_universal_best']); self.assertFalse(r['downloads_authorized'])
    def test_ram_beats_generation(self):
        r=self.rec('M6',16); self.assertEqual(r['candidate']['id'],'mlx-community/Qwen3.5-4B-MLX-4bit'); self.assertIsNone(r['draft'])
    def test_m1_is_not_official_splash(self):
        r=self.rec('Apple M1 Max',64); self.assertEqual(r['runtime'],'omlx-mlx'); self.assertTrue(r['m1_m2_splash_fork_candidate'])
    def test_future_variants_stop(self):
        for chip in ['M6 Ultra','M4 Ultra','M7']:
            with self.subTest(chip=chip): self.assertEqual(self.rec(chip)['status'],'research_required')
    def test_os_gates(self):
        self.assertEqual(self.rec(os='14.7')['status'],'research_required')
        self.assertEqual(self.rec(os='26.3')['runtime'],'omlx-mlx')
    def test_multi_model_is_management(self):
        self.assertEqual(self.rec(mode='multi-model')['runtime'],'omlx-splash')
    def test_space_unknown_and_low_block_plan(self):
        self.assertTrue(self.rec(space=None)['checks_before_setup'])
        self.assertIn('Need at least',self.rec(space=1)['checks_before_setup'][0])
    def test_invalid_values(self):
        for ram in [float('nan'),float('inf'),-1,0]:
            with self.assertRaises(ValueError):self.rec(ram=ram)
        for chip in ['Intel','M5; rm','M5Max','M0']:
            with self.assertRaises(ValueError):self.rec(chip)
    def test_memory_thresholds(self):
        for chip,ram,key in [('M1',8,'2B-MLX'),('M2',24,'4B-MLX'),('M5 Max',36,'9B-MLX'),('M5 Max',48,'35B-A3B-4bit'),('M2 Max',64,'35B-A3B-4bit'),('M1 Ultra',128,'35B-A3B-8bit')]:
            self.assertIn(key,self.rec(chip,ram)['candidate']['id'])
    def test_contradictory_hardware_declines(self):
        self.assertEqual(self.rec('M6',256)['status'],'research_required')
        self.assertEqual(self.rec('M5 Ultra',8)['status'],'research_required')
    def test_optional_model_is_lighter_and_not_auto_installed(self):
        r=self.rec();self.assertIn('9B',r['optional_lighter_model']['id']);self.assertFalse(r['downloads_authorized'])
        self.assertIsNone(self.rec('M1',8)['optional_lighter_model'])
    def test_below_minimum_declines(self):
        self.assertEqual(self.rec(ram=4)['status'],'research_required')

if __name__=='__main__': unittest.main()
