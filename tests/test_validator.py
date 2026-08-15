import sys
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from scanner.validator import parse_ports, validate_target


class ValidatorTests(unittest.TestCase):

    def test_target(self):
        self.assertEqual(validate_target("127.0.0.1"), "127.0.0.1")
        self.assertEqual(validate_target("localhost"), "localhost")

    def test_ports(self):
        self.assertEqual(parse_ports("22,80,443"), [22, 80, 443])
        self.assertEqual(parse_ports("80-82"), [80, 81, 82])
        self.assertEqual(parse_ports("82,80-81,80"), [80, 81, 82])

    def test_invalid_port(self):
        with self.assertRaises(ValueError):
            parse_ports("0")

        with self.assertRaises(ValueError):
            parse_ports("65536")

    def test_invalid_range(self):
        with self.assertRaises(ValueError):
            parse_ports("100-10")


if __name__ == "__main__":
    unittest.main()
