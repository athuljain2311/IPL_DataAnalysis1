# Module generates all the charts that are present under the franchise-wise analysis tab

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import sys

from src.exception import CustomException
from src.logger import logging

# Generates the graph for top run scorers for a franchise

def franchiseTotalRuns(player_stats,franchise):

    try:

        runs_for_franchise = player_stats[['TeamName','Name','TotalRuns']].groupby(['TeamName','Name']).sum().reset_index()
        top_runs = runs_for_franchise.loc[runs_for_franchise['TeamName'] == franchise,['Name','TotalRuns']].sort_values('TotalRuns',ascending=False).head(10)

        NAME_ORDER = top_runs.Name.tolist()
        NAME_ORDER.reverse()

        fig = go.Figure()

        top = top_runs.Name.iloc[0]
        runs = top_runs.loc[top_runs['Name'] == top].TotalRuns.values[0]

        top_df = top_runs.loc[top_runs['Name'] == top]
        non_top_df = top_runs.loc[top_runs['Name'] != top]

        fig.add_trace(go.Bar(x = non_top_df['TotalRuns'],
                            y = non_top_df['Name'],
                            orientation = 'h',
                            text = non_top_df['TotalRuns'],
                            marker = dict(color = '#c5c5c5')))

        fig.add_trace(go.Bar(x = top_df['TotalRuns'],
                            y = top_df['Name'],
                            orientation = 'h',
                            text = top_df['TotalRuns'],
                            marker = dict(color = '#ffa500')))

        fig.update_xaxes(showticklabels=False,showgrid=False)
        fig.update_yaxes(showgrid=False)

        fig.update_traces(name='' , hovertemplate='%{y}: %{x} Runs')

        title_text = f'<b><span style="color:#ffa500">{top}</span> leads the list with <span style="color:#ffa500">{runs}</span> runs</b>'

        fig.update_layout(plot_bgcolor = 'white',
                        font = dict(color = '#444444',family='Verdana',size=11),
                        title = dict(text = title_text),
                        showlegend = False,
                        height = 500,
                        width = 600,
                        yaxis = dict(linecolor = 'white',categoryorder = 'array',categoryarray = NAME_ORDER))
        
        return fig
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)

# Generates the graph for top wicket takers for a franchise

def franchiseTotalWickets(player_stats,franchise):

    try:
        wickets_for_franchise = player_stats[['TeamName','Name','Wickets']].groupby(['TeamName','Name']).sum().reset_index()
        top_wickets = wickets_for_franchise.loc[wickets_for_franchise['TeamName'] == franchise,['Name','Wickets']].sort_values('Wickets',ascending=False).head(10)

        NAME_ORDER = top_wickets.Name.tolist()
        NAME_ORDER.reverse()

        fig = go.Figure()

        top = top_wickets.Name.iloc[0]
        wickets = top_wickets.loc[top_wickets['Name'] == top].Wickets.values[0]

        top_df = top_wickets.loc[top_wickets['Name'] == top]
        non_top_df = top_wickets.loc[top_wickets['Name'] != top]

        fig.add_trace(go.Bar(x = non_top_df['Wickets'],
                            y = non_top_df['Name'],
                            orientation = 'h',
                            text = non_top_df['Wickets'],
                            marker = dict(color = '#c5c5c5')))

        fig.add_trace(go.Bar(x = top_df['Wickets'],
                            y = top_df['Name'],
                            orientation = 'h',
                            text = top_df['Wickets'],
                            marker = dict(color = '#A020F0')))

        fig.update_xaxes(showticklabels=False, showgrid=False)
        fig.update_yaxes(showgrid=False)

        fig.update_traces(name='' , hovertemplate='%{y}: %{x} Wickets')

        title_text = f'<b><span style="color:#A020F0">{top}</span> leads the list with <span style="color:#A020F0">{wickets}</span> wickets</b>'

        fig.update_layout(plot_bgcolor = 'white',
                        font = dict(color = '#444444',family='Verdana',size=11),
                        title = dict(text = title_text),
                        height = 500,
                        width = 600,
                        showlegend = False,
                        yaxis = dict(linecolor = 'white',categoryorder = 'array',categoryarray = NAME_ORDER))
        
        return fig
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)

# Generates the graph for the yearwise standings of a franchise

