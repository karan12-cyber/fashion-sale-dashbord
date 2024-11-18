import streamlit as st
import pandas as pd

# Set Streamlit page configuration
st.set_page_config(
    page_title="Fashion Sales Dashboard",
    page_icon="🛍",
    layout="wide"
)

# New dummy data for testing
@st.cache_data
def load_dummy_data():
    return pd.DataFrame({
        'Month_Name': ['January', 'February', 'March', 'April', 'May', 'June'],
        'Brand': ['Brand X', 'Brand Y', 'Brand Z', 'Brand A', 'Brand B', 'Brand C'],
        'Quantity_Sold': [200, 150, 300, 100, 120, 80],
        'Quantity_In_Stock': [100, 60, 200, 50, 40, 30],
        'Marketing_Group': ['Premium', 'Budget', 'Premium', 'Budget', 'Luxury', 'Luxury'],
        'Classified_Category': ['Apparel', 'Footwear', 'Apparel', 'Accessories', 'Footwear', 'Accessories'],
        'Category': ['Men', 'Women', 'Kids', 'Unisex', 'Men', 'Women'],
        'Price': [50, 20, 30, 70, 90, 40],
    })

data = load_dummy_data()

# Sidebar for navigation
st.sidebar.title("Navigation")
pages = {
    "Sales Dashboard": "dashboard",
    "Inventory Management": "inventory",
    "Executive Insights": "insights"
}
page = st.sidebar.radio("Go to", list(pages.keys()))

# Define each page function
def sales_dashboard():
    st.title("📊 Sales Dashboard")
    st.markdown("### Analyze sales trends and performance metrics.")

    # Filter data
    marketing_group = st.sidebar.selectbox("Select Marketing Group", data['Marketing_Group'].unique())
    classified_category = st.sidebar.selectbox("Select Classified Category", data['Classified_Category'].unique())
    filtered_data = data[
        (data['Marketing_Group'] == marketing_group) &
        (data['Classified_Category'] == classified_category)
    ]
    st.dataframe(filtered_data)

    # Sales Trend Analysis
    st.subheader("Sales Trend Analysis")
    monthly_sales = filtered_data.groupby(['Month_Name', 'Brand'])['Quantity_Sold'].sum().reset_index()
    if not monthly_sales.empty:
        st.line_chart(monthly_sales.pivot(index='Month_Name', columns='Brand', values='Quantity_Sold').fillna(0))
    else:
        st.write("No data available for the selected filters.")

def inventory_management():
    st.title("📦 Inventory Management")
    st.markdown("### Monitor stock levels and inventory turnover.")
    
    # Inventory overview
    st.subheader("Inventory Overview")
    inventory_stats = data[['Brand', 'Quantity_In_Stock', 'Price']].copy()
    inventory_stats['Value'] = inventory_stats['Quantity_In_Stock'] * inventory_stats['Price']
    st.dataframe(inventory_stats)

    st.subheader("Stock-Out Alerts")
    stock_out_alerts = data[data['Quantity_In_Stock'] == 0]
    if not stock_out_alerts.empty:
        st.warning("Some brands are out of stock!")
        st.dataframe(stock_out_alerts)
    else:
        st.success("No stock-outs detected.")

def executive_insights():
    st.title("💡 Executive Insights")
    st.markdown("### Gain insights and recommendations powered by AI.")
    
    questions = [
        "Which products contribute most to revenue?",
        "What are the best-selling categories and brands?",
        "Which inventory items have the highest turnover rates?",
    ]
    for i, question in enumerate(questions, start=1):
        st.subheader(f"Insight {i}: {question}")
        st.text("Generated AI-driven recommendations would appear here (requires OpenAI API key).")
        st.info("AI integration is currently mocked for this demo.")

# Page routing
if page == "Sales Dashboard":
    sales_dashboard()
elif page == "Inventory Management":
    inventory_management()
elif page == "Executive Insights":
    executive_insights()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info("This is a multi-page Streamlit application for fashion sales analytics.")
