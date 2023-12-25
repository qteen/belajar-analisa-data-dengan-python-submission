import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

def create_monthly_growth_df(day_df):
    monthly_growth_df = day_df.resample(rule='M', on='dteday').agg({
        'casual': 'sum',
        'registered': 'sum'
    })
    monthly_growth_df.index = monthly_growth_df.index.strftime('%Y-%m')
    monthly_growth_df = monthly_growth_df.reset_index()
    monthly_growth_df.rename(columns={
        'dteday': 'year_month',
        'casual': 'total_casual',
        'registered': 'total_registered'
    }, inplace=True)
    
    return monthly_growth_df

def create_season_average_df(day_df):
    season_avg_df = day_df.groupby(by="season_nm").cnt.mean()
    season_avg_df = season_avg_df.reset_index()
    season_avg_df.rename(columns={
        'cnt': 'average_consumer'
    }, inplace=True)
    
    return season_avg_df

def create_temperature_average_df(day_df):
    temp_avg_df = day_df.groupby(by="temp_val").cnt.mean()
    temp_avg_df = temp_avg_df.reset_index()
    temp_avg_df.rename(columns={
        'cnt': 'average_consumer',
        'temp_val': 'temperature'
    }, inplace=True)

    return temp_avg_df

if __name__=='__main__':
    day_df = pd.read_csv("dashboard/important_day_df.csv")
    day_df.sort_values(by="dteday", inplace=True)
    day_df.reset_index(inplace=True)
    day_df["dteday"] = pd.to_datetime(day_df["dteday"])

    min_date = day_df["dteday"].min()
    max_date = day_df["dteday"].max()

    data = {}
    with st.sidebar:
        st.title("Qteen")
        # Mengambil start_date & end_date dari date_input
        result = st.date_input(
            label='Rentang Waktu',min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )
        if isinstance(result, tuple) and len(result)>1:
            start_date, end_date = result
            main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                    (day_df["dteday"] <= str(end_date))]
            data['monthly_growth_df'] = create_monthly_growth_df(main_df)
            data['season_average_df'] = create_season_average_df(main_df)
            data['temp_average_df'] = create_temperature_average_df(main_df)

    with st.container():
        st.header('Qteen Submission Dashboard :sparkles:')

        st.subheader("Monthly Consumer Growth")
        if 'monthly_growth_df' in data:
            fig, ax = plt.subplots(figsize=(18, 8))
            ax.plot(data['monthly_growth_df']["year_month"], data['monthly_growth_df']["total_casual"], marker='o', linewidth=2, color="red")
            ax.plot(data['monthly_growth_df']["year_month"], data['monthly_growth_df']["total_registered"], marker='o', linewidth=2, color="blue") 
            ax.tick_params(axis='y', labelsize=20)
            ax.tick_params(axis='x', labelsize=10)
            st.pyplot(fig)

        st.subheader("Season Usage Average")
        if 'season_average_df' in data:
            colors = ["green", "red", "yellow", "orange"]
            fig, ax = plt.subplots(figsize=(18, 8))
            ax.barh(data['season_average_df']["season_nm"], data['season_average_df']["average_consumer"], color=colors)
            ax.tick_params(axis='y', labelsize=20)
            ax.tick_params(axis='x', labelsize=10)
            st.pyplot(fig)

        st.subheader("Temperature Usage Average")
        if 'temp_average_df' in data:
            fig, ax = plt.subplots(figsize=(18, 8))
            # plt.bar(data['temp_average_df']["temperature"], data['temp_average_df']["average_consumer"], color="orange")
            sns.regplot(x="temperature", y="average_consumer", data=data['temp_average_df'].sort_values(by="temperature", ascending=True), ax=ax)
            ax.tick_params(axis='y', labelsize=20)
            ax.tick_params(axis='x', labelsize=10)
            st.pyplot(fig)

    st.divider()
    st.caption('Copyright (c) Qteen 2023')