def standings(points_table,franchise):

    try:

        position = points_table[points_table['TeamName'] == franchise][['Year','Standings']]
        position['Color'] = position['Standings'].apply(lambda x: '#02894B' if x <= 4 else '#EF3340')

        fig = go.Figure()

        fig.add_trace(go.Scatter(x = position.Year,
                                y = position.Standings,
                                hovertemplate = '%{x} : %{y}',
                                name = '',
                                mode = 'lines+markers',
                                marker = dict(size = 10, color = position.Color, line_color = '#A8BBB0',line_width = 1),
                                line = dict(width = 1, color = '#A8BBB0')))

        fig.update_yaxes(showticklabels = True, title = 'Standings', autorange= 'reversed',showgrid=False)
        fig.update_xaxes(title = 'Year',showgrid=False)

        qualification = position['Year'][position['Standings']<=4].shape[0]
        if qualification == 1:
            title_text = f"Qualified for the Playoffs <span style='color:#02894B'>{qualification}</span> time"
        else:
            title_text = f"Qualified for the Playoffs <span style='color:#02894B'>{qualification}</span> times"

        fig.update_layout(plot_bgcolor = 'white',
                        title = dict(text=title_text),
                        height = 500,
                        width = 800,
                        font = dict(family='Verdana',size = 12,color='#444444'))
                    
        return fig
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)

# Generates the graph for the average age of a franchise's squad over the years

def avgAge(player_stats,franchise):

    try:
        average_age_season = player_stats[['Year','Age']].groupby('Year').agg('mean').apply(lambda x:round(x,1))
        average_age_season.reset_index(inplace=True)

        team_average_age = None

        for team in player_stats['TeamName'].unique():
            average_age = player_stats[player_stats['TeamName'] == team][['Year','Age']].groupby('Year').agg('mean').apply(lambda x:round(x,1)).reset_index()
            average_age['Team'] = team
            if team_average_age is None:
                team_average_age = average_age
            else:
                team_average_age = pd.concat([team_average_age,average_age],ignore_index=True)

        current_team = franchise
        other_teams = player_stats.TeamName.unique().tolist()
        other_teams.remove(current_team)

        fig = go.Figure()

        for team in other_teams:
            age_distribution = team_average_age.loc[team_average_age['Team'] == team]
            
            fig.add_trace(go.Scatter(x = age_distribution.Year,
                                y = age_distribution.Age,
                                name = '',
                                mode = 'lines',
                                line = dict(width = 0.5, color = '#A8BBB0')))
            
        fig.add_trace(go.Scatter(x = average_age_season.Year,
                                y = average_age_season.Age,
                                name = '',
                                mode = 'lines',
                                line = dict(width = 2, color = '#738580')))

        age_distribution = team_average_age.loc[team_average_age['Team'] == current_team]

        fig.add_trace(go.Scatter(x = age_distribution.Year,
                                y = age_distribution.Age,
                                name = '',
                                mode = 'lines+markers',
                                line = dict(width = 1, color = '#970C10')))


        fig.update_xaxes(title = 'Year',showgrid=False)
        fig.update_yaxes(showticklabels=True, title = 'Average Age',showgrid=False)
        fig.update_traces(hovertemplate='%{x}: %{y} Years')

        # Calculates the number of occasions when the squad's age has exceeded that of tournament's average player age

        c = 0
        for year in team_average_age.loc[team_average_age['Team'] == franchise].Year.unique():
            team_age = team_average_age.loc[(team_average_age['Team'] == franchise)&(team_average_age['Year'] == year),'Age'].values[0]
            avg_age = average_age_season.loc[average_age_season['Year'] == year,'Age'].values[0]
            if team_age > avg_age:
                c = c+1

        if c == 1:
            title_text = f"<span style='color:#970C10'>Squad's Average Age</span> exceeded <span style='color:#738580'>Tournament's Average Player Age</span> on {c} Occasion"
        else:
            title_text = f"<span style='color:#970C10'>Squad's Average Age</span> exceeded <span style='color:#738580'>Tournament's Average Player Age</span> on {c} Occasions"

        fig.update_layout(plot_bgcolor='white',
                        title = dict(text=title_text),
                        width = 800,
                        height = 600,
                        showlegend = False,
                        font = dict(family='Verdana',size = 12,color='#444444'))

        return fig
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)

# Generates the bar graph displaying the outcomes when the franchises met head to head

def headToHead(head_to_head):

    try:

        NAME_ORDER = head_to_head.Team.tolist()
        NAME_ORDER.reverse()

        fig = go.Figure()

        fig.add_trace(go.Bar(x = head_to_head['Wins'],
                            y = head_to_head['Team'],
                            orientation = 'h',
                            name = '',
                            hovertemplate = '%{y}:%{x}',
                            marker = dict(color = head_to_head['Color']),
                            width = 0.5,
                            text = head_to_head['Wins'],
                            textposition = 'inside',
                            insidetextanchor = 'middle'))

        fig.update_xaxes(showticklabels=False)

        fig.update_layout(plot_bgcolor = 'white',
                        font = dict(color = '#444444',family='Verdana',size=12),
                        title = dict(text = '<b>Head-to-Head Results</b>', font_size=20),
                        showlegend = False,
                        height = 400,
                        yaxis = dict(linecolor = 'white',categoryorder = 'array',categoryarray = NAME_ORDER))
        
        return fig
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)

