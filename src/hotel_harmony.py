"""EDA 02 — Hotel Harmony: Data Insights for Optimized Operations."""
from __future__ import annotations

import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .config import ROOT, project_output, savefig
from .download import load_hotels

MONTH_ORDER = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def clean_hotels(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()
    df.columns = [c.strip() for c in df.columns]
    if "children" in df.columns:
        df["children"] = df["children"].fillna(0)
    if "agent" in df.columns:
        df["agent_missing"] = df["agent"].isna().astype(int)
        df["agent"] = df["agent"].fillna(0)
    if "company" in df.columns:
        df["company_missing"] = df["company"].isna().astype(int)
        df["company"] = df["company"].fillna(0)
    df["country"] = df["country"].fillna("Unknown")
    df["adr"] = pd.to_numeric(df["adr"], errors="coerce")
    df = df[df["adr"].between(-10, 1000) | df["adr"].isna()]
    df["total_nights"] = df["stays_in_weekend_nights"].fillna(0) + df["stays_in_week_nights"].fillna(0)
    df["total_guests"] = df["adults"].fillna(0) + df["children"].fillna(0) + df["babies"].fillna(0)
    df["arrival_date"] = pd.to_datetime(
        df["arrival_date_year"].astype(str)
        + "-"
        + df["arrival_date_month"].astype(str)
        + "-"
        + df["arrival_date_day_of_month"].astype(str),
        errors="coerce",
    )
    if "reservation_status_date" in df.columns:
        df["reservation_status_date"] = pd.to_datetime(df["reservation_status_date"], errors="coerce")
    df["arrival_date_month"] = pd.Categorical(df["arrival_date_month"], categories=MONTH_ORDER, ordered=True)
    df = df.drop_duplicates()
    df = df[df["total_guests"] > 0]
    return df.reset_index(drop=True)


def _season(month: str) -> str:
    if month in {"December", "January", "February"}:
        return "Winter"
    if month in {"March", "April", "May"}:
        return "Spring"
    if month in {"June", "July", "August"}:
        return "Summer"
    return "Autumn"


def run() -> dict:
    out = project_output("hotel_harmony")
    raw = load_hotels()
    df = clean_hotels(raw)
    fig_dir = out / "figures"

    plt.figure()
    sns.countplot(data=df, x="hotel", hue="is_canceled", palette=["#16a34a", "#dc2626"])
    plt.title("Bookings by Hotel Type and Cancellation")
    savefig(fig_dir / "01_hotel_cancellations.png")

    plt.figure(figsize=(12, 6))
    month_counts = df["arrival_date_month"].value_counts().reindex(MONTH_ORDER)
    sns.barplot(x=list(month_counts.index.astype(str)), y=month_counts.values, color="#0ea5e9")
    plt.xticks(rotation=45, ha="right")
    plt.title("Arrivals by Month")
    plt.ylabel("Bookings")
    savefig(fig_dir / "02_arrivals_by_month.png")

    plt.figure()
    sample = df.sample(min(8000, len(df)), random_state=42)
    sns.boxplot(data=sample, x="is_canceled", y="lead_time")
    plt.title("Lead Time vs Cancellation")
    savefig(fig_dir / "03_lead_time_cancel.png")

    plt.figure(figsize=(11, 6))
    adr_year = df.groupby("arrival_date_year")["adr"].mean()
    adr_year.plot(marker="o", color="#7c3aed")
    plt.title("Average Daily Rate by Year")
    plt.ylabel("ADR")
    savefig(fig_dir / "04_adr_by_year.png")

    plt.figure(figsize=(11, 6))
    seg = df.groupby("market_segment")["adr"].mean().sort_values(ascending=False)
    sns.barplot(x=seg.values, y=seg.index, color="#f59e0b")
    plt.title("Average ADR by Market Segment")
    savefig(fig_dir / "05_adr_by_segment.png")

    plt.figure(figsize=(11, 6))
    plt.title("Lead Time by Market Segment")
    sns.boxplot(data=df, x="market_segment", y="lead_time", showfliers=False)
    plt.xticks(rotation=35, ha="right")
    savefig(fig_dir / "06_lead_time_segment.png")

    cancel_rate = float(df["is_canceled"].mean())
    avg_lead = float(df["lead_time"].mean())
    hotel_mix = df["hotel"].value_counts().to_dict()
    n_cancel = int(df["is_canceled"].sum())
    peak_month = str(df["arrival_date_month"].mode().iloc[0])
    avg_special = float(df["total_of_special_requests"].mean())
    top_country = str(df["country"].value_counts().idxmax())
    adr_hotel = df.groupby("hotel")["adr"].mean().round(2).to_dict()
    parking_share = float((df["required_car_parking_spaces"] > 0).mean())
    avg_week = float(df["stays_in_week_nights"].mean())
    avg_weekend = float(df["stays_in_weekend_nights"].mean())
    agent_bookings = int((df["agent"] > 0).sum()) if "agent" in df.columns else 0

    cancel_hotel = df.groupby("hotel")["is_canceled"].mean().round(4).to_dict()
    lead_cancel_corr = float(df[["lead_time", "is_canceled"]].corr().iloc[0, 1])
    channel = df["distribution_channel"].value_counts().head(5).to_dict()
    prev_cancel = df.groupby("hotel")["previous_cancellations"].mean().round(3).to_dict()
    month_rev = df.assign(stay_rev=lambda x: x["adr"] * x["total_nights"].clip(lower=1))
    month_rev = month_rev.groupby("arrival_date_month", observed=False)["stay_rev"].sum()
    top_rev_month = str(month_rev.idxmax())
    special_adr = float(df[["total_of_special_requests", "adr"]].corr().iloc[0, 1])
    stay_repeat = df.groupby("is_repeated_guest")["total_nights"].mean().round(2).to_dict()
    room = df["reserved_room_type"].value_counts().head(5).to_dict()

    df["season"] = df["arrival_date_month"].astype(str).map(_season)
    season_cancel = df.groupby("season")["is_canceled"].mean().round(4).to_dict()
    change_req = float(df[["booking_changes", "total_of_special_requests"]].corr().iloc[0, 1])

    model_df = df.dropna(subset=["is_canceled", "lead_time", "adr", "total_of_special_requests", "hotel"]).copy()
    features_num = ["lead_time", "adr", "previous_cancellations", "booking_changes", "total_of_special_requests", "total_nights"]
    features_cat = ["hotel", "deposit_type", "customer_type", "market_segment"]
    features_cat = [c for c in features_cat if c in model_df.columns]
    X = model_df[features_num + features_cat]
    y = model_df["is_canceled"].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    pre = ColumnTransformer(
        [
            ("num", StandardScaler(), features_num),
            ("cat", OneHotEncoder(handle_unknown="ignore"), features_cat),
        ]
    )
    clf = Pipeline([("pre", pre), ("model", LogisticRegression(max_iter=400))])
    clf.fit(X_train, y_train)
    auc = float(roc_auc_score(y_test, clf.predict_proba(X_test)[:, 1]))
    ohe = clf.named_steps["pre"].named_transformers_["cat"]
    cat_names = list(ohe.get_feature_names_out(features_cat))
    names = features_num + cat_names
    coefs = clf.named_steps["model"].coef_[0]
    top_drivers = (
        pd.Series(coefs, index=names).sort_values(key=np.abs, ascending=False).head(8).round(3).to_dict()
    )

    party = model_df[["adults", "children", "babies", "adr"]].dropna()
    lin = LinearRegression().fit(party[["adults", "children", "babies"]], party["adr"])
    party_coef = {
        "adults": round(float(lin.coef_[0]), 3),
        "children": round(float(lin.coef_[1]), 3),
        "babies": round(float(lin.coef_[2]), 3),
        "intercept": round(float(lin.intercept_), 3),
    }

    qa = {
        "basic": [
            {"q": "Average lead time", "a": round(avg_lead, 2)},
            {"q": "Bookings by hotel type", "a": {k: int(v) for k, v in hotel_mix.items()}},
            {"q": "Canceled bookings", "a": n_cancel},
            {"q": "Most common arrival month", "a": peak_month},
            {"q": "Average special requests", "a": round(avg_special, 3)},
            {"q": "Country with most bookings", "a": top_country},
            {"q": "Average ADR by hotel type", "a": adr_hotel},
            {"q": "Share requiring parking", "a": round(parking_share, 4)},
            {"q": "Average week/weekend nights", "a": {"week": round(avg_week, 2), "weekend": round(avg_weekend, 2)}},
            {"q": "Bookings with a travel agent id", "a": agent_bookings},
        ],
        "medium": [
            {"q": "Cancellation rate by hotel", "a": cancel_hotel},
            {"q": "Average ADR by market segment", "a": df.groupby("market_segment")["adr"].mean().round(2).to_dict()},
            {"q": "Lead time vs cancellation correlation", "a": round(lead_cancel_corr, 4)},
            {"q": "Top distribution channels", "a": {k: int(v) for k, v in channel.items()}},
            {"q": "Average previous cancellations by hotel", "a": prev_cancel},
            {"q": "ADR trend by year", "a": df.groupby("arrival_date_year")["adr"].mean().round(2).to_dict()},
            {"q": "Highest revenue month (ADR x nights)", "a": top_rev_month},
            {"q": "Special requests vs ADR correlation", "a": round(special_adr, 4)},
            {"q": "Stay length repeat vs new guests", "a": stay_repeat},
            {"q": "Most booked reserved room types", "a": {k: int(v) for k, v in room.items()}},
        ],
        "advanced": [
            {"q": "Logistic model AUC for cancellation", "a": round(auc, 4)},
            {"q": "Strongest cancellation drivers (coefficients)", "a": top_drivers},
            {"q": "ADR vs party composition (linear coefficients)", "a": party_coef},
            {"q": "Booking changes vs special requests correlation", "a": round(change_req, 4)},
            {"q": "Seasonal cancellation rates", "a": season_cancel},
            {"q": "Lead time median by market segment", "a": df.groupby("market_segment")["lead_time"].median().round(1).to_dict()},
        ],
    }

    findings = {
        "slug": "hotel_harmony",
        "code": "EDA 02",
        "title": "Hotel Harmony: Data Insights for Optimized Operations",
        "dataset": "Hotel booking demand (Antonio, Almeida & Nunes; Kaggle jessemostipak/hotel-booking-demand)",
        "overview": (
            "Elite Hotels International reviews city and resort booking history to stabilize occupancy, "
            "cut avoidable cancellations, and price rooms using ADR and channel mix."
        ),
        "problem_statement": (
            "Booking patterns and guest satisfaction are uneven across hotels, channels, and seasons. "
            "Management needs evidence on lead time, cancellations, demand peaks, and revenue so operations "
            "and marketing can allocate rooms, staff, and promotions more effectively."
        ),
        "methodology": [
            "Clean missing agent/company/children fields, parse arrival dates, drop duplicates and zero-guest rows.",
            "Define metrics: lead time, cancellation rate, stay length, special requests, and ADR-based revenue.",
            "Profile demand by hotel type, month, market segment, and country.",
            "Relate lead time and deposit type to cancellations; fit a logistic baseline.",
            "Convert findings into overbooking, pricing, and loyalty actions.",
        ],
        "data_overview": {
            "rows_raw": int(len(raw)),
            "rows_clean": int(len(df)),
            "cancellation_rate": round(cancel_rate, 4),
            "hotels": {k: int(v) for k, v in hotel_mix.items()},
            "years": sorted(int(y) for y in df["arrival_date_year"].dropna().unique()),
            "average_stay_nights": round(float(df["total_nights"].mean()), 2),
            "realized_stay_share": round(float(1 - cancel_rate), 4),
        },
        "key_findings": [
            f"Overall cancellation rate is {cancel_rate:.1%} after cleaning.",
            f"Guests book about {avg_lead:.0f} days ahead on average; longer lead times track with more cancellations (r={lead_cancel_corr:.2f}).",
            f"{peak_month} is the busiest arrival month; {top_rev_month} leads ADR × stay revenue.",
            f"PRT and other top origin markets dominate volume; {top_country} is the single largest country.",
            f"A logistic model using lead time, deposit, segment, and requests reaches AUC {auc:.2f} on a hold-out set.",
        ],
        "limitations": [
            "The public dataset covers two hotels in Portugal, not a global brand.",
            "ADR is not full P&L; extras, commissions, and costs are missing.",
            "Company and agent IDs are anonymized and heavily missing.",
            "Guest satisfaction is proxied by requests and repeats, not survey scores.",
            "Cancellation model is explanatory, not a production overbooking engine.",
        ],
        "conclusion": (
            "Demand is seasonal and channel-dependent. City vs resort mix, non-refundable deposits, "
            "and long lead times are the practical levers for cancellation control, while ADR and "
            "segment mix drive revenue planning."
        ),
        "recommendations": [
            "Tighten deposit or reminder policies on long-lead leisure bookings with high cancel risk.",
            "Staff and price for the summer/peak-month wave rather than a flat annual plan.",
            "Protect relationships with TA/TO and Direct channels that carry volume.",
            "Use parking and special-request data to design upsell packages, not only room rate.",
            "Build a repeat-guest offer; loyalty stays look different from first-time transient stays.",
        ],
        "qa": qa,
        "figures": [p.relative_to(ROOT).as_posix() for p in sorted(fig_dir.glob("*.png"))],
        "data_dictionary": {
            "hotel": "Resort Hotel or City Hotel",
            "is_canceled": "1 if canceled, else 0",
            "lead_time": "Days between booking and arrival",
            "arrival_date_*": "Arrival year, month, week, day",
            "stays_in_weekend_nights / stays_in_week_nights": "Nights booked",
            "adults / children / babies": "Party composition",
            "country": "Guest country of origin",
            "market_segment": "Market segment",
            "distribution_channel": "Booking channel",
            "adr": "Average daily rate",
            "deposit_type": "No Deposit, Non Refund, Refundable",
            "total_of_special_requests": "Count of special requests",
            "reservation_status": "Canceled, Check-Out, No-Show",
        },
        "additional_resources": [
            "https://www.kaggle.com/jessemostipak/hotel-booking-demand",
            "https://www.sciencedirect.com/science/article/pii/S2352340918315191",
            "docs/CASE_STUDY.md, docs/SOLUTION_GUIDE.md",
        ],
        "stakeholders": {
            "internal": ["Management", "Operations", "Marketing", "Customer Service"],
            "external": ["Guests", "Travel agencies", "Suppliers"],
        },
    }
    (out / "findings.json").write_text(json.dumps(findings, indent=2, default=str), encoding="utf-8")
    df.head(2000).to_csv(out / "cleaned_sample.csv", index=False)
    return findings
