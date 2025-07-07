import streamlit as st

st.set_page_config("Dashboard Sales and Weather", page_icon=":money:",
                   layout="wide")
st.title("Welcome to our Dashboard!")
st.write("Authors: Jakob Staudinger & Tom Scherndl")
st.markdown("""
In this dashboard you find all relevant business data of our ficitious\
company. In the **left sidebar** you see multiple pages structuring the data\
into 3 components:

* **Retail Data**:  All products that have been sold in the last months.
* **Weather Data:**: Obviously, this is very important for our business(?)...
* **Combination of Weather and Retail Data**: To check whether the weather \
has an effect on our sales and revenue.

## Aims and Scope of the dashboard
1) Visualizing the overall sold items and revenues.
2) Visualizing the weather for the observation period.
3) Show whether weather variables have an effect on sales (revenue or sales)

Just click on the respective section and have fun exploring and interacting \
with the dashboard. """)
