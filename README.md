✈️ AI-Driven Customer Satisfaction Analysis for British Airways

This project is an AI-powered customer feedback analysis system designed to help airlines understand passenger experiences and improve service quality. The application analyzes customer reviews using Amazon Bedrock (Nova Lite) and automatically identifies sentiment, predicted CSAT score, issue category, priority level, root cause, business impact, and actionable recommendations.

The solution is built using Python, Streamlit, AWS Lambda, Amazon API Gateway, Amazon Bedrock, Pandas, and Plotly. A clean and interactive Streamlit dashboard provides business insights through visualizations, including sentiment distribution, issue analysis, and dataset summaries. Users can also submit new reviews for real-time AI analysis powered by cloud-based foundation models.

The system follows a serverless architecture where Streamlit sends customer reviews to an API Gateway endpoint, which invokes an AWS Lambda function. The Lambda function communicates with Amazon Bedrock to generate structured AI insights, returning them to the dashboard within seconds.

Features
🤖 AI-powered review analysis using Amazon Bedrock
😊 Sentiment classification and predicted CSAT score
🚨 Issue detection and priority assessment
🔍 Root cause and business impact identification
💡 Actionable recommendations
📊 Interactive dashboard with data visualizations
☁️ Fully serverless AWS architecture

This project demonstrates the practical application of Generative AI and cloud computing to enhance customer satisfaction analysis and support data-driven decision-making in the airline industry.
