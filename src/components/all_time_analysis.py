# Module generates all the charts that are present under the all-time analysis tab

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import sys

from src.exception import CustomException
from src.logger import logging

# Generates the bar chart displaying the ipl winners

def topTitlesGraph(titles):

    # Gets the order in which the names have to displayed on the y-axis
    try:
        NAME_ORDER = titles['Team Name'].tolist()
        NAME_ORDER.reverse()
        
        fig = go.Figure()

        fig.add_trace(go.Bar(x = titles['Wins'],
                            y = titles['Team Name'],
                            orientation = 'h',
                            text = titles['Wins'],
                            textposition = 'inside',
                            insidetextanchor = 'middle',
                            hovertemplate = '%{y}:%{x} Titles',
                            name = '',
                            marker = dict(color = '#F8D210')))

        fig.update_xaxes(showticklabels=False)

        fig.update_layout(plot_bgcolor = 'white',
                        font = dict(color = '#444444',family='Verdana',size=12),
                        title = dict(text = '<b>IPL Winners</b>', font_size = 24),
                        showlegend = False,
                        yaxis = dict(linecolor = 'white',categoryorder = 'array',categoryarray = NAME_ORDER))
        
        return fig
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)

# Generates the bar chart displaying the distribution of wins

def topWinsTeamGraph(matches):

    try:

        winners = matches[['Winner','city']].groupby('Winner').count().reset_index().sort_values('city',ascending=False)
        winners = winners.drop(winners[winners['Winner'] == 'No Result'].index[0])
        winners.rename(columns={'city':'Win'},inplace=True)

        # Gets the order in which the names have to be displayed along the y-axis

        NAME_ORDER = winners['Winner'].tolist()
        NAME_ORDER.reverse()

        fig = go.Figure()

        top = winners.Winner.iloc[0]
        wins = winners[winners['Winner'] == top].Win.values[0]

        top_df = winners.loc[winners['Winner'] == top]
        non_top_df = winners.loc[winners['Winner'] != top]

        fig.add_trace(go.Bar(x = non_top_df['Win'],
                            y = non_top_df['Winner'],
                            orientation = 'h',
                            text = non_top_df['Win'],
                            insidetextanchor = 'middle',
                            marker = dict(color = '#c5c5c5')))

        fig.add_trace(go.Bar(x = top_df['Win'],
                            y = top_df['Winner'],
                            orientation = 'h',
                            text = top_df['Win'],
                            marker = dict(color = '#057DCD')))

        fig.update_xaxes(showticklabels=False)

        fig.update_traces(name='', hovertemplate='%{y} : %{x} Wins')

        title_text = f'<b><span style="color:#057DCD">{top}</span> leads the list with <span style="color:#057DCD">{wins}</span> wins</b>'

        fig.update_layout(plot_bgcolor = 'white',
                        height = 600,
                        font = dict(color = '#444444',family='Verdana',size=12),
                        title = dict(text = title_text),
                        showlegend = False,
                        yaxis = dict(linecolor = 'white',categoryorder = 'array',categoryarray = NAME_ORDER))
        
        return fig
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)

# Generates the graphs for player participation over the years

