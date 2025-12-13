from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uuid

router = APIRouter(prefix='/tests', tags=['tests'])
templates = Jinja2Templates(directory='/app/templates')

@router.get('/start', response_class=HTMLResponse)
async def start_test(request: Request):
    session_id = uuid.uuid4()
    return templates.TemplateResponse(
        'test.html',
        {'request': request, 'session_id': session_id}
    )