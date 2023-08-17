# Module generates all the charts that are present under the player-wise analysis tab

import plotly.graph_objects as go
import sys

from src.exception import CustomException
from src.logger import logging

# Generates the table showing the career batting stats of a player

def batStats(player_stats,player):

    try:

        matches = player_stats[player_stats['Name'] == player]['Matches'].sum().astype(int)
        total_runs = player_stats[player_stats['Name'] == player]['TotalRuns'].sum()
        highest_score = player_stats[player_stats['Name'] == player].sort_values(['HighestScore','IsNotDismissed'],ascending=[False,False])['BestScore'].iloc[0]
        
        balls = player_stats[player_stats['Name'] == player]['Balls'].sum()
        if balls == 0:
            strike_rate = '-'
        else:
            strike_rate = round((total_runs/balls)*100,2)

        outs = player_stats[player_stats['Name'] == player]['Outs'].sum()
        if outs == 0:
            average = '-'
        else:
            average = round(total_runs/outs,2)

        fifties = player_stats[player_stats['Name'] == player].FiftyPlusRuns.sum().astype(int)
        hundreds = player_stats[player_stats['Name'] == player].Centuries.sum().astype(int)

        headers = ['Matches','Total Runs','Highest Score','Strike Rate','Average','Fifties','Hundreds']
        content = [matches,total_runs,highest_score,strike_rate,average,fifties,hundreds]

        for i in range(len(headers)):
            headers[i] = f'<b>{headers[i]}</b>'

        fig = go.Figure()

        fig.add_trace(go.Table(
            header=dict(values=headers,
                    align='center',
                    fill_color = 'white'),
            cells=dict(values=content,
                    align='center',
                    fill_color = '#F2F1F0',
                    font_color = 'black',
                    height = 26)))

        fig.update_layout(font=dict(family='Verdana'),
                        height = 300,
                        width=800,
                        title = dict(text = '<b>Batting</b>'))

        return fig
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)

# Generates the table showing the career bowling stats of a player

def bowlStats(player_stats,player):
    try:
        matches = player_stats[player_stats['Name'] == player]['Matches'].sum().astype(int)
        wickets = player_stats[player_stats['Name'] == player]['Wickets'].sum()

        runs = player_stats[player_stats['Name'] == player]['TotalRunsConceded'].sum()
        balls = player_stats[player_stats['Name'] == player]['BallsBowled'].sum()

        if balls == 0:
            economy = '-'
        else:
            economy = round((runs/balls)*6,2)

        if balls == 0:
            strike_rate = '-'
        else:
            strike_rate = round((balls/wickets),2)

        best_figures = player_stats[player_stats['Name'] == player].sort_values(['BestBowlingWickets','BestBowlingRuns'],ascending=[False,True])['BestBowling'].iloc[0]

        four_for = player_stats[player_stats['Name'] == player].FourWickets.sum().astype(int)
        five_for = player_stats[player_stats['Name'] == player].FiveWickets.sum().astype(int)

        headers = ['Matches','Wickets','Best Bowling Figures','Strike Rate','Economy','Four-for','Five-for']
        content = [matches,wickets,best_figures,strike_rate,economy,four_for,five_for]

        for i in range(len(headers)):
            headers[i] = f'<b>{headers[i]}</b>'

        fig = go.Figure()

        fig.add_trace(go.Table(
            header=dict(values=headers,
                    align='center',
                    fill_color = 'white'),
            cells=dict(values=content,
                    align='center',
                    fill_color = '#F2F1F0',
                    font_color = 'black',
                    height = 26)))

        fig.update_layout(font=dict(family='Verdana'),
                        height = 300,
                        width=800,
                        title = dict(text = '<b>Bowling</b>'))

        return fig
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)

# Generates the graph showing the runs scored over the seasons

def runsPerSeason(player_stats,player):

    try:
        runs = player_stats[['Year','TotalRuns']][player_stats['Name'] == player]
        fig = go.Figure()

        fig.add_trace(go.Scatter(x = runs['Year'],
                                y = runs['TotalRuns'],
                                mode = 'lines+markers',
                                name = '',
                                hovertemplate = '%{x} : %{y} Runs',
                                marker = dict(size = 8, color = '#970C10'),
                                line = dict(width = 1, color = '#970C10')))

        fig.update_xaxes(title = 'Year',showgrid=False)
        fig.update_yaxes(title = 'Runs',showgrid=False)

        fig.update_layout(plot_bgcolor = 'white',
                        title = dict(text = '<b>Runs per Season</b>'),
                        height = 600,
                        width = 800,
                        font = dict(family='Verdana',size = 12,color='#444444'),
                        showlegend=False)

        return fig
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)

# Generates the graph showing the strike rate over the seasons