def playerStrength(player_stats):

    try:
    
        player_strength = { 'Year' : [], 'Indian' : [], 'Overseas' : []}

        # Filters the number of indian and overseas players based on the year

        for year in player_stats.Year.unique():
            player_count = player_stats.Nationality[(player_stats['Year'] == year)].value_counts().reset_index().rename(columns={'index':'Domicile','Nationality':'Strength'})
            player_strength['Year'].append(year)
            player_strength['Indian'].append(player_count.iloc[0,-1])
            player_strength['Overseas'].append(player_count.iloc[1,-1])
            
        player_strength = pd.DataFrame(player_strength)

        fig = make_subplots(cols=1, rows=2, shared_xaxes=True, row_heights = [0.3,0.7], vertical_spacing = 0.05)

        fig.add_trace(go.Scatter(x = player_strength.Year,
                                y = player_strength.Overseas,
                                name = 'Overseas',
                                hovertemplate = '%{x} : %{y}',
                                marker = dict(size = 8),
                                line = dict(width = 1,
                                        color = '#FA26A0')),
                    row = 1,
                    col = 1)

        for column, color in [('Indian','#F8D210'), ('Overseas','#FA26A0')]:
            fig.add_trace(go.Bar(x = player_strength.Year,
                                y = player_strength[column].tolist(),
                                name = column,
                                hovertemplate = '(%{x}:%{y})',
                                text = player_strength[column].tolist(),
                                textposition = 'inside',
                                insidetextanchor = 'middle',
                                width = 0.6,
                                marker = dict(color = color,
                                            line_width = 0)),
                        row = 2,
                        col = 1)    

        fig.add_annotation(text='<b>Overseas Players per Season over the Years</b>',
                        font = dict(color = '#444444',family='Verdana',size=13),
                        showarrow = False,
                        xref = 'paper',
                        yref = 'paper',
                        x=0,
                        y=1.075)

        fig.add_annotation(text='<b>Players per Season over the Years</b>',
                        font = dict(color = '#444444',family='Verdana',size=13),
                        showarrow = False,
                        xref = 'paper',
                        yref = 'paper',
                        x=0,
                        y=0.65)

        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        fig.update_yaxes(showticklabels=False, row = 2, col = 1)
            
        fig.update_layout(barmode='stack',
                        width = 900,
                        height = 800,
                        plot_bgcolor = 'white',
                        showlegend = True,
                        font = dict(family='Verdana',size = 10,color='#444444'))
            
        return fig
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)

# Generates the bar graph for leading run scorers

def topRunsGraph(player_stats, nationality):

    try:
    
        if nationality == 'Indian and Overseas':
            top_runs = player_stats[['Name','TotalRuns']].groupby('Name').sum().reset_index().sort_values('TotalRuns',ascending = False).head(20)
        else:
            top_runs = player_stats[player_stats['Nationality'] == nationality][['Name','TotalRuns']].groupby('Name').sum().reset_index().sort_values('TotalRuns',ascending = False).head(20)

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
        
        # Adding the bar chart for the leading run scorer separately with a specific color

        fig.add_trace(go.Bar(x = top_df['TotalRuns'],
                            y = top_df['Name'],
                            orientation = 'h',
                            text = top_df['TotalRuns'],
                            marker = dict(color = '#ffa500')))

        fig.update_xaxes(showticklabels=False)

        fig.update_traces(name='' , hovertemplate='%{y}: %{x} Runs', insidetextanchor='middle')

        title_text = f'<b><span style="color:#ffa500">{top}</span> leads the list with <span style="color:#ffa500">{runs}</span> runs</b>'

        fig.update_layout(plot_bgcolor = 'white',
                        height = 700,
                        font = dict(color = '#444444',family='Verdana',size=12),
                        title = dict(text = title_text),
                        showlegend = False,
                        yaxis = dict(linecolor = 'white',categoryorder = 'array',categoryarray = NAME_ORDER))
        
        return fig
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)

# Generates the bar graph for leading wicket scorers

def topWicketsGraph(player_stats,nationality):

    try:
        if nationality == 'Indian and Overseas':
            top_wickets = player_stats[['Name','Wickets']].groupby('Name').sum().reset_index().sort_values('Wickets',ascending = False).head(20)
        else:
            top_wickets = player_stats[player_stats['Nationality'] == nationality][['Name','Wickets']].groupby('Name').sum().reset_index().sort_values('Wickets',ascending = False).head(20)

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
        
        # Adding the bar chart for the leading wicket taker separately with a specific color

        fig.add_trace(go.Bar(x = top_df['Wickets'],
                            y = top_df['Name'],
                            orientation = 'h',
                            text = top_df['Wickets'],
                            marker = dict(color = '#A020F0')))

        fig.update_xaxes(showticklabels=False)

        fig.update_traces(name='' , hovertemplate='%{y}: %{x} Wickets', insidetextanchor = 'middle')

        title_text = f'<b><span style="color:#A020F0">{top}</span> leads the list with <span style="color:#A020F0">{wickets}</span> wickets</b>'

        fig.update_layout(plot_bgcolor = 'white',
                        height = 700,
                        font = dict(color = '#444444',family='Verdana',size=12),
                        title = dict(text = title_text),
                        showlegend = False,
                        yaxis = dict(linecolor = 'white',categoryorder = 'array',categoryarray = NAME_ORDER))
        
        return fig
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)

