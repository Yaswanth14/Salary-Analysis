import pandas as pd
import plotly.express as px 
import streamlit as st 

st.set_page_config(page_title="Software Employee Salary Analysis", page_icon=":bar_chart:", layout="wide")

@st.cache_data
def get_data():
    df = pd.read_csv('employee_stats.csv')
    return df
df = get_data()


# ---- Sidebar ----
st.sidebar.header("Please Filter Here:")

location = st.sidebar.multiselect(
    "Select the Locations:",
    options=df["Location"].unique(),
    default=df["Location"].unique()
)

job = st.sidebar.selectbox(
    "Select the Role Type:",
    options=df["Job_roles"].unique(),
    placeholder="SDE"
)

status = st.sidebar.multiselect(
    "Select Employment Status:",
    options=df["Employment_status"].unique(),
    default=df["Employment_status"].unique()
)


df_selection = df.query(
    "Location == @location & Job_roles == @job & Employment_status == @status"
)



# ----- Main Page ------
st.title(":bar_chart: Salary Analysis")
st.markdown("##")

# Resluts
total_results = len(df_selection)
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:"*int(round(average_rating,0))
average_salary = round(df_selection["Salary"].mean(), 2)

lc, mc, rc = st.columns(3)

with lc:
    st.subheader(f"Total Results: {total_results}")
with mc:
    st.subheader(f"Average Rating: {average_rating} {star_rating}")
with rc:
    st.subheader(f"Average Salary for {job}: {average_salary}") 

st.markdown("---")   

# st.dataframe(df_selection)

# Salary vs Location Box Plot
fig_hist = px.box(
    df_selection, 
    x='Location', 
    y='Salary', 
    range_y=(0,5000000),
    title='<b>Boxplot of Salary by Location</b>'
    )


# Avg. Salary vs Location Line Chart
df_sorted = df_selection.sort_values(by='Location')
average_salary_by_location = df_sorted.groupby('Location')['Salary'].mean().reset_index()
fig_line = px.line(
    average_salary_by_location, 
    x='Location', 
    y='Salary', 
    markers=True, 
    line_shape='linear',
    title='<b>Line Chart of Avg. Salary by Location</b>'
    )

lc, rc = st.columns(2)
lc.plotly_chart(fig_hist, use_container_width=True)
rc.plotly_chart(fig_line, use_container_width=True)


st.header("Other Useful insigts: ")


# Job Roles Pie Chart
df_roles = df.query(
    "Location == @location & Employment_status == @status"
)

job_title_counts = df_roles['Job_roles'].value_counts()
fig_pie = px.pie(
    job_title_counts, 
    names=job_title_counts.index, 
    values=job_title_counts.values,
    color_discrete_sequence=px.colors.qualitative.Pastel,
    title='<b>Pie Chart for Job Role Composition</b>'
    )

# Other Roles Avg. Salary in Barplot
average_salary_df = df_roles.groupby('Job_roles')['Salary'].mean().reset_index()
fig_bar = px.bar(
    average_salary_df, 
    x='Job_roles', 
    y='Salary', 
    color_discrete_sequence=px.colors.qualitative.Pastel,
    title='<b>Average Salary by Job Roles</b>'
    )
# st.plotly_chart(fig_bar)

lc, rc = st.columns(2)
lc.plotly_chart(fig_pie, use_container_width=True)
rc.plotly_chart(fig_bar, use_container_width=True)



footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: #8062D6;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with ❤ by <a style='text-decoration:None; color:pink; text-align: center;' href="https://github.com/Yaswanth14" target="_blank">Yaswanth Modepalli</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)




# ---- Hide Style ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
