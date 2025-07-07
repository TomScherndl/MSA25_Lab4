import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from helperfile import load_data
st.set_page_config("Dashboard Sales and Weather", page_icon=":money:",
                   layout="wide")

df_weather = load_data(file_name="weather_aggregated", type="weather")
df_weather_weekly = load_data(file_name="aggregated_weekly", type="retail")
df_weather_monthly = load_data(file_name="aggregated_monthly", type="retail")

tab0, tab1, tab2 = st.tabs(["Overview", "Wind Data Count",
                            "Temperature and Humidity"])

with tab0:
    st.title("🌟 Gold Layer Weather Data Dashboard: WIND")
    st.markdown(f"""The following windy day categories were available:
        {df_weather["wind_category"].unique()}.
    For an overview, see the following table:""")
    st.dataframe(df_weather, hide_index=True)

with tab1:
    st.title("Wind Categories - Count")
    st.subheader("📊 Count by Wind Category")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=df_weather, x="wind_category", y="count",
                palette="coolwarm",
                ax=ax, hue="wind_category")
    st.pyplot(fig)

    st.subheader("📊 Aggregated Data Overview")
    wind_categories = df_weather["wind_category"].unique()
    selected_category = st.selectbox("Select Wind Category", wind_categories)

    filtered_df = (df_weather
                   .loc[lambda x: x["wind_category"] == selected_category])
    st.dataframe(filtered_df, hide_index=True)

    st.write("🔄 Data auto-refreshes when reloaded.")

with tab2:
    st.title("Wind Categories - Temperature and Humidity")
    st.markdown("## Average Temperature and Humidity")
    col = st.columns((1, 1), gap="medium")
    with col[0]:
        st.scatter_chart(data=df_weather, y="wind_category", x="avg_temp",
                         y_label="Wind Category", x_label="Temperature (°C)")
    with col[1]:
        st.scatter_chart(data=df_weather, y="wind_category", x="avg_humidity",
                         y_label="Wind Category", x_label="Humidity (g/m³)")

    granularity_weather = st.radio(label="Granularity of Time: ",
                                   options=["weekly", "monthly"],
                                   horizontal=True)

    if granularity_weather == "weekly":
        st.markdown("## Change over time (weekly change)")
        df = df_weather_weekly
    else:
        st.markdown("## Change over time (monthly change)")
        df = df_weather_monthly

    col = st.columns((1, 1, 1), gap="small", border=True)

    with col[0]:
        st.line_chart(data=df, x="date", y="temperature",
                      x_label="Time", y_label="Temperature (°C)")
    with col[1]:
        st.line_chart(data=df, x="date", y="humidity",
                      x_label="Time", y_label="Humidity (g/m³)")
    with col[2]:
        st.line_chart(data=df, x="date", y="wind_speed",
                      x_label="Time", y_label="Humidity (g/m³)")