def strikeRatePerSeason(player_stats,player):

    try:
        strikerate = player_stats[['Year','StrikeRate']][player_stats['Name'] == player]
        fig = go.Figure()

        fig.add_trace(go.Scatter(x = strikerate['Year'],
                                y = strikerate['StrikeRate'],
                                name = '',
                                hovertemplate = '%{x} : %{y}',
                                mode = 'lines+markers',
                                marker = dict(size = 8, color = '#970C10'),
                                line = dict(width = 1, color = '#970C10')))

        fig.update_xaxes(title = 'Year',showgrid=False)
        fig.update_yaxes(title = 'Strike Rate',showgrid=False)

        fig.update_layout(plot_bgcolor = 'white',
                        title = dict(text = '<b>Strike Rate (Batting) per Season</b>'),
                        height = 600,
                        width = 800,
                        font = dict(family='Verdana',size = 12,color='#444444'),
                        showlegend=False)
        
        return fig
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)

# Generates the graph showing the batting average over the seasons

def averagePerSeason(player_stats,player):
    try:
        average = player_stats[['Year','BattingAverage']][player_stats['Name'] == player]
        average['BattingAverage'] = average['BattingAverage'].apply(lambda x: 0 if x<0 else x)

        fig = go.Figure()

        fig.add_trace(go.Scatter(x = average['Year'],
                                y = average['BattingAverage'],
                                name = '',
                                hovertemplate = '%{x} : %{y}',
                                mode = 'lines+markers',
                                marker = dict(size = 6, color = '#970C10'),
                                line = dict(width = 1, color = '#970C10')))

        fig.update_xaxes(title = 'Year',showgrid=False)
        fig.update_yaxes(title = 'Average',showgrid=False)

        fig.update_layout(plot_bgcolor = 'white',
                        title = dict(text = '<b>Average (Batting) per Season</b>'),
                        height = 600,
                        width = 800,
                        font = dict(family='Verdana',size = 12,color='#444444'),
                        showlegend=False)

        return fig
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)

# Generates the graph showing the wickets taken over the seasons

def wicketsPerSeason(player_stats,player):
    try:
        wickets = player_stats[['Year','Wickets']][player_stats['Name'] == player]
        fig = go.Figure()

        fig.add_trace(go.Scatter(x = wickets['Year'],
                                y = wickets['Wickets'],
                                name = '',
                                hovertemplate = '%{x} : %{y}',
                                mode = 'lines+markers',
                                marker = dict(size = 6, color = '#970C10'),
                                line = dict(width = 1, color = '#970C10')))

        fig.update_xaxes(title = 'Year',showgrid=False)
        fig.update_yaxes(title = 'Wickets',showgrid=False)

        fig.update_layout(plot_bgcolor = 'white',
                        title = dict(text = '<b>Wickets per Season</b>'),
                        height = 600,
                        width = 800,
                        font = dict(family='Verdana',size = 12,color='#444444'),
                        showlegend=False)

        return fig
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)

# Generates the graph showing the bowling strike rate over the seasons

def bowlingStrikeRatePerSeason(player_stats,player):
    try:
        strikerate = player_stats[['Year','BowlingStrikeRate']][player_stats['Name'] == player]
        fig = go.Figure()

        fig.add_trace(go.Scatter(x = strikerate['Year'],
                                y = strikerate['BowlingStrikeRate'],
                                name = '',
                                hovertemplate = '%{x} : %{y}',
                                mode = 'lines+markers',
                                marker = dict(size = 6, color = '#970C10'),
                                line = dict(width = 1, color = '#970C10')))

        fig.update_xaxes(title = 'Year',showgrid=False)
        fig.update_yaxes(title = 'Strike Rate (Bowling)',showgrid=False)

        fig.update_layout(plot_bgcolor = 'white',
                        title = dict(text = '<b>Strike Rate (Bowling) per Season</b>'),
                        height = 600,
                        width = 800,
                        font = dict(family='Verdana',size = 12,color='#444444'),
                        showlegend=False)

        return fig
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)

# Generates the graph showing the economy rate over the seasons

def economyPerSeason(player_stats,player):
    try:
        economy = player_stats[['Year','EconomyRate']][player_stats['Name'] == player]
        fig = go.Figure()

        fig.add_trace(go.Scatter(x = economy['Year'],
                                y = economy['EconomyRate'],
                                name = '',
                                hovertemplate = '%{x} : %{y}',
                                mode = 'lines+markers',
                                marker = dict(size = 6, color = '#970C10'),
                                line = dict(width = 1, color = '#970C10')))

        fig.update_xaxes(title = 'Year',showgrid=False)
        fig.update_yaxes(title = 'Economy',showgrid=False)

        fig.update_layout(plot_bgcolor = 'white',
                        title = dict(text = '<b>Economy per Season</b>'),
                        height = 600,
                        width = 800,
                        font = dict(family='Verdana',size = 12,color='#444444'),
                        showlegend=False)

        return fig
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)