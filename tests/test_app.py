import unittest
from app import calculate_total, format_receipt

class CheckoutTests(unittest.TestCase):
    def test_multiple_units(self):
        self.assertEqual(calculate_total(10, 3), 30)
    def test_zero_quantity(self):
        self.assertEqual(calculate_total(10, 0), 0)
    def test_one_unit(self):
        self.assertEqual(calculate_total(10, 1), 10)
    def test_decimal_price(self):
        self.assertAlmostEqual(calculate_total(2.5, 4), 10)
    def test_free_item(self):
        self.assertEqual(calculate_total(0, 3), 0)
    def test_receipt_regression(self):
        self.assertEqual(format_receipt(30), "Total: $30.00")