# Generates the graphs for the top run scorers for each franchise
# head_to_head dataframe is used to map the colors uniformly

def headToHeadRuns(franchise_runs,franchise1,franchise2,head_to_head):

    try:
        f1_runs = franchise_runs[franchise_runs['TeamName'] == franchise1][['Name','TotalRuns']].sort_values('TotalRuns',ascending=False).head(5)
        f2_runs = franchise_runs[franchise_runs['TeamName'] == franchise2][['Name','TotalRuns']].sort_values('TotalRuns',ascending=False).head(5)

        f1 = f1_runs.Name.tolist()
        f1.reverse()

        f2 = f2_runs.Name.tolist()
        f2.reverse()

        fig = make_subplots(cols=1, rows=2, shared_xaxes=True, row_heights = [0.5,0.5], vertical_spacing = 0.2)


        fig.add_trace(go.Bar(x = f1_runs['TotalRuns'],
                            y = f1_runs['Name'],
                            orientation = 'h',
                            text = f1_runs['TotalRuns'],
                            marker = dict(color = head_to_head.loc[head_to_head['Team'] == franchise1, 'Color'].values[0])),
                    row = 1,
                    col = 1)

        fig.add_trace(go.Bar(x = f2_runs['TotalRuns'],
                            y = f2_runs['Name'],
                            orientation = 'h',
                            text = f2_runs['TotalRuns'],
                            marker = dict(color = head_to_head.loc[head_to_head['Team'] == franchise2, 'Color'].values[0])),
                    row = 2,
                    col = 1)

        fig.update_xaxes(showticklabels=False)

        fig.update_yaxes(categoryorder='array',
                        categoryarray=f1,
                        row = 1,
                        col = 1)

        fig.update_yaxes(categoryorder='array',
                        categoryarray=f2,
                        row = 2,
                        col = 1)

        fig.update_yaxes(linecolor = 'white')

        fig.update_traces(name='' , hovertemplate='%{y}: %{x} Runs', insidetextanchor='middle')

        fig.add_annotation(text=f'<b>{franchise1}</b>',
                        font = dict(color = '#444444',family='Verdana',size=14),
                        showarrow = False,
                        xref = 'paper',
                        yref = 'paper',
                        x=0,
                        y=1.09)

        fig.add_annotation(text=f'<b>{franchise2}</b>',
                        font = dict(color = '#444444',family='Verdana',size=14),
                        showarrow = False,
                        xref = 'paper',
                        yref = 'paper',
                        x=0,
                        y=0.46)

        fig.update_layout(plot_bgcolor = 'white',
                        font = dict(color = '#444444',family='Verdana',size=12),
                        height = 600,
                        width = 600,
                        showlegend = False)

        return fig
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)

# Generates the graphs for the top wicket takers for each franchise
# head_to_head dataframe is used to map the colors uniformly

def headToHeadWickets(franchise_wickets,franchise1,franchise2,head_to_head):
    try:
        f1_wickets = franchise_wickets[franchise_wickets['TeamName'] == franchise1][['Name','Wickets']].sort_values('Wickets',ascending=False).head(5)
        f2_wickets = franchise_wickets[franchise_wickets['TeamName'] == franchise2][['Name','Wickets']].sort_values('Wickets',ascending=False).head(5)

        f1 = f1_wickets.Name.tolist()
        f1.reverse()

        f2 = f2_wickets.Name.tolist()
        f2.reverse()

        fig = make_subplots(cols=1, rows=2, shared_xaxes=True, row_heights = [0.5,0.5], vertical_spacing = 0.2)


        fig.add_trace(go.Bar(x = f1_wickets['Wickets'],
                            y = f1_wickets['Name'],
                            orientation = 'h',
                            text = f1_wickets['Wickets'],
                            marker = dict(color = head_to_head.loc[head_to_head['Team'] == franchise1, 'Color'].values[0])),
                    row = 1,
                    col = 1)

        fig.add_trace(go.Bar(x = f2_wickets['Wickets'],
                            y = f2_wickets['Name'],
                            orientation = 'h',
                            text = f2_wickets['Wickets'],
                            marker = dict(color = head_to_head.loc[head_to_head['Team'] == franchise2, 'Color'].values[0])),
                    row = 2,
                    col = 1)

        fig.update_xaxes(showticklabels=False)

        fig.update_yaxes(categoryorder='array',
                        categoryarray=f1,
                        row = 1,
                        col = 1)

        fig.update_yaxes(categoryorder='array',
                        categoryarray=f2,
                        row = 2,
                        col = 1)

        fig.update_yaxes(linecolor = 'white')

        fig.update_traces(name='' , hovertemplate='%{y}: %{x} Wickets', insidetextanchor='middle')

        fig.add_annotation(text=f'<b>{franchise1}</b>',
                        font = dict(color = '#444444',family='Verdana',size=14),
                        showarrow = False,
                        xref = 'paper',
                        yref = 'paper',
                        x=0,
                        y=1.09)

        fig.add_annotation(text=f'<b>{franchise2}</b>',
                        font = dict(color = '#444444',family='Verdana',size=14),
                        showarrow = False,
                        xref = 'paper',
                        yref = 'paper',
                        x=0,
                        y=0.46)

        fig.update_layout(plot_bgcolor='white',
                        font = dict(color='#444444', family='Verdana', size=12),
                        height = 600,
                        width = 600,
                        showlegend = False)

        return fig
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)

