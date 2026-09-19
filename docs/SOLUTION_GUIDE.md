# Solution guide
Answers for **Hotel Harmony: Data Insights for Optimized Operations**.

## Basic-level questions
### 1. Average lead time
79.97
### 2. Bookings by hotel type
```json
{
  "City Hotel": 53273,
  "Resort Hotel": 33956
}
```
### 3. Canceled bookings
24008
### 4. Most common arrival month
August
### 5. Average special requests
0.699
### 6. Country with most bookings
PRT
### 7. Average ADR by hotel type
```json
{
  "City Hotel": 111.17,
  "Resort Hotel": 99.06
}
```
### 8. Share requiring parking
0.0838
### 9. Average week/weekend nights
```json
{
  "week": 2.62,
  "weekend": 1.0
}
```
### 10. Bookings with a travel agent id
75088

## Medium-level questions
### 1. Cancellation rate by hotel
```json
{
  "City Hotel": 0.301,
  "Resort Hotel": 0.2348
}
```
### 2. Average ADR by market segment
```json
{
  "Aviation": 100.61,
  "Complementary": 3.09,
  "Corporate": 68.34,
  "Direct": 116.78,
  "Groups": 75.17,
  "Offline TA/TO": 81.57,
  "Online TA": 118.3,
  "Undefined": 15.0
}
```
### 3. Lead time vs cancellation correlation
0.1845
### 4. Top distribution channels
```json
{
  "TA/TO": 69027,
  "Direct": 12954,
  "Corporate": 5062,
  "GDS": 181,
  "Undefined": 5
}
```
### 5. Average previous cancellations by hotel
```json
{
  "City Hotel": 0.036,
  "Resort Hotel": 0.022
}
```
### 6. ADR trend by year
```json
{
  "2015": 92.36,
  "2016": 101.57,
  "2017": 118.91
}
```
### 7. Highest revenue month (ADR x nights)
August
### 8. Special requests vs ADR correlation
0.1464
### 9. Stay length repeat vs new guests
```json
{
  "0": 3.7,
  "1": 1.95
}
```
### 10. Most booked reserved room types
```json
{
  "A": 56435,
  "D": 17376,
  "E": 6036,
  "F": 2820,
  "G": 2050
}
```

## Advanced-level questions
### 1. Logistic model AUC for cancellation
0.7658
### 2. Strongest cancellation drivers (coefficients)
```json
{
  "deposit_type_Non Refund": 2.265,
  "deposit_type_No Deposit": -1.502,
  "deposit_type_Refundable": -0.999,
  "market_segment_Online TA": 0.847,
  "market_segment_Offline TA/TO": -0.69,
  "total_of_special_requests": -0.552,
  "lead_time": 0.444,
  "customer_type_Transient": 0.422
}
```
### 3. ADR vs party composition (linear coefficients)
```json
{
  "adults": 20.698,
  "children": 38.649,
  "babies": 6.723,
  "intercept": 62.118
}
```
### 4. Booking changes vs special requests correlation
0.0183
### 5. Seasonal cancellation rates
```json
{
  "Autumn": 0.2334,
  "Spring": 0.2813,
  "Summer": 0.3158,
  "Winter": 0.2409
}
```
### 6. Lead time median by market segment
```json
{
  "Aviation": 3.0,
  "Complementary": 3.0,
  "Corporate": 5.0,
  "Direct": 15.0,
  "Groups": 115.0,
  "Offline TA/TO": 82.0,
  "Online TA": 55.0,
  "Undefined": 1.5
}
```
