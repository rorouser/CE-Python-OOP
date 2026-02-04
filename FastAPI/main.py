# main.py
from typing import List
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models import Gender, Role, User, UpdateUser

app = FastAPI()

# Montamos la carpeta de archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuramos la carpeta de plantillas
templates = Jinja2Templates(directory="templates")

db: List[User] = [
    User(id=uuid4(), first_name="John", last_name="Doe",
gender=Gender.male, roles=[Role.user]),
    User(id=uuid4(), first_name="Jane", last_name="Doe",
gender=Gender.female, roles=[Role.user])
]

# --- RUTA PARA CARGAR EL FRONTEND ---
@app.get("/")
async def read_index(request: Request):
    # Esto busca en /templates/index.html y le pasa el request para que pueda usarlo en la plantilla
    return templates.TemplateResponse("index.html", {"request":request})

@app.get("/api/v1/users")
async def get_users():
    return db

@app.get("/api/v1/users/{id}")
async def get_users(id: UUID):
    for user in db:
        if user.id == id:
            return user
    raise HTTPException(status_code=404, detail=f"User with id: {id} not found.")

@app.post("/api/v1/users")
async def create_user(user: User):
    # Si el ID no viene, lo generamos
    if not user.id:
        user.id = uuid4()
    db.append(user)
    return user

@app.delete("/api/v1/users/{id}")
async def delete_user(id: UUID):
    for user in db:
        if user.id == id:
            db.remove(user)
            return{ "detail": "User deleted"}
    raise HTTPException(status_code=404, detail=f"Delete user failed, id {id} not found.")

@app.put("/api/v1/users/{id}")
async def update_user(user_update: UpdateUser, id: UUID):
    for user in db:
        if user.id == id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return user.id
    raise HTTPException(status_code=404, detail=f"Could not find user with id: {id}")
