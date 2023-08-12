import pandas as pd
import plotly.express as px
import streamlit as st

st.title("app with plotly and streamlit")
df = px.data.gapminder()
st.write(df.head())

st.write(df.columns)

# summary stats\
st.write(df.describe())

year_option = df['year'].unique().tolist()
year = st.selectbox("Which year do u want to plot?", year_option, 0)
#df = df[df['year']==year]

fig = px.scatter(df, x='gdpPercap', y = 'lifeExp', size = 'pop', color = 'country', hover_name= 'country', log_x = True, size_max= 55, range_x = [100, 1000], range_y = [20, 90], animation_frame = 'year', animation_group = 'country' )
st.write(fig)


