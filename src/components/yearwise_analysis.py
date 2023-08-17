# Module generates all the charts that are present under the yearwise analysis tab

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys

from src.exception import CustomException
from src.logger import logging

# Generates the visualization of the points table for a particular year

def pointsTableGraph(table):
    
    try:
        teams = []
        for team in table.Team.tolist():
            team = f'<b>{team}</b>'
            teams.append('<br>'.join(team.split()))

        fig = make_subplots(cols=1, rows=3, shared_xaxes=False, row_heights = [0.1,0.4,0.35], vertical_spacing = 0.1)

        fig.add_trace(go.Scatter(x = teams,
                                y = table['Points'],
                                name = 'Points',
                                hovertemplate = '%{x} : %{y} Points',
                                marker = dict(size=8, color='#FFA500'),
                                line = dict(width = 1)),
                    row = 1,
                    col = 1)

        fig.update_yaxes(showticklabels=True, row = 1, col = 1)

        for column,color in [('Loss','#EF3340'), ('No Result','#00150C'), ('Tie','#C0E7F6'), ('Win','#02894B')]:
            fig.add_trace(go.Bar(x = teams,
                                y = table[column].tolist(),
                                name = column,
                                hovertemplate = '(%{x}: %{y})',
                                text = table[column].tolist(),
                                textposition = 'inside',
                                insidetextanchor = 'middle',
                                width = 0.3,
                                marker = dict(color = color,
                                            line_width = 0)),
                        row = 2,
                        col = 1)
            
        fig.update_yaxes(showticklabels=False, row = 2, col = 1)


        fig.add_trace(go.Bar(x = teams,
                                y = table['Net Run Rate'].tolist(),
                                name = 'Net Run Rate',
                                hovertemplate = '(%{x}: %{y})',
                                text = table['Net Run Rate'].tolist(),
                                textposition = 'outside',
                                width = 0.4,
                                marker = dict(color = '#2F435A',
                                            line_width = 0)),
                    row = 3,
                    col = 1)

        fig.update_yaxes(showticklabels=False, row = 3, col = 1)

        fig.update_xaxes(showgrid=False, tickangle=0, tickfont_size=10)
        fig.update_yaxes(showgrid=False)

        fig.add_vrect(x0=-0.5, x1=3.5, fillcolor='#02894B', opacity=0.1, annotation_text='')

        fig.update_layout(plot_bgcolor='white',
                        barmode = 'stack',
                        title = dict(text =f'<b>Points Table Visualized</b>'),
                        font = dict(family='Verdana',size = 11,color='#444444'),
                        height = 1200,
                        width = 900)
        
        return fig
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)

# Generates the graph for top run scorers for a particular year

