import sys
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from crud import create_test_result, get_test_result
from schemas import TestResultCreate
from database import get_db
from graphs import test_attempts_chart

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
    
    graph_json = test_attempts_chart(result.times)

    return templates.TemplateResponse(
        'results.html',
        {
            'request': request,
            'result': result,         
            'graph_json': graph_json
        }
    )