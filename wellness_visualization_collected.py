import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

def load_and_process_data():
    # Read the data files
    activity_df = pd.read_csv('archive/mturkfitbit_export_3.12.16-4.11.16/Fitabase Data 3.12.16-4.11.16/dailyActivity_merged.csv')
    sleep_df = pd.read_csv('archive/mturkfitbit_export_3.12.16-4.11.16/Fitabase Data 3.12.16-4.11.16/minuteSleep_merged.csv')
    weight_df = pd.read_csv('archive/mturkfitbit_export_3.12.16-4.11.16/Fitabase Data 3.12.16-4.11.16/weightLogInfo_merged.csv')
    
    # Process activity data
    activity_df['ActivityDate'] = pd.to_datetime(activity_df['ActivityDate'])
    
    # Calculate daily sleep duration in hours from minutes data
    sleep_df['date'] = pd.to_datetime(sleep_df['date'])
    sleep_daily = sleep_df.groupby(['Id', 'date'])['value'].sum().reset_index()
    sleep_daily['sleep_hours'] = sleep_daily['value'] / 60
    
    # Merge activity and sleep data
    df = activity_df.merge(sleep_daily[['Id', 'date', 'sleep_hours']], 
                          left_on=['Id', 'ActivityDate'], 
                          right_on=['Id', 'date'], 
                          how='left')
    
    # Calculate wellness score components (normalized between 0-100)
    df['steps_score'] = df['TotalSteps'] / 100  # 10000 steps = 100 points
    df['activity_score'] = (df['VeryActiveMinutes'] + df['FairlyActiveMinutes']) / 60 * 100  # 60 active minutes = 100 points
    df['sleep_score'] = df['sleep_hours'].clip(0, 10) * 10  # 8 hours = 80 points, 10 hours = 100 points
    df['calories_score'] = df['Calories'].clip(1800, 3500) / 35  # normalized to 100
    
    # Calculate overall wellness score (weighted average)
    df['Wellness Score'] = (
        df['steps_score'] * 0.3 +
        df['activity_score'] * 0.2 +
        df['sleep_score'] * 0.3 +
        df['calories_score'] * 0.2
    )
    
    # Clip final scores between 0 and 100
    df['Wellness Score'] = df['Wellness Score'].clip(0, 100)
    
    # Keep only necessary columns
    result_df = df[['Id', 'ActivityDate', 'Wellness Score']].copy()
    result_df = result_df.sort_values('ActivityDate')
    
    return result_df

def plot_wellness_scores(df):
    fig = go.Figure()
    
    # Color palette
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    for i, user_id in enumerate(df['Id'].unique()):
        user_data = df[df['Id'] == user_id].copy()
        
        # Calculate trend
        score_change = user_data['Wellness Score'].iloc[-1] - user_data['Wellness Score'].iloc[0]
        trend = '📈 Improving' if score_change > 0 else '📉 Declining'
        
        # Calculate moving average for smoother line
        user_data['MA7'] = user_data['Wellness Score'].rolling(window=7, min_periods=1).mean()
        
        fig.add_trace(go.Scatter(
            x=user_data['ActivityDate'],
            y=user_data['MA7'],
            name=f"User {user_id} ({trend})",
            mode='lines',
            line=dict(width=3, color=colors[i % len(colors)]),
            hovertemplate="Date: %{x}<br>Score: %{y:.1f}<extra></extra>"
        ))
        
        # Add actual points with lower opacity
        fig.add_trace(go.Scatter(
            x=user_data['ActivityDate'],
            y=user_data['Wellness Score'],
            name=f"User {user_id} (Daily)",
            mode='markers',
            marker=dict(size=6, color=colors[i % len(colors)], opacity=0.5),
            showlegend=False,
            hovertemplate="Date: %{x}<br>Score: %{y:.1f}<extra></extra>"
        ))
    
    fig.update_layout(
        title={
            'text': 'Comprehensive Wellness Score Trends',
            'font': {'size': 24}
        },
        xaxis_title='Date',
        yaxis_title='Wellness Score',
        yaxis=dict(range=[0, 100]),
        hovermode='x unified',
        template='plotly_white',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor='rgba(255, 255, 255, 0.8)'
        ),
        plot_bgcolor='white'
    )
    
    # Add gridlines
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    
    # Save the plot as HTML
    fig.write_html('wv.html')

def main():
    # Load and process the actual Fitbit data
    df = load_and_process_data()
    
    # Create and save the visualization
    plot_wellness_scores(df)
    print("Visualization has been created and saved as 'wv.html'")

if __name__ == "__main__":
    main()