def topRunsYearGraph(player_stats,year):

    try:

        top_runs = player_stats[(player_stats['Year'] == year) & (player_stats['TotalRuns']>0)][['Name','TotalRuns','StrikeRate','BattingAverage']].head(10)

        NAME_ORDER = top_runs['Name'].tolist()
        NAME_ORDER.reverse()

        fig = make_subplots(cols=3, rows=1, subplot_titles=['<b>Total Runs</b>','<b>Strike Rate</b>','<b>Average</b>'], shared_yaxes=True, column_widths = [0.4,0.3,0.3])

        top_scorer = top_runs.Name.iloc[0]

        top_runs['Color'] = '#C5C5C5'
        top_runs.loc[top_runs['Name'] == top_scorer,'Color'] = '#ffa500'

        top_scorer_df = top_runs.loc[top_runs['Name'] == top_scorer]
        non_top_scorer_df = top_runs.loc[top_runs['Name'] != top_scorer]

        fig.add_trace(go.Bar(x = non_top_scorer_df['TotalRuns'],
                            y = non_top_scorer_df['Name'],
                            orientation = 'h',
                            text = non_top_scorer_df['TotalRuns'],
                            marker = dict(color = non_top_scorer_df.Color.iloc[0])),
                    row = 1,
                    col = 1)

        fig.add_trace(go.Bar(x = top_scorer_df['TotalRuns'],
                            y = top_scorer_df['Name'],
                            orientation = 'h',
                            text = top_scorer_df['TotalRuns'],
                            marker = dict(color = top_scorer_df.Color.iloc[0])),
                    row = 1,
                    col = 1)

        fig.add_trace(go.Scatter(x = top_runs['StrikeRate'],
                                y = top_runs['Name'],
                                mode = 'lines+markers',
                                line = dict(width=1,color=non_top_scorer_df.Color.iloc[0])),
                    row = 1,
                    col = 2)

        fig.add_trace(go.Scatter(x = top_scorer_df['StrikeRate'],
                                y = top_scorer_df['Name'],
                                mode = 'markers',
                                marker = dict(size=10,color=top_scorer_df.Color.iloc[0])),
                    row = 1,
                    col = 2)

        fig.add_trace(go.Scatter(x = top_runs['BattingAverage'],
                                y = top_runs['Name'],
                                mode = 'lines+markers',
                                line = dict(width=1,color=non_top_scorer_df.Color.iloc[0])),
                    row = 1,
                    col = 3)

        fig.add_trace(go.Scatter(x = top_scorer_df['BattingAverage'],
                                y = top_scorer_df['Name'],
                                mode = 'markers',
                                marker = dict(size=10,color=top_scorer_df.Color.iloc[0])),
                    row = 1,
                    col = 3)
        
        fig.update_xaxes(showticklabels=False, row=1, col=1,showgrid=False)
        fig.update_yaxes(showgrid=False)
        
        fig.update_traces(textposition='inside', insidetextanchor='middle', hovertemplate='(%{y}: %{x} Runs)', row=1, col=1)
        fig.update_traces(hovertemplate='(%{y}: %{x})', row=1, col=2)
        fig.update_traces(hovertemplate='(%{y}: %{x})', row=1, col=3)
        fig.update_traces(name='')

        title_text = f'<b><span style="color:{top_scorer_df.Color.iloc[0]}">{top_scorer}</span></b> leads the list of top run scorers in IPL {year} with <b><span style="color:{top_scorer_df.Color.iloc[0]}">{top_runs.TotalRuns.iloc[0]}</span></b> runs, at a strike rate of <b><span style="color:{top_scorer_df.Color.iloc[0]}">{top_runs.StrikeRate.iloc[0]}</span></b>'

        fig.update_layout(plot_bgcolor = 'white',
                        font = dict(color = '#444444',family='Verdana',size=12),
                        title = dict(text = title_text, font_size = 14),
                        showlegend = False,
                        height = 500,
                        yaxis = dict(linecolor = 'white',categoryorder = 'array',categoryarray = NAME_ORDER))

        return fig
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)

# Generates the graph for the top wicket takers for a particular year

