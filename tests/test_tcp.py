import sys
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from scanner.tcp import service_hint


class TcpTests(unittest.TestCase):

    def test_service_hints(self):
        self.assertEqual(service_hint(80), "http")
        self.assertEqual(service_hint(443), "https")

    def test_unknown_service(self):
        self.assertIsInstance(service_hint(65000), str)


if __name__ == "__main__":
    unittest.main()
