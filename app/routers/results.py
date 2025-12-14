import io
import base64
import sys
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import plotly.express as px
import matplotlib.pyplot as plt
from crud import create_test_result, get_test_result
from schemas import TestResultCreate
from database import get_db

sys.path.append("/app/")

router = APIRouter(prefix='/results', tags=['results'])
templates = Jinja2Templates(directory='/app/templates')

@router.post('/submit')
async def submit_results(
    test_data: TestResultCreate,
    db: Session = Depends(get_db)    
):
    result = create_test_result(db, test_data)
    return {'result_id': result.id}

@router.get('/{result_id}', response_class=HTMLResponse)
async def show_results(
    result_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    result = get_test_result(db, result_id)
    if not result:
        raise HTTPException(status_code=404, detail='Result not found')
    
    graph_json = plotly_chart(result.times)

    return templates.TemplateResponse(
        'results.html',
        {
            'request': request,
            'result': result,         
            'graph_json': graph_json
        }
    )

def plotly_chart(times: list[float]) -> str:
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