def topWicketsYearGraph(player_stats,year):

    try:

        top_wickets = player_stats[(player_stats['Year'] == year) & (player_stats['Wickets']>0)][['Name','Wickets','BowlingStrikeRate','BowlingAverage']].sort_values('Wickets',ascending=False).head(10)

        NAME_ORDER = top_wickets['Name'].tolist()
        NAME_ORDER.reverse()

        fig = make_subplots(cols=3, rows=1, subplot_titles=['<b>Total Wickets</b>','<b>Strike Rate</b>','<b>Average</b>'], shared_yaxes=True, column_widths = [0.4,0.3,0.3])

        top_wicket_taker = top_wickets.Name.iloc[0]

        top_wickets['Color'] = '#C5C5C5'
        top_wickets.loc[top_wickets['Name'] == top_wicket_taker,'Color'] = '#A020F0'

        top_wicket_taker_df = top_wickets.loc[top_wickets['Name'] == top_wicket_taker]
        non_top_wicket_taker_df = top_wickets.loc[top_wickets['Name'] != top_wicket_taker]

        fig.add_trace(go.Bar(x = non_top_wicket_taker_df['Wickets'],
                            y = non_top_wicket_taker_df['Name'],
                            orientation = 'h',
                            text = non_top_wicket_taker_df['Wickets'],
                            marker = dict(color = non_top_wicket_taker_df.Color.iloc[0])),
                    row = 1,
                    col = 1)

        fig.add_trace(go.Bar(x = top_wicket_taker_df['Wickets'],
                            y = top_wicket_taker_df['Name'],
                            orientation = 'h',
                            text = top_wicket_taker_df['Wickets'],
                            marker = dict(color = top_wicket_taker_df.Color.iloc[0])),
                    row = 1,
                    col = 1)

        fig.add_trace(go.Scatter(x = top_wickets['BowlingStrikeRate'],
                                y = top_wickets['Name'],
                                mode = 'lines+markers',
                                line = dict(width=1,color=non_top_wicket_taker_df.Color.iloc[0])),
                    row = 1,
                    col = 2)

        fig.add_trace(go.Scatter(x = top_wicket_taker_df['BowlingStrikeRate'],
                                y = top_wicket_taker_df['Name'],
                                mode = 'markers',
                                marker = dict(size=10,color=top_wicket_taker_df.Color.iloc[0])),
                    row = 1,
                    col = 2)

        fig.add_trace(go.Scatter(x = top_wickets['BowlingAverage'],
                                y = top_wickets['Name'],
                                mode = 'lines+markers',
                                line = dict(width=1,color=non_top_wicket_taker_df.Color.iloc[0])),
                    row = 1,
                    col = 3)

        fig.add_trace(go.Scatter(x = top_wicket_taker_df['BowlingAverage'],
                                y = top_wicket_taker_df['Name'],
                                mode = 'markers',
                                marker = dict(size=10,color=top_wicket_taker_df.Color.iloc[0])),
                    row = 1,
                    col = 3)
        
        fig.update_traces(textposition='inside', insidetextanchor='middle', hovertemplate='(%{y}: %{x} Wickets)', row=1, col=1)
        fig.update_traces(hovertemplate='(%{y}: %{x})', row=1, col=2)
        fig.update_traces(hovertemplate='(%{y}: %{x})', row=1, col=3)

        fig.update_xaxes(showticklabels=False, row=1, col=1, showgrid=False)
        fig.update_yaxes(showgrid=False)

        title_text = f'<b><span style="color:{top_wicket_taker_df.Color.iloc[0]}">{top_wicket_taker}</span></b> leads the list of top wicket takers in IPL {year} with <b><span style="color:{top_wicket_taker_df.Color.iloc[0]}">{top_wickets.Wickets.iloc[0]}</span></b> wickets, at a strike rate of <b><span style="color:{top_wicket_taker_df.Color.iloc[0]}">{top_wickets.BowlingStrikeRate.iloc[0]}</span></b>'

        fig.update_layout(plot_bgcolor = 'white',
                        font = dict(color = '#444444',family='Verdana',size=12),
                        height = 500,
                        title = dict(text = title_text, font_size = 14),
                        showlegend = False,
                        yaxis = dict(linecolor = 'white',categoryorder = 'array',categoryarray = NAME_ORDER))

        fig.update_traces(name='')

        return fig
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)

# Generates the graphs for batsmen with the top strike rates in a particular year

def topStrikerBat(player_stats,year):

    try:

        strikers = player_stats[(player_stats['Year'] == year) & (player_stats['TotalRuns'] >= 200) & (player_stats['StrikeRate'] > 100)].sort_values('StrikeRate',ascending=False)[['Name','TotalRuns','StrikeRate']].head(10)

        NAME_ORDER = strikers.Name.tolist()
        NAME_ORDER.reverse()

        fig = make_subplots(cols=2, rows=1,subplot_titles=['<b>Strike Rate</b>','<b>Runs</b>'], shared_yaxes=True, column_widths = [0.6,0.4])

        top_striker = strikers.Name.iloc[0]
        strike_rate = strikers.loc[strikers['Name'] == top_striker,'StrikeRate'].values[0]

        top_striker_df = strikers.loc[strikers['Name'] == top_striker]
        non_top_striker_df = strikers.loc[strikers['Name'] != top_striker]

        fig.add_trace(go.Bar(x = non_top_striker_df['StrikeRate'],
                            y = non_top_striker_df['Name'],
                            orientation = 'h',
                            text = non_top_striker_df['StrikeRate'],
                            marker = dict(color = '#c5c5c5')),
                    row = 1,
                    col = 1)

        fig.add_trace(go.Bar(x = top_striker_df['StrikeRate'],
                            y = top_striker_df['Name'],
                            orientation = 'h',
                            text = top_striker_df['StrikeRate'],
                            marker = dict(color = '#ffa500')),
                    row = 1,
                    col = 1)

        fig.update_traces(textposition='inside', insidetextanchor='middle', row=1, col=1)
        fig.update_xaxes(showticklabels=False, row=1, col=1, showgrid = False)
        fig.update_yaxes(showgrid = False)

        fig.add_trace(go.Scatter(x = strikers['TotalRuns'],
                                y = strikers['Name'],
                                mode = 'lines+markers',
                                marker = dict(size = 8),
                                line = dict(width=1,color = '#c5c5c5')),
                    row = 1,
                    col = 2)

        fig.add_trace(go.Scatter(x = top_striker_df['TotalRuns'],
                                y = top_striker_df['Name'],
                                mode = 'markers',
                                marker = dict(size = 8),
                                line = dict(width=1,color = '#ffa500')),
                    row = 1,
                    col = 2)

        annotation = f'<b><span style="color:#ffa500">{top_striker}</span> leads the list with a strike rate of <span style="color:#ffa500">{strike_rate}</span></b>'

        fig.update_layout(plot_bgcolor = 'white',
                        font = dict(color = '#444444',family='Verdana',size=12),
                        height = 500,
                        title = dict(text = annotation, font_size = 14),
                        showlegend = False,
                        yaxis = dict(linecolor = 'white',categoryorder = 'array',categoryarray = NAME_ORDER))

        fig.update_traces(name='', hovertemplate='(%{y}: %{x})')

        return fig
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)