# Generates the graph showing the standings of the franchises over the years
# head_to_head dataframe is used to map the colors uniformly

def headToHeadStandings(points_table,franchise1,franchise2,head_to_head):
    try:
        position1 = points_table[points_table['TeamName'] == franchise1][['Year','Standings']]
        position1['Color'] = position1['Standings'].apply(lambda x: '#02894B' if x <= 4 else '#EF3340')

        position2 = points_table[points_table['TeamName'] == franchise2][['Year','Standings']]
        position2['Color'] = position2['Standings'].apply(lambda x: '#02894B' if x <= 4 else '#EF3340')

        fig = go.Figure()

        color1 = head_to_head.loc[head_to_head['Team'] == franchise1, 'Color'].values[0]
        color2 = head_to_head.loc[head_to_head['Team'] == franchise2, 'Color'].values[0]

        fig.add_trace(go.Scatter(x = position1.Year,
                                y = position1.Standings,
                                name = franchise1,
                                mode = 'lines+markers',
                                marker = dict(size = 10, color = position1.Color, line_color = position1.Color, line_width = 2),
                                line = dict(width = 1, color = color1)))

        fig.add_trace(go.Scatter(x = position2.Year,
                                y = position2.Standings,
                                name = franchise2,
                                mode = 'lines+markers',
                                marker = dict(size = 12, color = position2.Color),
                                line = dict(width = 1, color = color2)))

        fig.update_yaxes(showticklabels = True, autorange= 'reversed', title_text = 'Standings', showgrid=False)
        fig.update_xaxes(title_text = 'Year',showgrid=False)
        fig.update_traces(hovertemplate='%{x}: %{y}')

        fig.update_layout(plot_bgcolor = 'white',
                        height = 600,
                        width = 800,
                        font = dict(family='Verdana',size = 12,color='#444444'),
                        showlegend=False)
                    
        return fig
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)

# Generates the graph showing the average squad age of the franchises over the years
# head_to_head dataframe is used to map the colors uniformly

def headToHeadAge(player_stats,franchise1,franchise2,head_to_head):
    try:
        team_average_age = None

        for team in player_stats['TeamName'].unique():
            average_age = player_stats[player_stats['TeamName'] == team][['Year','Age']].groupby('Year').agg('mean').apply(lambda x:round(x,1)).reset_index()
            average_age['Team'] = team
            if team_average_age is None:
                team_average_age = average_age
            else:
                team_average_age = pd.concat([team_average_age,average_age],ignore_index=True)

        f1 = team_average_age.loc[team_average_age['Team'] == franchise1]
        f2 = team_average_age.loc[team_average_age['Team'] == franchise2]

        fig = go.Figure()

        color1 = head_to_head.loc[head_to_head['Team'] == franchise1, 'Color'].values[0]
        color2 = head_to_head.loc[head_to_head['Team'] == franchise2, 'Color'].values[0]
            
        fig.add_trace(go.Scatter(x = f1.Year,
                                y = f1.Age,
                                name = franchise1,
                                mode = 'lines+markers',
                                marker = dict(size = 6, color = color1),
                                line = dict(width = 1, color = color1)))

        fig.add_trace(go.Scatter(x = f2.Year,
                                y = f2.Age,
                                name = franchise2,
                                mode = 'lines+markers',
                                marker = dict(size = 6, color = color2),
                                line = dict(width = 1, color = color2)))

        fig.update_yaxes(showticklabels=True, title_text = 'Age', showgrid=False)
        fig.update_xaxes(showticklabels=True, title_text = 'Year', showgrid=False)
        fig.update_traces(hovertemplate='%{x}: %{y} Years')

        fig.update_layout(plot_bgcolor='white',
                        showlegend = False,
                        height = 600,
                        width = 800,
                        font = dict(family='Verdana',size = 12,color='#444444'))

        return fig
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)