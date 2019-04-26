import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "/../")
from phoenix.RealmRanks import RealmRanks  # noqa: E402


class TestRealmRanks(unittest.TestCase):

    def test_set_rp(self):
        rr = RealmRanks("1L1")
        rr.set_rp(50)
        self.assertEqual(rr.current_rp, 50)

    def test_get_rank_rr1(self):
        rr = RealmRanks("1L2")
        self.assertEqual(rr.get_rank(), 1)

    def test_get_rank_rr5(self):
        rr = RealmRanks("5L9")
        self.assertEqual(rr.get_rank(), 5)

    def test_get_rank_rr14(self):
        rr = RealmRanks("14L0")
        self.assertEqual(rr.get_rank(), 14)

    def test_get_rank_rr15(self):
        # Yes, this should return 14, since we don't have higher rank
        rr = RealmRanks("15L6")
        self.assertEqual(rr.get_rank(), 14)

    def test_get_level_rr1l5(self):
        rr = RealmRanks("1L5")
        self.assertEqual(rr.get_level(), 5)

    def test_get_level_rr2l9(self):
        rr = RealmRanks("2L9")
        self.assertEqual(rr.get_level(), 9)

    def test_get_level_rr6l0(self):
        rr = RealmRanks("6L0")
        self.assertEqual(rr.get_level(), 0)

    def test_get_level_rr14l4(self):
        # Yes, this should return 0, since we don't have higher rank
        rr = RealmRanks("14L4")
        self.assertEqual(rr.get_level(), 0)

    def test_next_level_rr1l2(self):
        rr = RealmRanks("1L2")
        self.assertEqual(rr.next_level(), "125")

    def test_next_level_rr1l2_pretty(self):
        rr = RealmRanks("1L2")
        self.assertEqual(rr.next_level(pretty=True), "R1L3")

    def test_next_level_rr5l9(self):
        rr = RealmRanks("5L9")
        self.assertEqual(rr.next_level(), "1,010,625")

    def test_next_level_rr5l9_pretty(self):
        rr = RealmRanks("5L9")
        self.assertEqual(rr.next_level(pretty=True), "R6L0")

    def test_next_level_rr14l1(self):
        # Yes, this should return rr14l0 value, since we don't have higher rank
        rr = RealmRanks("14L1")
        self.assertEqual(rr.next_level(), "187,917,143")

    def test_next_level_rr14l1_pretty(self):
        # Yes, this should return R14L0, since we don't have higher rank
        rr = RealmRanks("14L1")
        self.assertEqual(rr.next_level(pretty=True), "R14L0")


if __name__ == '__main__':
    unittest.main()