# Generates the graph for bowlers with the top strike rates in a particular year

def topStrikerBowl(player_stats,year):
    try:

        strikers = player_stats[(player_stats['Year'] == year) & (player_stats['Wickets'] >= 10)].sort_values('BowlingStrikeRate',ascending=True)[['Name','Wickets','BowlingStrikeRate']].head(10)

        NAME_ORDER = strikers.Name.tolist()
        NAME_ORDER.reverse()

        fig = make_subplots(cols=2, rows=1, subplot_titles=['<b>Strike Rate</b>','<b>Wickets</b>'], shared_yaxes=True, column_widths = [0.6,0.4])

        top_striker = strikers.Name.iloc[0]
        strike_rate = strikers.loc[strikers['Name'] == top_striker,'BowlingStrikeRate'].values[0]

        top_striker_df = strikers.loc[strikers['Name'] == top_striker]
        non_top_striker_df = strikers.loc[strikers['Name'] != top_striker]

        fig.add_trace(go.Bar(x = non_top_striker_df['BowlingStrikeRate'],
                            y = non_top_striker_df['Name'],
                            orientation = 'h',
                            marker = dict(color='#c5c5c5'),
                            text = non_top_striker_df['BowlingStrikeRate']),
                    row = 1,
                    col = 1)

        fig.add_trace(go.Bar(x = top_striker_df['BowlingStrikeRate'],
                            y = top_striker_df['Name'],
                            orientation = 'h',
                            text = top_striker_df['BowlingStrikeRate'],
                            marker = dict(color = '#A020F0')),
                    row = 1,
                    col = 1)

        fig.update_traces(textposition='inside', insidetextanchor='middle', row=1, col=1)
        fig.update_xaxes(showticklabels=False, row=1, col=1, showgrid=False)
        fig.update_yaxes(showgrid=False)

        fig.add_trace(go.Scatter(x = strikers['Wickets'],
                                y = strikers['Name'],
                                mode = 'lines+markers',
                                line = dict(width=1, color='#c5c5c5')),
                    row = 1,
                    col = 2)

        fig.add_trace(go.Scatter(x = top_striker_df['Wickets'],
                                y = top_striker_df['Name'],
                                mode = 'markers',
                                marker = dict(size = 8),
                                line = dict(width=1,color = '#A020F0')),
                    row = 1,
                    col = 2)

        annotation = f'<b><span style="color:#A020F0">{top_striker}</span> leads the list with a strike rate of <span style="color:#A020F0">{strike_rate}</span></b>'

        fig.update_layout(plot_bgcolor = 'white',
                        font = dict(color = '#444444',family='Verdana',size=11),
                        height = 500,
                        title = dict(text = annotation),
                        showlegend = False,
                        yaxis = dict(linecolor = 'white',categoryorder = 'array',categoryarray = NAME_ORDER))

        fig.update_traces(name='', hovertemplate='(%{y}:%{x})')

        return fig
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)

# Generates the graphs for the top run scorers for a franchise in a particular year

