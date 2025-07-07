import streamlit as st
from helperfile import load_data
st.set_page_config("Dashboard Sales and Weather", page_icon=":money:",
                   layout="wide")

df_retail_weekly = load_data(file_name="aggregated_weekly")
df_retail_monthly = load_data(file_name="aggregated_monthly")

df_retail_weekly_stores = load_data(file_name="aggregated_weekly_stores")
df_retail_monthly_stores = load_data(file_name="aggregated_monthly_stores")

df_retail_weekly_products = load_data(file_name="aggregated_weekly_pc")
df_retail_monthly_products = load_data(file_name="aggregated_monthly_pc")

stores = df_retail_monthly_stores["store_id"].unique()
products = df_retail_monthly_products["product_id"].unique()

st.title("Effects of Weather on Sales")
st.markdown("In this part, we check whether weather has any effects on\
            sales (`revenue` or `sold items`). This may also be checked\
            either overall or only for specific products or stores. ")
granularity = st.radio(label="Choose granularity of data: ",
                       options=["weekly", "monthly"], horizontal=True)
if granularity == "weekly":
    df = df_retail_weekly
else:
    df = df_retail_monthly

IV = st.selectbox(label="Variable on X-axis:",
                  options=["temperature", "humidity", "wind_speed"])
DV = st.selectbox(label="Variable on Y-axis:",
                  options=["quantity_sold", "revenue"])

st.header(f"Overall Correlation between {IV} and {DV}")
corr_estimate = df[[IV, DV]].corr(method="spearman")[IV][1]
st.markdown(f"Spearman Correlation: r={corr_estimate:.3f}")
st.scatter_chart(data=df, x=IV, y=DV)

st.divider()
st.subheader("Check the realtionship for only a given store or product: ")
selected_store = st.selectbox(label="Choose Store:", options=stores,
                              index=None,
                              placeholder="Choose a StoreID first.")

if selected_store:
    if granularity == "weekly":
        df = df_retail_weekly_stores
    else:
        df = df_retail_monthly_stores
    filt_stores_df = df.loc[lambda x: x["store_id"] == selected_store]
    corr_store = filt_stores_df[[IV, DV]].corr(method="spearman")[IV][1]

    st.header(f"Correlation for store {selected_store}")
    st.markdown(f"Spearman Correlation: r={corr_store:.3f}")
    st.scatter_chart(data=filt_stores_df, x=IV, y=DV)

selected_product = st.selectbox(label="Choose Product:", options=products,
                                index=None,
                                placeholder="Choose a product first.")
if selected_product:
    if granularity == "weekly":
        df = df_retail_weekly_products
    else:
        df = df_retail_monthly_products
    filt_products_df = (df.loc[lambda x: x["product_id"] == selected_product])
    corr_products = filt_products_df[[IV, DV]].corr(method="spearman")[IV][1]

    st.header(f"Correlation for product {selected_product}")
    st.markdown(f"Spearman Correlation: r={corr_products:.3f}")
    st.scatter_chart(data=filt_products_df, x=IV, y=DV)
