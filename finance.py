import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.title("Stock Price Analysis App")

# User Inpuut Dataset // Global Variables
st.subheader("Enter your datafile name")
data = st.text_input("CSV format only","Example: stock.csv")
st.write("Your Dataset is: ",data)
st.write("----------------------------")


# Display df head and tail)
try:
    df = pd.read_csv(data,index_col="Date",parse_dates=True)
    func_cols = df.columns
    st.markdown("Head samples")
    st.write(df.head(3))

    st.markdown("Tail samples")
    st.write(df.tail(3))
    st.markdown("Correlation Between Columns")
    st.write(df.corr())
    st.success("Data loaded successfully")

except:
    st.error("Dataset Error(Check Your Input)")
st.write("----------------------------")
### Add Data PreProcessing Pipeline in the future!!


### Add Data PreProcessing Pipeline in the future!!
st.header("Visualizations")
st.subheader("Line Plot")

if st.checkbox("Display Line Plot"):
    st.write("Full View")
    df.plot(title ="Stock Price Protfolio")
    st.pyplot()

    if st.checkbox("Individual View"):
        for x in df.columns:
            df[x].plot(title = x)
            st.pyplot()
    else:
        pass
st.write("----------------------------")
# Moving Average for 5,30,90
st.subheader("Trend Using Moving Average")

def moving_average(data):
    for x in func_cols:
        data["{}_{}".format(x,"5-Days")] = data[x].rolling(5).mean()
        data["{}_{}".format(x,"20-Days")] = data[x].rolling(20).mean()
        data["{}_{}".format(x,"60-Days")] = data[x].rolling(60).mean()
    return data

# Add Rolling Columns
if st.checkbox("Calculate Moving Average"):
    df = moving_average(df)
    st.dataframe(df.head(5))
    st.success("Calculation Completed")
    st.info("Moving Average is calculated in [5,20,60] Days respectfully")


if st.checkbox("Trends"):
    df = moving_average(df)
    st.markdown("General Trend(s)")
    columns = st.multiselect("Choose The Desired Columns: ",[cols for cols in df.columns])

    for x in columns:
        df[x].plot(title = x)
        st.pyplot()
else:
    pass


st.write("----------------------------")
# Basic analysis
# Daily Percentage Change
def daily_percentage(data):
    for i in func_cols:
        data["{}_{}".format(i,"Daily_Return")] = data[i].pct_change(1)
    return(data)

st.subheader("Daily Return")

if st.checkbox("Calculate Daily Return"):
    df = daily_percentage(df)
    st.dataframe(df.head(5))
    st.success("Calculation Completed")

if st.checkbox("Distribution"):
    df = daily_percentage(df)
    st.markdown("Distribution")
    columns = st.multiselect("Choose Desired Columns",[cols for cols in df.columns])

    for x in columns:
        df[x].plot(kind ="kde",title = x)
        st.text("{} \n Max Return: {} // Minimum Return: {}".format(x,round(df[x].max(),2),round(df[x].min(),2)))
        st.pyplot()
else:
    pass
st.write("----------------------------")
# Cumulative Daily return

def cumulative(data):
    for i in func_cols:
        data["{}_{}".format(i,"Daily_Return")] = data[i].pct_change(1)
        data["Cumulative Returns {}".format(i)]  = (1+data["{}_{}".format(i,"Daily_Return")]).cumprod()
    return (data)

st.subheader("Cumulative Daily Return")

if st.checkbox("Calculate Cumulative Return"):
    df = cumulative(df)
    st.dataframe(df.head(5))
    st.success("Calculation Completed")

if st.checkbox("Cumulative Trend"):
    df = cumulative(df)
    st.markdown("Trends")
    columns = st.multiselect("Choose Desired Columns",[cols for cols in df.columns])

    for x in columns:
        df[x].plot(title = x)
        st.text("Fst Date:{}\nLst Date:{}".format(df.index[1],df.index[-1]))

        st.text("Current {}:{} Equals {}".format(x,df[x].index[-1],round(df[x][-1],2)))
        st.pyplot()
else:
    pass


# calculate Profit
st.write("----------------------------")
st.header("Cumulative Profit Calculation")

stock_ops = st.multiselect("Choose Stock(s) to Invest",[x for x in func_cols])
for num in range(len(stock_ops)):
    df = cumulative(df)
    option = st.selectbox("Select Cumulative Return",[x for x in df.columns[len(func_cols):]],key = stock_ops[num])
    invest = st.number_input("Input Dollars",key = stock_ops[num])
    st.write(option,"\n has a cumulative return of",round(df[option][-1],2),
            "You Invested",stock_ops[num],"for",invest)

    st.write("Total Return in Dollars are",round(df[option][-1]*invest,2))

st.write("----------------------------")
st.subheader("Export Dataset")

## Updating Export Function in the Future

def export_data(data):
    for x in func_cols:
        data["{}_{}".format(x,"5-Days")] = data[x].rolling(5).mean()
        data["{}_{}".format(x,"20-Days")] = data[x].rolling(20).mean()
        data["{}_{}".format(x,"60-Days")] = data[x].rolling(60).mean()
        data["{}_{}".format(x,"Daily_Return")] = data[x].pct_change(1)
        data["{}_{}".format(x,"Daily_Return")] = data[x].pct_change(1)
        data["Cumulative Returns {}".format(x)]  = (1+data["{}_{}".format(x,"Daily_Return")]).cumprod()

    return(data)

if st.button("See Final Dataset"):
    df = export_data(df)
    st.dataframe(df.head())

if st.button("Download"):
    df.to_csv("New_Dataset_{}".format(data))
    st.success("Download successfully")
