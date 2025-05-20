import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# Generate sample data
def generate_sample_data(num_users=5, days=30):
    # Create date range
    dates = [datetime.now() - timedelta(days=x) for x in range(days)]
    dates.reverse()
    
    data = []
    for user_id in range(1, num_users + 1):
        # Generate base scores with some randomness
        base_score = np.random.normal(70, 10, days)
        
        # Add trend - some users improving, some declining
        trend = np.linspace(-10 if user_id % 2 else 10, 0, days)
        scores = base_score + trend
        
        # Clip scores to be between 0 and 100
        scores = np.clip(scores, 0, 100)
        
        for date, score in zip(dates, scores):
            data.append({
                'Date': date,
                'User': f'User {user_id}',
                'Wellness Score': round(score, 2)
            })
    
    return pd.DataFrame(data)

# Create visualization
def plot_wellness_scores(df):
    fig = go.Figure()
    
    for user in df['User'].unique():
        user_data = df[df['User'] == user]
        
        # Calculate if user is improving or declining
        score_change = user_data['Wellness Score'].iloc[-1] - user_data['Wellness Score'].iloc[0]
        trend = '📈 Improving' if score_change > 0 else '📉 Declining'
        
        fig.add_trace(go.Scatter(
            x=user_data['Date'],
            y=user_data['Wellness Score'],
            name=f"{user} ({trend})",
            mode='lines+markers',
            line=dict(width=2),
            marker=dict(size=8)
        ))
    
    fig.update_layout(
        title='Wellness Scores Comparison Over Time',
        xaxis_title='Date',
        yaxis_title='Wellness Score',
        yaxis=dict(range=[0, 100]),
        hovermode='x unified',
        template='plotly_white'
    )
    
    # Add a legend
    fig.update_layout(
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    # Save the plot as HTML
    fig.write_html('wellness_trends.html')

def main():
    # Generate sample data
    df = generate_sample_data()
    
    # Create and save the visualization
    plot_wellness_scores(df)
    print("Visualization has been created and saved as 'wellness_trends.html'")

if __name__ == "__main__":
    main()