# Generates the graphs for fifties and hundreds over the years

def battingLandmark(player_stats,nationality):

    try:
    
        if nationality == 'Indian and Overseas':
            landmarks = player_stats[['Year','FiftyPlusRuns','Centuries']].groupby('Year').sum().reset_index()
        else:
            landmarks = player_stats[player_stats['Nationality'] == nationality][['Year','FiftyPlusRuns','Centuries']].groupby('Year').sum().reset_index()
        
        landmarks.FiftyPlusRuns = landmarks.FiftyPlusRuns.astype(int)
        landmarks.Centuries = landmarks.Centuries.astype(int)

        fig = make_subplots(cols=1, rows=2, shared_xaxes=True,subplot_titles=['<b>100s per Season</b>','<b>50s and 100s per Season</b>'], row_heights = [0.3,0.7], vertical_spacing = 0.05)

        fig.add_trace(go.Scatter(x = landmarks.Year,
                                y = landmarks.Centuries,
                                name = 'Centuries',
                                hovertemplate = '%{x} : %{y}',
                                marker = dict(size = 8),
                                line = dict(width = 1,
                                        color = '#FA26A0')),
                    row = 1,
                    col = 1)

        for column, color in [('FiftyPlusRuns','#F8D210'), ('Centuries','#FA26A0')]:
            fig.add_trace(go.Bar(x = landmarks.Year,
                                y = landmarks[column].tolist(),
                                name = column,
                                hovertemplate = '(%{x}: %{y})',
                                text = list(map(lambda x: '' if x==0 else x, landmarks[column].tolist())),
                                textposition = 'outside',
                                width = 0.6,
                                marker = dict(color = color,
                                            line_width = 0)),
                        row = 2,
                        col = 1)
            
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        fig.update_yaxes(showticklabels=False, row = 2, col = 1)
            
        fig.update_layout(barmode='stack',
                        width = 900,
                        height = 900,
                        plot_bgcolor = 'white',
                        font = dict(family='Verdana',size = 10,color='#444444'))
            
        return fig
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)

# Generates the graphs for four and five wicket hauls over the years

def bowlingLandmark(player_stats,nationality):

    try:
    
        if nationality == 'Indian and Overseas':
            landmarks = player_stats[['Year','FourWickets','FiveWickets']].groupby('Year').sum().reset_index()
        else:
            landmarks = player_stats[player_stats['Nationality'] == nationality][['Year','FourWickets','FiveWickets']].groupby('Year').sum().reset_index()
        
        landmarks.FourWickets = landmarks.FourWickets.astype(int)
        landmarks.FiveWickets = landmarks.FiveWickets.astype(int)

        fig = make_subplots(cols=1, rows=2, shared_xaxes=True,subplot_titles=['<b>5 fors per Season</b>','<b>4 and 5 fors per Season</b>'], row_heights = [0.3,0.7], vertical_spacing = 0.05)

        fig.add_trace(go.Scatter(x = landmarks.Year,
                                y = landmarks.FiveWickets,
                                name = 'Five fors',
                                hovertemplate = '%{x} : %{y}',
                                marker = dict(size = 8),
                                line = dict(width = 1,
                                        color = '#FA26A0')),
                    row = 1,
                    col = 1)

        for column, color, name in [('FourWickets','#F8D210','Four fors'), ('FiveWickets','#FA26A0','Five fors')]:
            fig.add_trace(go.Bar(x = landmarks.Year,
                                y = landmarks[column].tolist(),
                                name = name,
                                hovertemplate = '(%{x}: %{y})',
                                text = list(map(lambda x: '' if x==0 else x, landmarks[column].tolist())),
                                textposition = 'outside',
                                width = 0.6,
                                marker = dict(color = color,
                                            line_width = 0)),
                        row = 2,
                        col = 1)      
        
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        fig.update_yaxes(showticklabels=False, row = 2, col = 1)
            
        fig.update_layout(barmode='stack',
                        width = 900,
                        height = 900,
                        plot_bgcolor = 'white',
                        font = dict(family='Verdana',size = 10,color='#444444'))
            
        return fig
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)

