import sys
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from scanner.scoring import score_open_ports


class ScoringTests(unittest.TestCase):

    def test_empty(self):
        score, severity = score_open_ports([])
        self.assertEqual(score, 0)
        self.assertEqual(severity, "NORMAL")

    def test_telnet(self):
        score, severity = score_open_ports([23])
        self.assertEqual(score, 30)
        self.assertEqual(severity, "LOW")

    def test_score_capped(self):
        score, severity = score_open_ports([21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432, 6379])
        self.assertLessEqual(score, 100)
        self.assertEqual(severity, "CRITICAL")


if __name__ == "__main__":
    unittest.main()
