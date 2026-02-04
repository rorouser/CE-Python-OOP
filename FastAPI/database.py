#database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# El archivo se creará automáticamente como 'usuarios.db'
SQLALCHEMY_DATABASE_URL = "sqlite:///./usuarios.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False,
bind=engine)

Base = declarative_base()

# Dependencia para obtener la DB en cada ruta
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()