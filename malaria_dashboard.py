import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

#Page Settings
st.set_page_config(page_title="Sri Lanka Malaria Dashboard 🇱🇰", layout="wide")

#Load Data
df = pd.read_csv("cleaned_malaria_data.csv")

#Title & Introduction
st.title("Sri Lanka Malaria Indicators Dashboard")
st.markdown("""
Welcome to the Sri Lanka Malaria Indicators Dashboard.  
This dashboard presents trends and summaries from national malaria data, helping to monitor and evaluate key public health indicators over time.
""")

#Dropdown to Explore Specific Indicator 
st.subheader(" Explore a Specific Indicator")

# Filter by indicator
selected = st.selectbox("Choose an Indicator", sorted(df['indicator_name'].unique()))
df_sel = df[df['indicator_name'] == selected]

# Year filter
year_min, year_max = int(df['year'].min()), int(df['year'].max())
year_range = st.slider("Select Year Range", year_min, year_max, (year_min, year_max))
df_sel = df_sel[df_sel['year'].between(year_range[0], year_range[1])]

# Line chart for selected indicator
fig_sel = px.line(df_sel, x='year', y='value', title=f"{selected} Over Time", markers=True)
st.plotly_chart(fig_sel, use_container_width=True)


#Total Values Over Time
st.subheader("Total Malaria-Related Values Over Time")
df_yearly = df.groupby('year', as_index=False)['value'].sum()
fig_total = px.line(df_yearly, x='year', y='value',
                    title='Total Malaria-Related Values Over Time',
                    markers=True,
                    labels={'value': 'Total Value', 'year': 'Year'})
st.plotly_chart(fig_total, use_container_width=True)

#Top 5 Indicators Over Time 
st.subheader("Top 5 Malaria Indicators Over Time")
top_indicators = df.groupby('indicator_name')['value'].sum().nlargest(5).index
df_top = df[df['indicator_name'].isin(top_indicators)]
fig_top = px.line(df_top, x='year', y='value', color='indicator_name',
                  title='Top 5 Indicators by Total Value',
                  markers=True,
                  labels={'value': 'Value', 'year': 'Year', 'indicator_name': 'Indicator'})
st.plotly_chart(fig_top, use_container_width=True)

#Total Value by Indicator (Horizontal Bar)
st.subheader("Total Value by Indicator")
fig_bar = px.bar(
    df.groupby('indicator_name')['value'].sum().sort_values(ascending=False).reset_index(),
    x='value',
    y='indicator_name',
    orientation='h',
    title='Total Reported Value by Indicator',
    labels={'value': 'Total Value', 'indicator_name': 'Indicator'}
)
st.plotly_chart(fig_bar, use_container_width=True)

#Heatmap by Year and Indicator 
st.subheader("Indicator Heatmap by Year")
pivot_df = df.pivot_table(values='value', index='indicator_name', columns='year', aggfunc='sum').fillna(0)
fig_heatmap = go.Figure(data=go.Heatmap(
    z=pivot_df.values,
    x=pivot_df.columns,
    y=pivot_df.index,
    colorscale='Blues',
    colorbar=dict(title='Value')
))
fig_heatmap.update_layout(title='Indicator Heatmap by Year')
st.plotly_chart(fig_heatmap, use_container_width=True)


#Raw Data Viewer 
with st.expander(" View Raw Data"):
    st.dataframe(df)

#Footer
st.markdown("---")
st.caption("Data source: [WHO via HumData.org](https://data.humdata.org/dataset/who-data-for-lka/resource/2d7645c4-7dd8-47a4-adfb-e709935ca7a0) | Dashboard by Tehara De Silva")
