import streamlit as st
import pandas as pd
import plotly.express as px
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

df = pd.read_csv("processed_reviews.csv")

analyzer = SentimentIntensityAnalyzer()

def get_sentiment(review):
    score = analyzer.polarity_scores(str(review))
    compound = score["compound"]

    if compound >= 0.05:
        return "Positive"
    elif compound <= -0.05:
        return "Negative"
    else:
        return "Neutral"

def detect_issue(review):
    review = str(review).lower()

    if any(word in review for word in ["delay", "late", "waiting"]):
        return "Flight Delay"

    elif any(word in review for word in ["baggage", "luggage", "bag"]):
        return "Baggage Issue"

    elif any(word in review for word in ["staff", "crew", "service"]):
        return "Customer Service"

    elif any(word in review for word in ["food", "meal", "breakfast", "dinner"]):
        return "Food Quality"

    elif any(word in review for word in ["seat", "legroom", "space"]):
        return "Seating Comfort"

    else:
        return "Other"

def get_recommendation(issue):

    recommendations = {
        "Flight Delay":
        "Provide travel vouchers and improve schedule management.",

        "Customer Service":
        "Conduct staff training and improve passenger support.",

        "Baggage Issue":
        "Improve baggage tracking and customer communication.",

        "Food Quality":
        "Review catering quality and expand meal options.",

        "Seating Comfort":
        "Improve seat quality and legroom experience.",

        "Other":
        "Investigate customer concerns individually."
    }

    return recommendations.get(issue, "No recommendation available")

st.title("✈️ British Airways Customer Satisfaction Dashboard")

st.subheader("Dataset Overview")

issue_counts = df["issue"].value_counts()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Reviews", len(df))
col2.metric("Positive Reviews", len(df[df["sentiment"] == "Positive"]))
col3.metric("Negative Reviews", len(df[df["sentiment"] == "Negative"]))
col4.metric("Top Issue", issue_counts.idxmax())

st.divider()

st.subheader("Sentiment Distribution")

fig1 = px.pie(
    df,
    names="sentiment",
    title="Customer Sentiment Distribution"
)

st.plotly_chart(fig1, use_container_width=True)

st.divider()

st.subheader("Issue Breakdown")

st.dataframe(issue_counts)

st.divider()

st.subheader("Issue Analysis")

fig2 = px.bar(
    x=issue_counts.index,
    y=issue_counts.values,
    labels={"x": "Issue", "y": "Count"},
    title="Top Customer Issues"
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()

st.subheader("Data")

st.dataframe(
    df[
        [
            "sentiment",
            "issue",
            "recommendation"
        ]
    ]
)

st.divider()

st.subheader("Analyze New Customer Review")

user_review = st.text_area(
    "Enter Customer Review",
    placeholder="Example: Flight delayed 5 hours and staff were rude."
)

if st.button("Analyze Review"):

    if user_review.strip() != "":

        sentiment = get_sentiment(user_review)
        issue = detect_issue(user_review)
        recommendation = get_recommendation(issue)

        st.success(f"Sentiment: {sentiment}")
        st.warning(f"Issue Detected: {issue}")
        st.info(f"Recommendation: {recommendation}")

    else:
        st.error("Please enter a review.")