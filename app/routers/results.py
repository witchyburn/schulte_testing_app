import io
import base64
import sys
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
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
    
    graph_url = generate_times_chart(result.times, result.average_time)
    return templates.TemplateResponse(
        'results.html',
        {
            'request': request,
            'result': result,         
            'graph_url': graph_url
        }
    )

def generate_times_chart(times: list[float], avg_time: float) -> str:
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans"]
    plt.rcParams['axes.labelcolor'] = '#333'
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.rcParams['axes.labelsize'] = 16

    attempts = range(1, len(times) + 1)
    plt.figure(figsize=(10, 6))
    plt.plot(attempts,
             times,
             color='#667eea',
             linestyle='-',
             linewidth=2,
             marker='o',
             markersize=12,
             markerfacecolor='#764ba2')
    for i, num in enumerate(times):
        plt.text(attempts[i], times[i] + (avg_time * 0.01), f'{num:.1f}', fontsize=10, ha='center', va='bottom')
    plt.xlabel('Номер попытки')
    plt.ylabel('Время, сек')
    plt.grid(True, alpha=0.3)
    plt.xticks(attempts, fontsize=14, color="#333")
    plt.yticks(fontsize=14, color="#333")

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    plt.close()
    buf.seek(0)

    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return f'data:image/png;base64,{image_base64}'