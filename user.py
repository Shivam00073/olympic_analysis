import streamlit as st
import pandas as pd
import preprocessor,helper
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import plotly.figure_factory as ff

df=pd.read_csv('athlete_events.csv')
region_df=pd.read_csv('noc_regions.csv')


df=preprocessor.preprocessor(df,region_df)

st.sidebar.title('Olympic Analysis')
st.sidebar.image('blue-81847_960_720.jpg')

user=st.sidebar.radio(
    'Select an Option ',('Medal Tally','Overall Analysis','Country_wise Analysis','Athelet wise Analysis')
)
medal_tally=helper.medal_tally(df)


if user == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    country,year=helper.country_year_list(df)
    selected_country=st.sidebar.selectbox('Select the Country',country)

    selected_year=st.sidebar.selectbox('Select the Year', year)
    medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally in '+ str(selected_year))
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country+' '+'Overall performance')
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(str.upper(selected_country) +' '+ ' performance in ' + str(selected_year)+ ' '+'Olympics')



    st.table(medal_tally)

if user =='Overall Analysis':
    edition=df['Year'].nunique() - 1
    cities=df['City'].unique().shape[0]
    sports=df['Sport'].unique().shape[0]
    events=df['Event'].unique().shape[0]
    regions=df['region'].unique().shape[0]
    athletes=df['Name'].unique().shape[0]

    col1,col2,col3=st.columns(3)
    with col1:
        st.header('Editions')
        st.title(edition)
        year_names = st.checkbox('See years')
        if year_names:
            st.table(df['Year'].unique())
    with col2:
        st.header('City')
        st.title(cities)
        cit_names= st.checkbox('Name of Cities')
        if cit_names:
            st.table(df['City'].unique())
    with col3:
        st.header('Sport')
        st.title(sports)
        sport_names = st.checkbox('See sport name')
        if sport_names:
            st.table(df['Sport'].unique())

    col1,col2,col3=st.columns(3)
    with col1:
        st.header('Event')
        st.title(events)
        year_names = st.checkbox('See Events')
        if year_names:
            st.table(df['events'].unique())
    with col2:
        st.header('Regions')
        st.title(regions)
        cit_names= st.checkbox('Name of Regions')
        if cit_names:
            st.table(df['region'].unique())
    with col3:
        st.header('Athletes')
        st.title('{:,}'.format(athletes))
        sport_names = st.checkbox('See Names')
        if sport_names:
            st.table(df['Name'].unique())

    nations_over_time=helper.countries_over_time(df)
    st.title('Nation Participated Over The Years')
    fig=px.line(nations_over_time,x='Edition',y='Countries_over_time')
    st.plotly_chart(fig)

    event_over_time=helper.events_over_time(df)
    st.title('Events Over The Years')
    fig = px.line(event_over_time, x='Year', y='Event_over_time')
    st.plotly_chart(fig)

    athletes_over_time=helper.athletes_over_time(df)
    st.title('Athelets Over The Years')
    fig = px.line(athletes_over_time, x='Year', y='Athletes_over_time')
    st.plotly_chart(fig)

    st.title('Events over the Years')
    fig,ax=plt.subplots(figsize=(25,25))
    yx=df.drop_duplicates(['Year', 'Event', 'Sport'])
    ax=sns.heatmap(yx.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    st.title('Most Successfull Athelets')
    sel_val=st.selectbox('Select the sport',df.Sport.unique().tolist())
    mo_suc=helper.most_successfull(df,sel_val)
    st.table(mo_suc)


if user=='Country_wise Analysis':
    select_country = st.sidebar.selectbox('Select the country', df.region.dropna().unique().tolist())
    st.title('Year wise Medal Tally of'+' '+ select_country)
    st.header('Medal Tally over the years')

    final_df = helper.country_wise_medal(df, select_country)
    fig = px.line(final_df, x='Year', y='Medal')
    st.plotly_chart(fig)

    st.title('Performance in different sports of '+' '+ select_country)

    fig,ax=plt.subplots(figsize=(25,25))
    pvt=helper.country_event_heatmap(df,select_country)
    ax=sns.heatmap(pvt,annot=True)
    ax.set_yticklabels(ax.get_ymajorticklabels(), fontsize=18)
    ax.set_xticklabels(ax.get_xmajorticklabels(), fontsize=16)

    st.pyplot(fig)

    st.title('Top 15 Athletes of '+' '+select_country)
    top_10_df=helper.top_athletes_country_wise(df,select_country)
    st.table(top_10_df)

if user=='Athelet wise Analysis':
    st.title('Athelet wise Analysis')
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x = athlete_df['Age'].dropna()
    x1 = athlete_df[athlete_df['Medal'] == "Gold"]['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == "Silver"]['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == "Bronze"]['Age'].dropna()
    fig = ff.create_distplot([x, x1, x2, x3], ['Age_Distribution', 'Gold', 'Silver', 'Bronze'], show_hist=False,
                             show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.header('Age Distribution')
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)
    fig=ff.create_distplot(x,name,show_hist=False,show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.header('Age Distribution wrt Sport(Gold Medalist)')
    st.plotly_chart(fig)

    st.header('Height and Weight Distribution')
    famous_sports.insert(0,'Overall')
    select_val=st.selectbox('Select the Sport',famous_sports)
    plt.figure(figsize=(15,15))
    temp_df=helper.weight_v_height(df,select_val)
    fig,ax=plt.subplots(figsize=(15,15))
    ax=sns.scatterplot(temp_df['Weight'], temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'],s=100)
    st.pyplot(fig)

    st.header('Male vs Female Participation Over the Years')
    final=helper.men_vs_women(df)
    fig=px.line(final,x='Year',y=['Male','Female'])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)



