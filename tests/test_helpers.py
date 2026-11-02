import os
import sys
import unittest

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import hex_to_rgba_int, parse_page_numbers


class TestHexToRgbaInt(unittest.TestCase):
    def test_valid_six_digit_hex_with_hash(self):
        self.assertEqual(hex_to_rgba_int("#ffffff"), (255, 255, 255, 100))
        self.assertEqual(hex_to_rgba_int("#000000"), (0, 0, 0, 100))
        self.assertEqual(hex_to_rgba_int("#1a2b3c"), (26, 43, 60, 100))

    def test_valid_six_digit_hex_without_hash(self):
        self.assertEqual(hex_to_rgba_int("ff0000"), (255, 0, 0, 100))
        self.assertEqual(hex_to_rgba_int("00ff00"), (0, 255, 0, 100))

    def test_optional_alpha_value(self):
        self.assertEqual(hex_to_rgba_int("#ff0000", alpha=50), (255, 0, 0, 50))
        self.assertEqual(hex_to_rgba_int("#00ff00", alpha=0), (0, 255, 0, 0))
        self.assertEqual(hex_to_rgba_int("#0000ff", alpha=255), (0, 0, 255, 255))

    def test_invalid_hex_length(self):
        with self.assertRaises(ValueError):
            hex_to_rgba_int("#fff")
        with self.assertRaises(ValueError):
            hex_to_rgba_int("#12345")
        with self.assertRaises(ValueError):
            hex_to_rgba_int("#1234567")
        with self.assertRaises(ValueError):
            hex_to_rgba_int("")

    def test_invalid_hex_characters(self):
        with self.assertRaises(ValueError):
            hex_to_rgba_int("#zzzzzz")
        with self.assertRaises(ValueError):
            hex_to_rgba_int("#12345g")
        with self.assertRaises(ValueError):
            hex_to_rgba_int("nothex")


class TestParsePageNumbers(unittest.TestCase):
    def test_individual_page_numbers(self):
        result = parse_page_numbers("1, 3, 5", 10)
        self.assertEqual(sorted(result), [0, 2, 4])

    def test_page_ranges(self):
        result = parse_page_numbers("2-4", 10)
        self.assertEqual(sorted(result), [1, 2, 3])

    def test_combined_numbers_and_ranges(self):
        result = parse_page_numbers("1-3, 5", 10)
        self.assertEqual(sorted(result), [0, 1, 2, 4])
        result2 = parse_page_numbers("1, 4-6, 8", 10)
        self.assertEqual(sorted(result2), [0, 3, 4, 5, 7])

    def test_out_of_range_page_numbers(self):
        result = parse_page_numbers("10, 20", 5)
        self.assertEqual(sorted(result), [])
        result_partial = parse_page_numbers("4-8", 5)
        self.assertEqual(sorted(result_partial), [3, 4])


if __name__ == '__main__':
    unittest.main()
