import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

# load berkas main_data.csv sebagai sebuah DataFrame
day_df = pd.read_csv('./data/day.csv')
hour_df = pd.read_csv('./data/hour.csv')

# membuat filter dengan widget date input serta menambahkan logo perusahaan pada sidebar
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()

with st.sidebar:
  # Menambahkan logo perusahaan
  st.image('./data/dataset-cover.jpeg')
  
  # Mengambil start_date & end_date dari date_input
  start_date, end_date = st.date_input(
    label='Range of date',min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
  )

# Data yang telah difilter ini selanjutnya akan disimpan dalam pattern_df
pattern_df = day_df[(day_df['dteday'] >= str(start_date)) & (day_df['dteday'] <= str(end_date))]

# menambahkan header pada dashboard tersebut.
st.header('Bike Sharing Dashboard :bike:')

# pola peminjaman sepeda antara pengguna casual dan pengguna terdaftar
st.subheader('Bicycle Rental Patterns between Casual and Registered Users (filtered by date)')
plt.figure(figsize=(10, 6))
plt.plot(pattern_df['dteday'], pattern_df['casual'], color='blue', label='Casual Users')
plt.plot(pattern_df['dteday'], pattern_df['registered'], color='green', label='Registered Users')
plt.xlabel('Date')
plt.ylabel('Number of Rental Bikes')
plt.title('Bicycle Rental Patterns between Casual and Registered Users')
plt.legend()
plt.grid(True)
plt.tight_layout()
st.pyplot(plt)

# jumlah rental sepeda berdasarkan cuaca perhari
st.subheader('Daily Number of Rental Bikes by Weather')
byweather_df = pd.DataFrame(day_df.groupby(by='weathersit')['cnt'].sum().sort_values(ascending=False).reset_index())
byweather_df.weathersit = byweather_df.weathersit.map({1: 'Sunny', 2: 'Foggy', 3: 'Rainy', 4: 'Stormy'})
byweather_df.rename(columns={'weathersit': 'weather', 'cnt': 'rental_bikes_count'}, inplace=True)
plt.figure(figsize=(10, 5))
colors = ['#72BCD4', '#D3D3D3', '#D3D3D3']
sns.barplot(
  y='rental_bikes_count',
  x='weather',
  hue='weather',
  data=byweather_df,
  palette=colors,
)
plt.title('Daily Number of Rental Bikes by Weather', loc='center', fontsize=15)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='x', labelsize=12)
st.pyplot(plt)

# Tren rental sepeda berdasarkan cuaca perjam
st.subheader('Hourly Bike Rental Trends by Weather Type')
weather_trend = pd.DataFrame(hour_df.groupby(['hr', 'weathersit'])['cnt'].sum().unstack())
weather_trend.rename(columns={1: 'Sunny', 2: 'Foggy', 3: 'Rainy', 4: 'Stormy'}, inplace=True)
weather_trend.index = weather_trend.index.astype(str)
weather_trend.plot(figsize=(10, 5))
plt.xlabel('Hour')
plt.ylabel('Total Rentals')
plt.title('Hourly Bike Rental Trends by Weather Type')
plt.legend(title='Weather Situation')
st.pyplot(plt)
