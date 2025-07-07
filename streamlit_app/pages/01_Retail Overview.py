import streamlit as st
from helperfile import load_data
st.set_page_config("Dashboard Sales and Weather", page_icon=":money:",
                   layout="wide")

st.title("Retail Data")

# get data
df_retail_overview = load_data(file_name="aggregated_overall")
df_retail_pc = load_data(file_name="aggregated_pc")
df_retail_rc = load_data(file_name="aggregated_store")
df_retail_weekly = load_data(file_name="aggregated_weekly")
df_retail_monthly = load_data(file_name="aggregated_monthly")

df_retail_weekly_pc = load_data(file_name="aggregated_weekly_pc")
df_retail_monthly_pc = load_data(file_name="aggregated_monthly_pc")
df_retail_weekly_stores = load_data(file_name="aggregated_weekly_stores")
df_retail_monthly_stores = load_data(file_name="aggregated_monthly_stores")

# general info to use in text
products = df_retail_pc["product_id"].unique()
num_products = len(products)
stores = df_retail_rc["store_id"].unique()
num_stores = len(stores)

tab0, tab1, tab2 = st.tabs(["Overview", "Product Category",
                            "Store Overview"])
with tab0:
    st.title("🌟 Gold Layer Sales Data Dashboard")
    st.markdown(f"""We have **{num_products}** products in our portfolio.
        which we sell from **{num_stores}** different stores.""")

    st.subheader("Retail and Sales Data")
    cols = st.columns((1, 1, 1, 1), gap="small", border=True)
    with cols[0]:
        st.metric(label="Number of Products",
                  value=num_products)
    with cols[1]:
        st.metric(label="Number of Stores",
                  value=num_stores)
    with cols[2]:
        st.metric(label="Sum of Revenues",
                  value=int(round(sum(df_retail_pc["revenue"]), 0)))
    with cols[3]:
        st.metric(label="Sum of Sold Items",
                  value=sum(df_retail_pc["quantity_sold"]))
    st.subheader("Weather Data")
    cols_temp = st.columns((1, 1, 1), gap="small", border=True)
    with cols_temp[0]:
        st.metric(label="Average Temperature",
                  value=round(df_retail_overview[0]["temperature"], 2))
    with cols_temp[1]:
        st.metric(label="Average Wind Speed",
                  value=round(df_retail_overview[0]["wind_speed"], 2))
    with cols_temp[2]:
        st.metric(label="Average Humidity",
                  value=round(df_retail_overview[0]["humidity"], 2))
    with st.expander(label="Show Data"):
        st.dataframe(df_retail_overview)
with tab1:
    st.subheader("📊 Aggregated Data Overview per Product")
    selected_product = st.selectbox("Select Product", products)

    st.divider()
    st.subheader(f"Sales over Time for Product {selected_product}")
    granularity_sales = st.radio(label="Data Granularity: ", horizontal=True,
                                 options=["weekly", "monthly"], key="sot_p")

    if granularity_sales == "weekly":
        filtered_df = df_retail_weekly_pc
    else:
        filtered_df = df_retail_monthly_pc
    # filter based on selected product
    filtered_df = (filtered_df
                   .loc[lambda x: x["product_id"] == selected_product])
    with st.expander(label="Show Data"): 
        st.dataframe(filtered_df, hide_index=True)
    st.subheader(f"Revenue for Product {selected_product}")
    st.line_chart(data=filtered_df, x="date", y="revenue",
                  x_label="Date", y_label="Revenue")
    st.subheader(f"Quantity Sold for Product {selected_product}")
    st.line_chart(data=filtered_df, x="date", y="quantity_sold",
                  x_label="Date", y_label="#Sold")

with tab2:
    st.subheader("📊 Aggregated Data Overview per Store")
    selected_store = st.selectbox("Select Store", stores)

    st.divider()
    st.subheader(f"Sales over Time for Store {selected_store}")
    granularity_stores = st.radio(label="Data Granularity: ", horizontal=True,
                                  options=["weekly", "monthly"], key="sot_s")

    if granularity_stores == "weekly":
        filtered_df = df_retail_weekly_stores
    else:
        filtered_df = df_retail_monthly_stores
    # filter based on selected product
    filtered_df = (filtered_df
                   .loc[lambda x: x["store_id"] == selected_store])

    with st.expander("Show Data"):
        st.dataframe(filtered_df, hide_index=True)
    st.subheader(f"Revenue for Store {selected_store}")
    st.line_chart(data=filtered_df, x="date", y="revenue",
                  x_label="Date", y_label="Revenue")
    st.subheader(f"Quantity Sold for Store {selected_store}")
    st.line_chart(data=filtered_df, x="date", y="quantity_sold",
                  x_label="Date", y_label="#Sold")
