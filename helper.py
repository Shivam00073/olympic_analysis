import pandas as pd


def medal_tally(df):

    medal_tally = df.drop_duplicates(subset=['NOC', 'Team', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                             ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    medal_tally['Gold']=medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['Total'] = medal_tally['Total'].astype('int')
    return medal_tally

def country_year_list(df):
    country = df['region'].dropna().unique().tolist()
    country.insert(0, 'Overall')

    year = df['Year'].unique().tolist()
    year.sort()
    year.insert(0, 'Overall')

    return country, year


def fetch_medal_tally(df, year, country):
    medal_tal = df.drop_duplicates(subset=['NOC', 'Team', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    flag = 0

    if year == 'Overall' and country == 'Overall':
        temp_df = medal_tal
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_tal[medal_tal['Year'] == int(year)]
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_tal[medal_tal['region'] == country]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_tal[(medal_tal['region'] == country) & (medal_tal['Year'] == year)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year',
                                                                                    ascending=True).reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x

def countries_over_time(df):
    nation_over_time=df.drop_duplicates(['Year','region'])['Year'].value_counts().reset_index().sort_values('index')
    nation_over_time=nation_over_time.rename(columns={'index':'Edition','Year':'Countries_over_time'})

    return nation_over_time

def events_over_time(df):

    event_over_time = df.drop_duplicates(['Year', 'Event'])['Year'].value_counts().reset_index().sort_values('index')
    event_over_time = event_over_time.rename(columns={'index': 'Year', 'Year': 'Event_over_time'})

    return event_over_time

def athletes_over_time(df):

    athletes_over_time = df.drop_duplicates(['Year', 'Name'])['Year'].value_counts().reset_index().sort_values('index')
    athletes_over_time = athletes_over_time.rename(columns={'index': 'Year', 'Year': 'Athletes_over_time'})

    return athletes_over_time


def most_successfull(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'region', 'Sport']].drop_duplicates(subset=['index'])
    x = x.rename(columns={'index': 'Name', 'Name_x': 'Medals'})
    return x

def country_wise_medal(df,country):
    df=df.dropna(subset=['Medal'])
    temp_df=df.drop_duplicates(subset=['NOC','Team','Event','Year','City','Sport','Medal','Games'])
    new_df=temp_df[temp_df['region']==country]
    final_df=new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df,country):
    temp_df = df.drop_duplicates(subset=['NOC', 'Team', 'Event', 'Year', 'City', 'Sport', 'Medal', 'Games'])
    new_df = temp_df[temp_df['region'] == country]
    pt=new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def top_athletes_country_wise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport']].drop_duplicates(subset=['index'])

    x = x.rename(columns={'index': 'Name', 'Name_x': 'Medals'})
    return x

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Age'].fillna('No medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = pd.merge(men, women, on='Year', how='left').fillna(0)
    final = final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'})
    return final