def franchiseRunsGraph(player_stats,year,franchise):

    try:

        franchise_runs = player_stats[(player_stats['Year'] == year) & (player_stats['TeamName'] == franchise)][['Name','Matches','TotalRuns','StrikeRate','BattingAverage']].head(5)
        franchise_runs.Matches = franchise_runs.Matches.astype(int)
        franchise_runs.rename(columns={'TotalRuns':'Runs','StrikeRate':'Strike Rate','BattingAverage':'Average'},inplace=True)
        franchise_runs.Average = franchise_runs.Average.apply(lambda x:round(x,1))
        franchise_runs['Color'] = '#C5C5C5'
        franchise_runs.iloc[0,-1] = '#ffa500'

        NAME_ORDER = franchise_runs.Name.tolist()
        NAME_ORDER.reverse()

        fig = make_subplots(cols=3, rows=1, subplot_titles=['<b>Total Runs</b>','<b>Strike Rate</b>','<b>Average</b>'], shared_yaxes=True, column_widths = [0.4,0.3,0.3])

        top_scorer = franchise_runs.Name.iloc[0]

        top_scorer_df = franchise_runs.loc[franchise_runs['Name'] == top_scorer]
        non_top_scorer_df = franchise_runs.loc[franchise_runs['Name'] != top_scorer]

        fig.add_trace(go.Bar(x = non_top_scorer_df['Runs'],
                            y = non_top_scorer_df['Name'],
                            orientation = 'h',
                            text = non_top_scorer_df['Runs'],
                            marker = dict(color = non_top_scorer_df.Color.iloc[0])),
                    row = 1,
                    col = 1)

        fig.add_trace(go.Bar(x = top_scorer_df['Runs'],
                            y = top_scorer_df['Name'],
                            orientation = 'h',
                            text = top_scorer_df['Runs'],
                            marker = dict(color = top_scorer_df.Color.iloc[0])),
                    row = 1,
                    col = 1)

        fig.update_traces(textposition='inside', insidetextanchor='middle', hovertemplate='(%{y}:%{x})', row=1, col=1)
        fig.update_traces(hovertemplate='(%{y}:%{x})', row=1, col=2)
        fig.update_traces(hovertemplate='(%{y}:%{x})', row=1, col=3)

        fig.update_xaxes(showticklabels=False, row=1, col=1, showgrid=False)
        fig.update_yaxes(showgrid=False)

        fig.add_trace(go.Scatter(x = franchise_runs['Strike Rate'],
                                y = franchise_runs['Name'],
                                mode = 'lines+markers',
                                line = dict(width=1,color=non_top_scorer_df.Color.iloc[0])),
                    row = 1,
                    col = 2)

        fig.add_trace(go.Scatter(x = top_scorer_df['Strike Rate'],
                                y = top_scorer_df['Name'],
                                mode = 'markers',
                                marker = dict(size=10,color=top_scorer_df.Color.iloc[0])),
                    row = 1,
                    col = 2)

        fig.add_trace(go.Scatter(x = franchise_runs['Average'],
                                y = franchise_runs['Name'],
                                mode = 'lines+markers',
                                line = dict(width=1,color=non_top_scorer_df.Color.iloc[0])),
                    row = 1,
                    col = 3)

        fig.add_trace(go.Scatter(x = top_scorer_df['Average'],
                                y = top_scorer_df['Name'],
                                mode = 'markers',
                                marker = dict(size=10,color=top_scorer_df.Color.iloc[0])),
                    row = 1,
                    col = 3)

        title_text = f'<b><span style="color:{top_scorer_df.Color.iloc[0]}">{top_scorer}</span> leads the list with <span style="color:{top_scorer_df.Color.iloc[0]}">{top_scorer_df.Runs.iloc[0]}</span> runs, at a strike rate of <span style="color:{top_scorer_df.Color.iloc[0]}">{top_scorer_df["Strike Rate"].iloc[0]}</span></b>'

        fig.update_layout(plot_bgcolor = 'white',
                        font = dict(color = '#444444',family='Verdana',size=12),
                        title = dict(text = title_text),
                        showlegend = False,
                        height = 400,
                        yaxis = dict(linecolor = 'white',categoryorder = 'array',categoryarray = NAME_ORDER))

        fig.update_traces(name='')

        return fig
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)

# Generates the graphs for the wicket takers for a franchise in a particular year