# Generates the graphs for boundaries scored over the years

def boundaryCount(player_stats,nationality):

    try:
    
        if nationality == 'Indian and Overseas':
            boundaries = player_stats[['Year','Fours','Sixes']].groupby('Year').sum().reset_index()
        else:
            boundaries = player_stats[player_stats['Nationality'] == nationality][['Year','Fours','Sixes']].groupby('Year').sum().reset_index()
        
        boundaries.Fours = boundaries.Fours.astype(int)
        boundaries.Sixes = boundaries.Sixes.astype(int)

        fig = make_subplots(cols=1, rows=2, shared_xaxes=True,subplot_titles=['<b>Sixes per Season</b>','<b>Boundaries per Season</b>'], row_heights = [0.3,0.7], vertical_spacing = 0.05)

        fig.add_trace(go.Scatter(x = boundaries.Year,
                                y = boundaries.Sixes,
                                name = 'Sixes',
                                marker = dict(size = 8),
                                line = dict(width = 1,
                                        color = '#FA26A0')),
                    row = 1,
                    col = 1)

        for column, color in [('Fours','#F8D210'), ('Sixes','#FA26A0')]:
            fig.add_trace(go.Bar(x = boundaries.Year,
                                y = boundaries[column].tolist(),
                                name = column,
                                hovertemplate = '(%{x},%{y})',
                                text = boundaries[column].tolist(),
                                textposition = 'inside',
                                insidetextanchor = 'middle',
                                width = 0.7,
                                marker = dict(color = color,
                                            line_width = 0)),
                        row = 2,
                        col = 1)
        
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        fig.update_yaxes(showticklabels=False, row = 2, col = 1)

        fig.update_layout(barmode='stack',
                        width = 900,
                        height = 900,
                        plot_bgcolor = 'white',
                        font = dict(family='Verdana',size = 10,color='black'))
            
        return fig
    
    except Exception as e:
        logging.error(CustomException(e,sys))
        raise CustomException(e,sys)

# Generates the html to be displayed on clicking the marker on the folium map

