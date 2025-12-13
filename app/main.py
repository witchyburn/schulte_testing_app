from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from models import Base
from database import engine
from routers import tests, results
import uvicorn

app = FastAPI(title="Schulte Test App")

app.mount("/static", StaticFiles(directory="/app/static"), name="static")
templates = Jinja2Templates(directory='/app/templates')

app.include_router(tests.router)
app.include_router(results.router)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)