def franchiseWicketsGraph(player_stats,year,franchise):

    try:

        franchise_wickets = player_stats[(player_stats['Year'] == year) & (player_stats['TeamName'] == franchise)][['Name','Matches','Wickets','BowlingStrikeRate','BowlingAverage']].sort_values('Wickets',ascending=False).head(5)
        franchise_wickets.Matches = franchise_wickets.Matches.astype(int)
        franchise_wickets.rename(columns={'BowlingStrikeRate':'Strike Rate','BowlingAverage':'Average'},inplace=True)
        franchise_wickets.Average = franchise_wickets.Average.apply(lambda x:round(x,1))

        franchise_wickets['Color'] = '#C5C5C5'
        franchise_wickets.iloc[0,-1] = '#A020F0'

        NAME_ORDER = franchise_wickets.Name.tolist()
        NAME_ORDER.reverse()

        fig = make_subplots(cols=3, rows=1, subplot_titles=['<b>Wickets</b>','<b>Strike Rate</b>','<b>Average</b>'], shared_yaxes=True, column_widths = [0.4,0.3,0.3])

        top_wicket_taker = franchise_wickets.Name.iloc[0]

        top_wicket_taker_df = franchise_wickets.loc[franchise_wickets['Name'] == top_wicket_taker]
        non_top_wicket_taker_df = franchise_wickets.loc[franchise_wickets['Name'] != top_wicket_taker]

        fig.add_trace(go.Bar(x = non_top_wicket_taker_df['Wickets'],
                            y = non_top_wicket_taker_df['Name'],
                            orientation = 'h',
                            text = non_top_wicket_taker_df['Wickets'],
                            marker = dict(color = non_top_wicket_taker_df.Color.iloc[0])),
                    row = 1,
                    col = 1)

        fig.add_trace(go.Bar(x = top_wicket_taker_df['Wickets'],
                            y = top_wicket_taker_df['Name'],
                            orientation = 'h',
                            text = top_wicket_taker_df['Wickets'],
                            marker = dict(color = top_wicket_taker_df.Color.iloc[0])),
                    row = 1,
                    col = 1)

        fig.update_traces(textposition='inside', insidetextanchor='middle', hovertemplate='%{y}: %{x} Wickets', row=1, col=1)
        fig.update_traces(hovertemplate='(%{y}: %{x})', row=1, col=2)
        fig.update_traces(hovertemplate='(%{y}: %{x})', row=1, col=3)
        fig.update_xaxes(showticklabels=False, row=1, col=1, showgrid=False)
        fig.update_yaxes(showgrid=False)

        fig.add_trace(go.Scatter(x = franchise_wickets['Strike Rate'],
                                y = franchise_wickets['Name'],
                                mode = 'lines+markers',
                                line = dict(width=1,color=non_top_wicket_taker_df.Color.iloc[0])),
                    row = 1,
                    col = 2)

        fig.add_trace(go.Scatter(x = top_wicket_taker_df['Strike Rate'],
                                y = top_wicket_taker_df['Name'],
                                mode = 'markers',
                                marker = dict(size=10,color=top_wicket_taker_df.Color.iloc[0])),
                    row = 1,
                    col = 2)

        fig.add_trace(go.Scatter(x = franchise_wickets['Average'],
                                y = franchise_wickets['Name'],
                                mode = 'lines+markers',
                                line = dict(width=1,color=non_top_wicket_taker_df.Color.iloc[0])),
                    row = 1,
                    col = 3)

        fig.add_trace(go.Scatter(x = top_wicket_taker_df['Average'],
                                y = top_wicket_taker_df['Name'],
                                mode = 'markers',
                                marker = dict(size=10,color=top_wicket_taker_df.Color.iloc[0])),
                    row = 1,
                    col = 3)

        title_text = f'<b><span style="color:{top_wicket_taker_df.Color.iloc[0]}">{top_wicket_taker}</span> leads the list with <span style="color:{top_wicket_taker_df.Color.iloc[0]}">{top_wicket_taker_df.Wickets.iloc[0]}</span> wickets, at a strike rate of <span style="color:{top_wicket_taker_df.Color.iloc[0]}">{top_wicket_taker_df["Strike Rate"].iloc[0]}</span></b>'

        fig.update_layout(plot_bgcolor = 'white',
                        font = dict(color = '#444444',family='Verdana',size=12),
                        title = dict(text = title_text),
                        showlegend = False,
                        height = 400,
                        yaxis = dict(linecolor = 'white',categoryorder = 'array',categoryarray = NAME_ORDER))

        fig.update_traces(name='')

        return fig
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)