import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
import sys

from src.components.all_time_analysis import *
from src.components.yearwise_analysis import *
from src.components.franchisewise_analysis import *
from src.components.playerwise_analysis import *

from src.exception import CustomException
from src.logger import logging

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.sidebar.title('IPL Data Analysis')

choice = st.sidebar.radio(
    'Select an Option',
    ('All-time Analysis', 'Year-wise Analysis', 'Franchise-wise Analysis', 'Player-wise Analysis')
)

try:

    player_stats = pd.read_csv('data/player_stats_all_time.csv')
    points_table = pd.read_csv('data/points_table_all_time.csv')
    matches = pd.read_csv('data/matches_all_time.csv')
    ground_data = pd.read_csv('data/ground_location.csv')

    ipl_winners = {
        2008:'Rajasthan Royals',
        2009:'Deccan Chargers',
        2010:'Chennai Super Kings',
        2011:'Chennai Super Kings',
        2012:'Kolkata Knight Riders',
        2013:'Mumbai Indians',
        2014:'Kolkata Knight Riders',
        2015:'Mumbai Indians',
        2016:'Sunrisers Hyderabad',
        2017:'Mumbai Indians',
        2018:'Chennai Super Kings',
        2019:'Mumbai Indians',
        2020:'Mumbai Indians',
        2021:'Chennai Super Kings',
        2022:'Gujarat Titans',
        2023:'Chennai Super Kings'
    }

    if choice == 'All-time Analysis':

        st.title('All-time Analysis')

        logging.info('All-time Analysis')

        nationalities = player_stats['Nationality'].unique().tolist()
        nationalities.insert(0,'Indian and Overseas')
        nationality = st.sidebar.selectbox('Select Nationality',nationalities)

        editions = player_stats['Year'].unique().shape[0]
        teams_participated = player_stats['TeamName'].unique().shape[0]
        matches_played = matches.shape[0]

        st.header('')

        col1,col2,col3 = st.columns(3)

        with col1:
            st.subheader('Editions')
            st.subheader(editions)
        with col2:
            st.subheader('Teams')
            st.subheader(teams_participated)
        with col3:
            st.subheader('Matches')
            st.subheader(matches_played)

        logging.info('Editions, Number of Teams and Matches columns generated')

        teamwise_winners = {}
        for year,team in ipl_winners.items():
            if team in teamwise_winners.keys():
                teamwise_winners[team].append(year)
            else:
                teamwise_winners[team] = [year]

        win_count = {}
        for team in teamwise_winners.keys():
            win_count[team] = len(teamwise_winners[team])

        win_count_y = list(win_count.keys())
        win_count_x = list(win_count.values())

        titles = pd.DataFrame({'Team Name':win_count_y,'Wins':win_count_x}).sort_values(['Wins','Team Name'],ascending=[False,True])
        
        logging.info('Generating Charts ...')

        st.plotly_chart(topTitlesGraph(titles))

        st.subheader('Distribution of Wins')
        st.plotly_chart(topWinsTeamGraph(matches))

        st.subheader('Player Participation over the Years')
        st.plotly_chart(playerStrength(player_stats))

        st.subheader(f'Top 10 Run Scorers of All Time ({nationality})')
        st.plotly_chart(topRunsGraph(player_stats,nationality))

        st.subheader(f'Top 10 Wicket Takers of All Time ({nationality})')
        st.plotly_chart(topWicketsGraph(player_stats,nationality))
        
        st.subheader(f'Highest Individual Scores ({nationality})')
        if nationality == 'Indian and Overseas':
            best_batting = player_stats[player_stats['BestScore'] != 'Not Available'].sort_values(['HighestScore','IsNotDismissed'],ascending=[False,True])[['Name','BestScore','Year']].head(20)
        else:
            best_batting = player_stats[(player_stats['Nationality'] == nationality) & (player_stats['BestScore'] != 'Not Available')].sort_values(['HighestScore','IsNotDismissed'],ascending=[False,True])[['Name','BestScore','Year']].head(20)
        st.table(best_batting)

        st.subheader(f'Best Bowling Figures ({nationality})')
        if nationality == 'Indian and Overseas':
            best_bowling = player_stats.sort_values(['BestBowlingWickets','BestBowlingRuns','Year'],ascending=[False,True,True])[['Name','BestBowling','Year']].drop_duplicates(['Name','BestBowling']).head(20)
        else:
            best_bowling = player_stats[player_stats['Nationality'] == nationality].sort_values(['BestBowlingWickets','BestBowlingRuns','Year'],ascending=[False,True,True])[['Name','BestBowling','Year']].drop_duplicates(['Name','BestBowling']).head(20)
        st.table(best_bowling)

        st.subheader(f'50s and 100s over the Years ({nationality})')
        st.plotly_chart(battingLandmark(player_stats,nationality))

        st.subheader(f'4 and 5 Wicket Hauls over the Years ({nationality})')
        st.plotly_chart(bowlingLandmark(player_stats,nationality))

        st.subheader(f'Boundary Count over the Years ({nationality})')
        st.plotly_chart(boundaryCount(player_stats,nationality))

        # Creating a Folium Map
        centroid = (21.1458,79.0882)

        m = folium.Map(location=centroid,zoom_start=6)

        for i in range(0,ground_data.shape[0]):
            html = popup_html(i,ground_data,matches)
            popup = folium.Popup(folium.Html(html,script=True),max_width=800)
            folium.Marker([ground_data['Latitude'].iloc[i],ground_data['Longitude'].iloc[i]],popup=popup).add_to(m)

        st.subheader('Ground-wise statistics')
        st_folium(m, width=800, height=500)

        logging.info('All Charts Generated')

    elif choice == 'Year-wise Analysis':

        st.title('Year-wise Analysis')

        logging.info('Year-wise Analysis')

        years = player_stats['Year'].unique().tolist()
        year = st.sidebar.selectbox('Select Year', years)

        st.header('')
        st.header(f'Champions : {ipl_winners[year]}')
        st.header('')

        players = player_stats[player_stats['Year'] == year]['Name'].unique().shape[0]
        matches_played = matches[matches['Year'] == year].shape[0]

        col1,col2 = st.columns(2)
        
        with col1:
            st.subheader('Matches')
            st.subheader(matches_played)

        with col2:
            st.subheader('Players')
            st.subheader(players)

        logging.info('Matches and Players columns generated')

        st.header('')

        st.subheader(f'Points Table {year}')

        logging.info('Generating Charts ...')

        table = points_table[points_table['Year'] == year][['Standings','TeamName','Matches','Wins','Loss','Tied','NoResult','Points','NetRunRate']]
        table.rename(columns={'TeamName':'Team','Wins':'Win','Tied':'Tie','NoResult':'No Result','NetRunRate':'Net Run Rate'},inplace=True)

        st.table(table)

        st.plotly_chart(pointsTableGraph(table))

        st.subheader(f'Top 10 Run Scorers in IPL {year}')
        st.plotly_chart(topRunsYearGraph(player_stats,year))

        st.subheader(f'Top 10 Wicket Takers in IPL {year}')
        st.plotly_chart(topWicketsYearGraph(player_stats,year))

        st.subheader('Highest Batting Strike Rate (with atleast 200 runs)')
        st.plotly_chart(topStrikerBat(player_stats,year))

        st.subheader('Highest Bowling Strike Rate (with atleast 10 wickets)')
        st.plotly_chart(topStrikerBowl(player_stats,year))

        franchises = sorted(player_stats['TeamName'][player_stats['Year'] == year].unique().tolist())
        if year == 2009:
            franchises.remove('Delhi Capitals')
        franchise = st.selectbox('Select a Franchise',franchises)

        st.header('')
        col1,col2,col3 = st.columns(3)
        with col1:
            wins = matches[(matches['Year'] == year)&((matches['FirstBattingTeamName'] == franchise)|(matches['SecondBattingTeamName'] == franchise)) & (matches['Winner'] == franchise)].Winner.value_counts().sum()
            st.subheader('Wins')
            st.subheader(wins)
        with col2:
            loss = matches[(matches['Year'] == year)&((matches['FirstBattingTeamName'] == franchise)|(matches['SecondBattingTeamName'] == franchise)) & ((matches['Winner'] != franchise) & (matches['Winner'] != 'No Result'))].Winner.value_counts().sum()
            st.subheader('Losses')
            st.subheader(loss)
        with col3:
            ties = matches[(matches['Year'] == year)&((matches['FirstBattingTeamName'] == franchise)|(matches['SecondBattingTeamName'] == franchise)) & ((matches['Winner'] == 'Tie') | (matches['Winner'] == 'No Result'))].Winner.value_counts().sum()
            st.subheader('Ties/No Result')
            st.subheader(ties)
        st.header('')

        st.subheader(f'Top 5 Run Scorers for {franchise} in IPL {year}')
        st.plotly_chart(franchiseRunsGraph(player_stats,year,franchise))

        st.subheader(f'Top 5 Wicket Takers for {franchise} in IPL {year}')
        st.plotly_chart(franchiseWicketsGraph(player_stats,year,franchise))

        logging.info('All Charts Generated')

    elif choice == 'Franchise-wise Analysis':

        st.title('Franchise-wise Analysis')

        logging.info('Franchise-wise Analysis')

        franchises = sorted(player_stats['TeamName'].unique().tolist())
        franchise = st.sidebar.selectbox('Select a Franchise',franchises)

        st.header('')

        col1,col2,col3 = st.columns(3)

        with col1:
            seasons = matches[(matches['FirstBattingTeamName'] == franchise)|(matches['SecondBattingTeamName'] == franchise)]['Year'].unique().shape[0]
            st.subheader('Seasons')
            st.subheader(seasons)

        with col2:
            matches_played = matches[(matches['FirstBattingTeamName'] == franchise)|(matches['SecondBattingTeamName'] == franchise)].shape[0]
            st.subheader('Matches')
            st.subheader(matches_played)

        with col3:
            wins = matches[((matches['FirstBattingTeamName'] == franchise)|(matches['SecondBattingTeamName'] == franchise)) & (matches['Winner'] == franchise)].shape[0]
            st.subheader('Wins')
            st.subheader(wins)

        logging.info('Seasons, Matches and Wins columns generated')

        st.header('')

        logging.info('Generating Charts ...')

        st.subheader(f'Top 10 Run Scorers for {franchise} (All Time)')
        st.plotly_chart(franchiseTotalRuns(player_stats,franchise))

        st.subheader(f'Top 10 Wicket Takers for {franchise} (All Time)')
        st.plotly_chart(franchiseTotalWickets(player_stats,franchise))

        st.subheader(f'Group Stage Standings - {franchise}')
        st.plotly_chart(standings(points_table,franchise))

        st.subheader(f'Average Age Comparison - {franchise}')
        st.plotly_chart(avgAge(player_stats,franchise))

        st.header('')
        st.subheader('Compare with a Franchise')
        st.header('')

        franchise1 = franchise

        franchises = player_stats['TeamName'].unique().tolist()
        franchises.remove(franchise1)
        franchises.sort()
        franchise2 = st.selectbox('Select a Franchise',franchises)
        
        head_to_head = matches[((matches['FirstBattingTeamName'] == franchise1) & (matches['SecondBattingTeamName'] == franchise2)) | ((matches['FirstBattingTeamName'] == franchise2) & (matches['SecondBattingTeamName'] == franchise1))].Winner.value_counts().reset_index().rename(columns={'index':'Team','Winner':'Wins'})
        
        if not head_to_head.empty:
            winners = head_to_head.Team.tolist()
            results = head_to_head.Wins.tolist()

            if 'No Result' in winners:
                position = winners.index('No Result')
                winners.pop(position)
                no_result = results.pop(position)
                
                head_to_head = pd.DataFrame({'Team':winners,'Wins':results})
                temp = pd.DataFrame({'Team':['No Result'],'Wins':[no_result]})
                
                head_to_head = head_to_head.sort_values('Wins',ascending=False)
                
                head_to_head['Color'] = '#F8D210'
                head_to_head.iloc[0,-1] = '#FA26A0'
                
                temp['Color'] = '#2FF3E0'
                
                head_to_head = pd.concat([head_to_head,temp],ignore_index=True)
                head_to_head = head_to_head.sort_values('Wins',ascending=False)

            else:
                head_to_head['Color'] = '#F8D210'
                head_to_head.iloc[0,-1] = '#FA26A0'

            st.plotly_chart(headToHead(head_to_head))

        else:
            head_to_head = pd.DataFrame({'Team':[franchise1,franchise2]})
            head_to_head['Color'] = '#F8D210'
            head_to_head.iloc[0,-1] = '#FA26A0'

        st.subheader('Top Run Scorers (All Time)')
        franchise_runs = player_stats[['TeamName','Name','TotalRuns']].groupby(['TeamName','Name']).sum().sort_values('TotalRuns',ascending=False).reset_index()
        st.plotly_chart(headToHeadRuns(franchise_runs,franchise1,franchise2,head_to_head))

        st.subheader('Top Wicket Takers (All Time)')
        franchise_wickets = player_stats[['TeamName','Name','Wickets']].groupby(['TeamName','Name']).sum().sort_values('Wickets',ascending=False).reset_index()
        st.plotly_chart(headToHeadWickets(franchise_wickets,franchise1,franchise2,head_to_head))

        st.subheader('Standings over the Years')
        st.plotly_chart(headToHeadStandings(points_table,franchise1,franchise2,head_to_head))

        st.subheader('Average Age Comparison')
        st.plotly_chart(headToHeadAge(player_stats,franchise1,franchise2,head_to_head))

        logging.info('All Charts Generated')

    else:

        st.title('Player-wise Analysis')

        logging.info('Player-wise Analysis')

        players = sorted(player_stats.Name.unique().tolist(),key=lambda name:name.lower())
        player = st.sidebar.selectbox('Select a Player',players)

        st.header('')
        col1,col2,col3 = st.columns(3)

        with col1:
            st.subheader('Date of Birth')
            st.subheader(player_stats[player_stats['Name'] == player]['PlayerDOB'].iloc[0])

        with col2:
            st.subheader('Batting Style')
            style = player_stats[player_stats['Name'] == player]['BattingStyle'].iloc[0]
            if style == 'rhb':
                st.subheader('Right Handed Batsman')
            else:
                st.subheader('Left Handed Batsman')

        with col3:
            st.subheader('Nationality')
            st.subheader(player_stats[player_stats['Name'] == player]['Nation'].iloc[0])

        logging.info('DOB, Batting Style and Nationality columns generated')

        logging.info('Generating Charts ...')

        st.header('')
        st.subheader('Teams Represented')
        st.table(player_stats[player_stats['Name'] == player][['TeamName','Year']].rename(columns={'TeamName':'Team Name'}))

        st.subheader('Career Stats')
        st.plotly_chart(batStats(player_stats,player))
        st.plotly_chart(bowlStats(player_stats,player))

        st.subheader('Year-wise Stats')
        st.plotly_chart(runsPerSeason(player_stats,player))
        st.plotly_chart(strikeRatePerSeason(player_stats,player))
        st.plotly_chart(averagePerSeason(player_stats,player))
        st.plotly_chart(wicketsPerSeason(player_stats,player))
        st.plotly_chart(bowlingStrikeRatePerSeason(player_stats,player))
        st.plotly_chart(economyPerSeason(player_stats,player))

        logging.info('All Charts Generated')

except Exception as e:
    logging.error(CustomException(e,sys))
    raise CustomException(e,sys)