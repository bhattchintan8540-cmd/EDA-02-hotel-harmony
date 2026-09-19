from __future__ import annotations

import numpy as np
import pandas as pd

from src.hotel_harmony import clean_hotels


def test_hotel_cleaning_flags_and_nights():
    raw = pd.DataFrame(
        {
            "hotel": ["City Hotel", "Resort Hotel"],
            "is_canceled": [0, 1],
            "lead_time": [10, 200],
            "arrival_date_year": [2017, 2017],
            "arrival_date_month": ["July", "July"],
            "arrival_date_week_number": [27, 27],
            "arrival_date_day_of_month": [1, 2],
            "stays_in_weekend_nights": [1, 2],
            "stays_in_week_nights": [2, 3],
            "adults": [2, 0],
            "children": [np.nan, 0],
            "babies": [0, 0],
            "meal": ["BB", "BB"],
            "country": [np.nan, "PRT"],
            "market_segment": ["Direct", "Online TA"],
            "distribution_channel": ["Direct", "TA/TO"],
            "is_repeated_guest": [0, 0],
            "previous_cancellations": [0, 1],
            "previous_bookings_not_canceled": [0, 0],
            "reserved_room_type": ["A", "A"],
            "assigned_room_type": ["A", "A"],
            "booking_changes": [0, 0],
            "deposit_type": ["No Deposit", "No Deposit"],
            "agent": [np.nan, 1],
            "company": [np.nan, np.nan],
            "days_in_waiting_list": [0, 0],
            "customer_type": ["Transient", "Transient"],
            "adr": [100.0, 80.0],
            "required_car_parking_spaces": [0, 1],
            "total_of_special_requests": [1, 0],
            "reservation_status": ["Check-Out", "Canceled"],
            "reservation_status_date": ["2017-07-03", "2017-07-01"],
        }
    )
    clean = clean_hotels(raw)
    assert len(clean) == 1
    assert clean.loc[0, "total_nights"] == 3
    assert clean.loc[0, "country"] == "Unknown"
    assert clean.loc[0, "children"] == 0
