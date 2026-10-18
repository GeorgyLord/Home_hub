from fastapi import FastAPI, Request
# from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles

from backend.myfunctions import *
from backend.myclasses import *

app = FastAPI()
db_manager = DatabaseManager()
templates = Jinja2Templates(directory="frontend/templates")


@app.post("/api/send-data")
async def receive_data(data: dict):
    task = Task()
    # Читаем тему, дату и текст из JS
    task.set_subject(data.get("subject", "Без темы"))
    task.set_data(data.get("date", ""))
    task.set_text(data.get("text", ""))
    
    db_manager.add_task(task)
    return {"status": "success"}

@app.post("/api/update-task")
async def update_task_endpoint(data: dict):
    task_id = data.get("id")
    new_subject = data.get("subject", "Без темы")
    new_date = data.get("date", "")
    new_text = data.get("text", "")
    
    if not task_id:
        return {"status": "error", "message": "ID задачи не передан"}
        
    # Обновите метод в DatabaseManager, чтобы он перезаписывал еще и subject:
    # UPDATE tasks SET subject = ?, text = ?, data = ? WHERE id = ?
    with sqlite3.connect(db_manager.db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET subject = ?, text = ?, data = ? WHERE id = ?",
            (new_subject, new_text, new_date, int(task_id))
        )
        conn.commit()
        success = cursor.rowcount > 0
        
    if success:
        return {"status": "success"}
    return {"status": "error", "message": "Ошибка обновления"}

@app.post("/api/delete-task")
async def delete_task_endpoint(data: dict):
    task_id = data.get("id")
    
    if not task_id:
        return {"status": "error", "message": "ID задачи не передан"}
        
    success = db_manager.delete_task(int(task_id))
    
    if success:
        return {"status": "success"}
    return {"status": "error", "message": "Не удалось удалить задачу"}


@app.get("/welcome")
def read_root():
    return {"message": "Привет! Теперь тут не проводник."}


@app.get("/", response_class=HTMLResponse)
async def welcome_page(request: Request):
    
    all_tasks = db_manager.get_all_tasks()
    # print(all_tasks)
    
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "Главная",
            "nowdata": get_current_date_format_1(),
            "tasks": all_tasks
        }
    )
