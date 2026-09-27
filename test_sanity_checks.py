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
        self.assertIsNotNone(err)
        self.assertIn("zero or negative", err or "")

    def test_negative_rejected(self):
        is_valid, val, err = validate_price(-15.0, "dressedPrice")
        self.assertFalse(is_valid)
        self.assertIsNotNone(err)
        self.assertIn("zero or negative", err or "")

    def test_null_rejected(self):
        is_valid, val, err = validate_price(None, "liveBirdPrice")
        self.assertFalse(is_valid)
        self.assertIsNotNone(err)
        self.assertIn("null", err or "")

    def test_below_range_rejected(self):
        is_valid, val, err = validate_price(49.99, "liveBirdPrice")
        self.assertFalse(is_valid)
        self.assertIsNotNone(err)
        self.assertIn("outside realistic range", err or "")

    def test_above_range_rejected(self):
        is_valid, val, err = validate_price(401.0, "skinlessPrice")
        self.assertFalse(is_valid)
        self.assertIsNotNone(err)
        self.assertIn("outside realistic range", err or "")

    def test_non_numeric_rejected(self):
        is_valid, val, err = validate_price("N/A", "liveBirdPrice")
        self.assertFalse(is_valid)
        self.assertIsNotNone(err)
        self.assertIn("not a valid number", err or "")

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
        self.assertIsNotNone(err)
        assert err is not None
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
        self.assertIsNotNone(err)
        assert err is not None
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
        self.assertIsNotNone(err)
        assert err is not None
        self.assertIn("Waiting for market update", err)

        # Website updated with today's rates
        today_dates = {
            "PoultryBazaar (Hyderabad)": today_ist
        }
        is_verified, err = verify_market_date_against_ist(today_dates, today_ist)
        self.assertTrue(is_verified)
        self.assertIsNone(err)

    def test_extract_table_date_from_chickenratetoday(self):
        from scrape_rates import extract_published_date_from_html
        from datetime import date

        table_html = """
        <h2>Chicken Rate Today Hyderabad September 26, 2026</h2>
        <figure class="wp-block-table">
          <table>
            <tbody>
              <tr><td>Date</td><td>Chicken</td><td>Skinless</td><td>Boneless</td></tr>
              <tr><td>September 26, 2026</td><td>170</td><td>210</td><td>220</td></tr>
              <tr><td>September 25, 2026</td><td>170</td><td>210</td><td>220</td></tr>
            </tbody>
          </table>
        </figure>
        """
        pub_date, raw_str = extract_published_date_from_html(table_html)
        self.assertEqual(pub_date, date(2026, 9, 26))
        self.assertIsNotNone(raw_str)
        assert raw_str is not None
        self.assertIn("September 26, 2026", raw_str)

    def test_extract_wholesale_rate_from_table(self):
        from scrape_rates import extract_vencobb_and_mandi_rates_from_html

        table_html = """
        <figure class="wp-block-table">
          <table>
            <tbody>
              <tr><td><strong>Market Wise</strong></td><td><strong>1 Kg Chicken- Live</strong></td><td><strong>Skinless</strong></td><td><strong>Boneless</strong></td></tr>
              <tr><td><strong>1 Kg Rate</strong></td><td>170</td><td>210</td><td>220</td></tr>
              <tr><td><strong>Wholesale Rate</strong></td><td>170</td><td>210</td><td>220</td></tr>
              <tr><td><strong>Retail Rate</strong></td><td>190</td><td>230</td><td>250</td></tr>
            </tbody>
          </table>
        </figure>
        """
        rates = extract_vencobb_and_mandi_rates_from_html(
            table_html,
            source_name="ChickenRateToday (Hyderabad)",
            default_center="hyderabad"
        )
        self.assertIn("hyderabad", rates)
        self.assertEqual(rates["hyderabad"]["wholesale_live_bird"], 170.0)
        self.assertEqual(rates["hyderabad"]["skinlessPrice"], 210.0)

    def test_official_sources_active_urls(self):
        from scrape_rates import OFFICIAL_SOURCES

        urls = [s["url"] for s in OFFICIAL_SOURCES]
        self.assertIn("https://chickenratetoday.in/today-chicken-rate-hyderabad/", urls)
        self.assertIn("https://chickenratetoday.in/today-chicken-rate-andhra-pradesh/", urls)
        self.assertIn("https://chickenratetoday.in/today-chicken-rate-vijayawada/", urls)

        # Confirm broken 404 links and root stale fallback are removed
        for u in urls:
            self.assertNotEqual(u, "https://chickenratetoday.in/hyderabad/")
            self.assertNotEqual(u, "https://chickenratetoday.in/")
            self.assertFalse("poultrysite.in" in u)

    def test_table_yesterday_date_aborts_push(self):
        from scrape_rates import extract_published_date_from_html, verify_market_date_against_ist
        from datetime import date

        table_html = """
        <figure class="wp-block-table">
          <table>
            <tbody>
              <tr><td>Date</td><td>Chicken</td><td>Skinless</td><td>Boneless</td></tr>
              <tr><td>September 25, 2026</td><td>170</td><td>210</td><td>220</td></tr>
            </tbody>
          </table>
        </figure>
        """
        pub_date, _ = extract_published_date_from_html(table_html)
        self.assertEqual(pub_date, date(2026, 9, 25))

        today_ist = date(2026, 9, 26)
        is_verified, err = verify_market_date_against_ist({"ChickenRateToday (Hyderabad)": pub_date}, today_ist)
        self.assertFalse(is_verified)
        self.assertIsNotNone(err)
        assert err is not None
        self.assertIn("Waiting for market update", err)

if __name__ == "__main__":
    unittest.main()
