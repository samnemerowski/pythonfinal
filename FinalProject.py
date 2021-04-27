"""
Sam Nemerowski
Professor Masloff
CS230 Final Project
"""

import pandas as pd
import matplotlib.pyplot as plt
import statistics
import streamlit as st
import numpy as np
import pip

csv = pd.read_csv("craigslistcars.csv")
data = csv.drop(columns="description")


def default_input(prompt, value):
    statement = input(f"{prompt} - [Press Enter for {value}] ")
    if statement == "":
        statement = value
    return statement


def uppercase(options):
    upper = [item.capitalize for item in options]
    return upper


def descriptive_statistics():
    pricing = data["price"].tolist()
    x = statistics.mean(pricing)
    y = statistics.median(pricing)
    z = statistics.stdev(pricing)
    st.title(f"Descriptive Statistics")
    st.write(f"Mean car price:                      ${x:,.2f}")
    st.write(f"Median car price:                    ${y:,.2f}")
    st.write(f"Standard deviation of car prices:    ${z:,.2f}")


def simple_map():
    MAPKEY = "pk.eyJ1IjoiY2hlY2ttYXJrIiwiYSI6ImNrOTI0NzU3YTA0azYzZ21rZHRtM2tuYTcifQ.6aQ9nlBpGbomhySWPF98DApk.eyJ1IjoiY2hlY2ttYXJrIiwiYSI6ImNrOTI0NzU3YTA0azYzZ21rZHRtM2tuYTcifQ.6aQ9nlBpGbomhySWPF98DA"
    orig_data = pd.read_csv("craigslistcars.csv")
    revised_data = orig_data.dropna()
    locations = zip(revised_data["lat"], revised_data["lon"])
    df = pd.DataFrame(locations, columns=["lat", "lon"])
    st.title("Used Cars Across America")
    st.map(df)


def choose_price():
    selected_price = st.sidebar.slider("Select your price range", 0, 100000, (0, 100000))
    return selected_price


def histogram():
    hist_values = np.array(data["price"])
    fig, ax = plt.subplots()
    bins_list = []
    for num in range(1, 90000, 10000):
        bins_list.append(num)
    ax.hist(hist_values, bins=bins_list, color="r")
    ax.set_xticks = bins_list
    st.title("Histogram of Used Cars by Price")
    ax.set_xlabel("Car Prices")
    ax.set_ylabel("Frequency")
    plt.figure(figsize=(15, 15))
    st.pyplot(fig)


def pie_chart():
    info = pd.read_csv("craigslistcars.csv")
    cars_chosen = st.sidebar.multiselect("Select the manufacturers you'd like to see in the pie chart", manufacturers)
    info = info.loc[info["manufacturer"].isin(cars_chosen)]
    info["index_col"] = info.index
    cars = info["manufacturer"].value_counts()
    plt.figure(figsize=(15, 15))
    explode = np.zeros(len(cars_chosen))
    color_options = ["gray", "blue", "lightskyblue", "lightpink", "lightgreen", "lightblue", "steelblue", "purple", "cyan", "magenta", "wheat", "salmon"]
    labels = cars_chosen
    plt.pie(cars, labels=labels, startangle=90, explode=explode, colors=color_options, autopct='%1.1f%%', shadow=False, labeldistance=1.1, textprops={'fontweight': 'bold', 'fontsize': 18}, wedgeprops={"linewidth": 3, "edgecolor": "k"})
    plt.legend(loc="best", fontsize=15)
    st.title("Used Car Ads by Select Manufacturers")
    plt.axis("equal")
    st.pyplot(plt)


def main():
    st.title("Used Cars in America")
    st.write("Scroll to learn about your options and use the sidebar to find your perfect car!")
    st.sidebar.title("See if there's a car for you!")
    pie_chart()
    simple_map()
    descriptive_statistics()
    histogram()
    selected_manufacturer = st.sidebar.selectbox("Which manufacturer would you like?", manufacturers)
    data2 = data[data.manufacturer == selected_manufacturer]
    st.write(data2)
    selected_state = st.sidebar.selectbox("Which state would you like to purchase from?", states)
    data2 = data2[data2.state == selected_state]
    st.write(data2)
    selected_color = st.sidebar.selectbox("What color do you want your car to be?", colors)
    data2 = data2[data2.paint_color == selected_color]
    st.write(data2)
    selected_price = choose_price()
    data2 = data2[data2.price > selected_price[0]]
    data2 = data2[data2.price < selected_price[1]]
    if len(data2) > 0:
        st.write("Congrats! There is a car for you!")
    else:
        st.write("Sorry, we don't have a car for you.")
    st.write(data2)


states = data["state"].unique()
years = data["year"].tolist()
manufacturers = data["manufacturer"].unique()
manufacturers_list = data["manufacturer"].tolist()
models = data["model"].tolist()
colors = data["paint_color"].unique()
prices = data["price"].tolist()

main()
