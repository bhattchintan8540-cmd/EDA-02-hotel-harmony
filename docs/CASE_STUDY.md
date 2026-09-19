# Case study — Hotel Harmony: Data Insights for Optimized Operations

## Problem statement
Booking patterns and guest satisfaction are uneven across hotels, channels, and seasons. Management needs evidence on lead time, cancellations, demand peaks, and revenue so operations and marketing can allocate rooms, staff, and promotions more effectively.

## Overview
Elite Hotels International reviews city and resort booking history to stabilize occupancy, cut avoidable cancellations, and price rooms using ADR and channel mix.

## Stakeholders
- Internal: Management, Operations, Marketing, Customer Service
- External: Guests, Travel agencies, Suppliers

## Data dictionary
| Column | Description |
| --- | --- |
| `hotel` | Resort Hotel or City Hotel |
| `is_canceled` | 1 if canceled, else 0 |
| `lead_time` | Days between booking and arrival |
| `arrival_date_*` | Arrival year, month, week, day |
| `stays_in_weekend_nights / stays_in_week_nights` | Nights booked |
| `adults / children / babies` | Party composition |
| `country` | Guest country of origin |
| `market_segment` | Market segment |
| `distribution_channel` | Booking channel |
| `adr` | Average daily rate |
| `deposit_type` | No Deposit, Non Refund, Refundable |
| `total_of_special_requests` | Count of special requests |
| `reservation_status` | Canceled, Check-Out, No-Show |

## Assignment questions
The brief's basic, medium, and advanced questions are answered in `docs/SOLUTION_GUIDE.md` and `outputs/hotel_harmony/findings.json`.
