import plotly.express as px

def test_attempts_chart(times: list[float]) -> str:
    attempts = range(1, 6)
    fig = px.line(
        x=attempts,
        y=times,
        labels={'x': 'попытка',
                'y': 'время, сек'},
        markers=True
    )

    fig.update_layout(
        xaxis=dict(
            title='Номер попытки',
            tickfont=dict(size=14),
            title_font=dict(size=16, weight='bold'),
        ),
        yaxis=dict(
            title='Время, сек',
            tickfont=dict(size=14),
            title_font=dict(size=16, weight='bold'),
        ),
        font_family='Arial, sans-serif',
        margin=dict(l=50, r=50, t=25, b=50),
        plot_bgcolor='white',
        font_color='#333'
    )

    fig.update_traces(
        line=dict(width=3, color='#667eea'),
        marker=dict(color='#764ba2', size=10)
    )
    
    fig.update_xaxes(type='category')

    return fig.to_json()