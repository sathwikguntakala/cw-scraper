#!/usr/bin/env python3
"""
Unit tests for Scraper Zero-Mistake Sanity Checks
"""
import unittest
from scrape_rates import validate_price, validate_district_rate, MIN_REALISTIC_PRICE, MAX_REALISTIC_PRICE

class TestSanityChecks(unittest.TestCase):
    def test_valid_prices(self):
        is_valid, val, err = validate_price(145.0, "liveBirdPrice")
        self.assertTrue(is_valid)
        self.assertEqual(val, 145.0)
        self.assertIsNone(err)

    def test_lower_boundary(self):
        is_valid, val, _ = validate_price(MIN_REALISTIC_PRICE, "liveBirdPrice")
        self.assertTrue(is_valid)
        self.assertEqual(val, 50.0)

    def test_upper_boundary(self):
        is_valid, val, _ = validate_price(MAX_REALISTIC_PRICE, "skinlessPrice")
        self.assertTrue(is_valid)
        self.assertEqual(val, 400.0)

    def test_zero_rejected(self):
        is_valid, val, err = validate_price(0, "liveBirdPrice")
        self.assertFalse(is_valid)
        self.assertIn("zero or negative", err)

    def test_negative_rejected(self):
        is_valid, val, err = validate_price(-15.0, "dressedPrice")
        self.assertFalse(is_valid)
        self.assertIn("zero or negative", err)

    def test_null_rejected(self):
        is_valid, val, err = validate_price(None, "liveBirdPrice")
        self.assertFalse(is_valid)
        self.assertIn("null", err)

    def test_below_range_rejected(self):
        is_valid, val, err = validate_price(49.99, "liveBirdPrice")
        self.assertFalse(is_valid)
        self.assertIn("outside realistic range", err)

    def test_above_range_rejected(self):
        is_valid, val, err = validate_price(401.0, "skinlessPrice")
        self.assertFalse(is_valid)
        self.assertIn("outside realistic range", err)

    def test_non_numeric_rejected(self):
        is_valid, val, err = validate_price("N/A", "liveBirdPrice")
        self.assertFalse(is_valid)
        self.assertIn("not a valid number", err)

    def test_district_rate_validation(self):
        # Good district
        good = {
            "id": "AP_ap_ntr_20260926",
            "districtName": "NTR",
            "liveBirdPrice": 142.0,
            "dressedPrice": 220.0,
            "skinlessPrice": 250.0,
        }
        valid, _, err = validate_district_rate(good)
        self.assertTrue(valid)
        self.assertIsNone(err)

        # Corrupt district with 0 price
        corrupt_zero = {
            "id": "AP_ap_ntr_20260926",
            "districtName": "NTR",
            "liveBirdPrice": 0.0,
            "dressedPrice": 220.0,
            "skinlessPrice": 250.0,
        }
        valid, _, err = validate_district_rate(corrupt_zero)
        self.assertFalse(valid)
        self.assertIn("liveBirdPrice is ₹0.00", err)

        # Corrupt district with null skinless price
        corrupt_null = {
            "id": "AP_ap_ntr_20260926",
            "districtName": "NTR",
            "liveBirdPrice": 140.0,
            "dressedPrice": 210.0,
            "skinlessPrice": None,
        }
        valid, _, err = validate_district_rate(corrupt_null)
        self.assertFalse(valid)
        self.assertIn("skinlessPrice is null", err)

    def test_extract_published_date(self):
        from scrape_rates import extract_published_date_from_html
        from datetime import date

        html_sample = "<div><h2>Today Chicken Rate Hyderabad</h2><p>Date: 25-09-2026</p></div>"
        pub_date, _ = extract_published_date_from_html(html_sample)
        self.assertEqual(pub_date, date(2026, 9, 25))

    def test_date_verification_aborts_on_yesterday_rates(self):
        from scrape_rates import verify_market_date_against_ist
        from datetime import date

        today_ist = date(2026, 9, 26)
        yesterday_ist = date(2026, 9, 25)

        # Website still displaying yesterday's rates
        stale_dates = {
            "PoultryBazaar (Hyderabad)": yesterday_ist
        }
        is_verified, err = verify_market_date_against_ist(stale_dates, today_ist)
        self.assertFalse(is_verified)
        self.assertIn("Waiting for market update", err)

        # Website updated with today's rates
        today_dates = {
            "PoultryBazaar (Hyderabad)": today_ist
        }
        is_verified, err = verify_market_date_against_ist(today_dates, today_ist)
        self.assertTrue(is_verified)
        self.assertIsNone(err)

if __name__ == "__main__":
    unittest.main()
