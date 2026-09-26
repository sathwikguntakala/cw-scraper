#!/usr/bin/env python3
"""
AP & TS Chicken Rates Scraper - Re-exports and runs the official Vencobb & BICC scraper.
"""
from scraper import (
    main,
    validate_price,
    validate_district_rate,
    MIN_REALISTIC_PRICE,
    MAX_REALISTIC_PRICE,
    AP_DISTRICTS,
    TS_DISTRICTS,
    scrape_official_sources,
    generate_daily_district_rates,
    init_firebase_admin,
    get_today_ist,
    extract_published_date_from_html,
    verify_market_date_against_ist,
)

if __name__ == "__main__":
    import sys
    sys.exit(main())
