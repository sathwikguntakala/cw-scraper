#!/usr/bin/env python3
"""
Entrypoint for the AP & TS Chicken Rates Scraper.
Imports and runs the Zero-Mistake validated scraper.
"""
import sys
from scrape_rates import (
    main,
    validate_price,
    validate_district_rate,
    MIN_REALISTIC_PRICE,
    MAX_REALISTIC_PRICE,
    AP_DISTRICTS,
    TS_DISTRICTS,
)

if __name__ == "__main__":
    sys.exit(main())
