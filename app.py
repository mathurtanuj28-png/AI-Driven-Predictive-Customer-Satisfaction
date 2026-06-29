import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import json

st.set_page_config(
    page_title="British Airways AI Dashboard",
    page_icon="✈️",
    layout="wide"
)

API_URL = "https://u8optahibl.execute-api.us-east-1.amazonaws.com/prod/analyze"

df = pd.read_csv("processed_reviews.csv")

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

st.plotly_chart(fig1, width="stretch")

st.divider()

st.subheader("Issue Breakdown")

st.dataframe(issue_counts, width="stretch")

st.divider()

st.subheader("Issue Analysis")

fig2 = px.bar(
    x=issue_counts.index,
    y=issue_counts.values,
    labels={"x": "Issue", "y": "Count"},
    title="Top Customer Issues"
)

st.plotly_chart(fig2, width="stretch")

st.divider()

st.subheader("Dataset")

st.dataframe(
    df[["sentiment", "issue", "recommendation"]],
    width="stretch"
)

st.divider()

st.header("🤖 AI Review Analyzer")

user_review = st.text_area(
    "Enter Customer Review",
    placeholder="Example: Flight delayed / staff were rude."
)

if st.button("Analyze Review"):

    if not user_review.strip():
        st.error("Please enter a review.")

    else:

        with st.spinner("Analyzing with Amazon Bedrock..."):

            try:

                response = requests.post(
                    API_URL,
                    json={"review": user_review},
                    timeout=30
                )

                if response.status_code != 200:
                    st.error(f"API Error ({response.status_code})")
                    st.code(response.text)
                    st.stop()

                result = response.json()

                if isinstance(result, dict) and "body" in result:
                    result = json.loads(result["body"])

                st.success(f"Sentiment: {result.get('sentiment','N/A')}")

                c1, c2 = st.columns(2)

                with c1:
                    st.metric(
                        "Predicted CSAT",
                        result.get("predicted_csat", "N/A")
                    )

                with c2:
                    st.metric(
                        "Priority",
                        result.get("priority", "N/A")
                    )

                st.subheader("Issue")
                st.warning(result.get("issue", "N/A"))

                st.subheader("Root Cause")
                st.write(result.get("root_cause", "N/A"))

                st.subheader("Business Impact")
                st.info(result.get("business_impact", "N/A"))

                st.subheader("Recommendation")
                st.success(result.get("recommendation", "N/A"))

            except requests.exceptions.Timeout:
                st.error("Request timed out.")

            except requests.exceptions.ConnectionError:
                st.error("Could not connect to API Gateway.")

            except Exception as e:
                st.exception(e)