def popup_html(row,ground_data,matches):
        
        try:
        
            # Average first innings score is calculated for each ground

            avg_innings_score = matches[['GroundName','Runs1']][matches['Runs1'] > 0].groupby('GroundName').agg('mean').apply(lambda x: round(x,0)).astype(int).reset_index().rename(columns={'GroundName':'Ground Name','Runs1':'Average First Innings Score'})

            # Labelling winners batting first and second, and the matches with no result

            bat_first = matches
            bat_first['WinnerBattingFirst'] = np.where((matches['FirstBattingTeamName'] == matches['Winner']),
                                                'First',
                                                np.where((matches['SecondBattingTeamName'] == matches['Winner']),
                                                        'Second',
                                                        'No Result')
                                                )
            
            # Getting the count of winners batting first, second and matches with no result - for each ground
            bat_first = bat_first[['GroundName','WinnerBattingFirst','Winner']].groupby(['GroundName','WinnerBattingFirst']).count().reset_index()
            
            # Getting the ground data with the help of index
            i = row
            ground_name = ground_data['GroundName'].iloc[i]
            ground_city = ground_data['City'].iloc[i]

            matches_held = matches[matches['GroundName'] == ground_name]['MatchRow'].count()
            
            # Getting all the teams with the most wins in a particular ground
            wins_df = matches[matches['GroundName'] == ground_name]['Winner'].value_counts().reset_index().rename(columns={'index':'Team','Winner':'Wins'})
            lst = wins_df['Team'][wins_df['Wins'] == max(wins_df['Wins'])].tolist()
            
            if len(lst)>1:
                most_wins_team = ', '.join(lst)
            else:
                most_wins_team = lst[0]   
            
            wins = max(wins_df['Wins'])
            
            avg_first_inns = avg_innings_score[avg_innings_score['Ground Name'] == ground_name].iloc[0,1]

            if not bat_first[(bat_first['GroundName'] == ground_name) & (bat_first['WinnerBattingFirst'] == 'First')].empty:
                wins_batting_first = bat_first[(bat_first['GroundName'] == ground_name) & (bat_first['WinnerBattingFirst'] == 'First')]['Winner'].values[0]
            else:
                wins_batting_first = 0

            if not bat_first[(bat_first['GroundName'] == ground_name) & (bat_first['WinnerBattingFirst'] == 'Second')].empty:
                wins_batting_second = bat_first[(bat_first['GroundName'] == ground_name) & (bat_first['WinnerBattingFirst'] == 'Second')]['Winner'].values[0]
            else:
                wins_batting_second = 0

            if not bat_first[(bat_first['GroundName'] == ground_name) & (bat_first['WinnerBattingFirst'] == 'No Result')].empty:
                no_result = bat_first[(bat_first['GroundName'] == ground_name) & (bat_first['WinnerBattingFirst'] == 'No Result')]['Winner'].values[0]
            else:
                no_result = 0

            left_col_color = "#EAFBFF"
            right_col_color = "#EAFBFF"

            html = f"""
                        <!DOCTYPE html>
                        
                        <html>
                        <center><h4 style="margin-bottom:5; font-family:Verdana; font-weight:900; width=200px;">{ground_name}</h4></center>
                        <center>
                            <table style="height:120px; width:300px;">
                                <tbody style="font-family:Verdana; font-weight:400;">
                                    <tr>
                                        <td style="background-color:{left_col_color};"><span style="color: #000000;">City </span></td>
                                        <td style="width: 150px;background-color:{right_col_color};">{ground_city}</td>
                                    </tr>
                                    <tr>
                                        <td style="background-color:{left_col_color};"><span style="color: #000000;">Matches Held </span></td>
                                        <td style="width: 150px;background-color:{right_col_color};">{matches_held}</td>
                                    </tr>
                                    <tr>
                                        <td style="background-color:{left_col_color};"><span style="color: #000000;">Team with Most Wins </span></td>
                                        <td style="width: 150px;background-color:{right_col_color};">{most_wins_team} ({wins})</td>
                                    </tr>
                                    <tr>
                                        <td style="background-color:{left_col_color};"><span style="color: #000000;">Average First Innings Score </span></td>
                                        <td style="width: 150px;background-color:{right_col_color};">{avg_first_inns}</td>
                                    </tr>
                                    <tr>
                                        <td style="background-color:{left_col_color};"><span style="color: #000000;">Wins Batting First</span></td>
                                        <td style="width: 150px;background-color:{right_col_color};">{wins_batting_first}</td>
                                    </tr>
                                    <tr>
                                        <td style="background-color:{left_col_color};"><span style="color: #000000;">Wins Batting Second</span></td>
                                        <td style="width: 150px;background-color:{right_col_color};">{wins_batting_second}</td>
                                    </tr>
                                    <tr>
                                        <td style="background-color:{left_col_color};"><span style="color: #000000;">No Result</span></td>
                                        <td style="width: 150px; background-color:{right_col_color};">{no_result}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </center>
                        </html>
                    """

            return html
        
        except Exception as e:
            logging.error(CustomException(e,sys))
            raise CustomException(e,sys)