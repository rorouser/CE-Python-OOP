from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List

import models
import dtos
from database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="EventMaster API")


@app.get("/")
def root():
    return {"message": "Bienvenido a EventMaster API"}

@app.post("/recintos/", response_model=dtos.RecintoOut, status_code=201)
def crear_recinto(recinto: dtos.RecintoCreate, db: Session = Depends(get_db)):
    db_recinto = models.Recinto(**recinto.model_dump())
    db.add(db_recinto)
    db.commit()
    db.refresh(db_recinto)
    return db_recinto


@app.get("/recintos/", response_model=List[dtos.RecintoOut])
def listar_recintos(db: Session = Depends(get_db)):
    return db.query(models.Recinto).all()


@app.get("/recintos/{id}", response_model=dtos.RecintoOut)
def obtener_recinto(id: int, db: Session = Depends(get_db)):
    recinto = db.query(models.Recinto).filter(models.Recinto.id == id).first()
    if not recinto:
        raise HTTPException(status_code=404, detail="Recinto no encontrado")
    return recinto


@app.put("/recintos/{id}", response_model=dtos.RecintoOut)
def actualizar_recinto(id: int, datos: dtos.RecintoUpdate, db: Session = Depends(get_db)):
    recinto = db.query(models.Recinto).filter(models.Recinto.id == id).first()
    if not recinto:
        raise HTTPException(status_code=404, detail="Recinto no encontrado")
    for campo, valor in datos.model_dump().items():
        setattr(recinto, campo, valor)
    db.commit()
    db.refresh(recinto)
    return recinto


@app.delete("/recintos/{id}", status_code=204)
def eliminar_recinto(id: int, db: Session = Depends(get_db)):
    recinto = db.query(models.Recinto).filter(models.Recinto.id == id).first()
    if not recinto:
        raise HTTPException(status_code=404, detail="Recinto no encontrado")
    db.delete(recinto)
    db.commit()

@app.post("/eventos/", response_model=dtos.EventoOut, status_code=201)
def crear_evento(evento: dtos.EventoCreate, db: Session = Depends(get_db)):
    # Verificar que el recinto existe
    recinto = db.query(models.Recinto).filter(models.Recinto.id == evento.recinto_id).first()
    if not recinto:
        raise HTTPException(status_code=404, detail="Recinto no encontrado")

    db_evento = models.Evento(**evento.model_dump())
    db.add(db_evento)
    db.commit()
    db.refresh(db_evento)
    return db_evento


@app.get("/eventos/", response_model=List[dtos.EventoOut])
def listar_eventos(ciudad: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Evento).join(models.Recinto)
    if ciudad:
        query = query.filter(models.Recinto.ciudad.ilike(f"%{ciudad}%"))
    return query.all()


@app.get("/eventos/{id}", response_model=dtos.EventoOut)
def obtener_evento(id: int, db: Session = Depends(get_db)):
    evento = db.query(models.Evento).filter(models.Evento.id == id).first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return evento


@app.put("/eventos/{id}", response_model=dtos.EventoOut)
def actualizar_evento(id: int, datos: dtos.EventoUpdate, db: Session = Depends(get_db)):
    evento = db.query(models.Evento).filter(models.Evento.id == id).first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    # Verificar que el nuevo recinto existe si se cambia
    if datos.recinto_id != evento.recinto_id:
        recinto = db.query(models.Recinto).filter(models.Recinto.id == datos.recinto_id).first()
        if not recinto:
            raise HTTPException(status_code=404, detail="Recinto no encontrado")

    for campo, valor in datos.model_dump().items():
        setattr(evento, campo, valor)
    db.commit()
    db.refresh(evento)
    return evento


@app.delete("/eventos/{id}", status_code=204)
def eliminar_evento(id: int, db: Session = Depends(get_db)):
    evento = db.query(models.Evento).filter(models.Evento.id == id).first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    db.delete(evento)
    db.commit()


@app.patch("/eventos/{id}/comprar", response_model=dtos.EventoOut)
def comprar_tickets(id: int, compra: dtos.CompraIn, db: Session = Depends(get_db)):
    evento = db.query(models.Evento).filter(models.Evento.id == id).first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    recinto = evento.recinto
    if evento.tickets_vendidos + compra.cantidad > recinto.capacidad:
        raise HTTPException(
            status_code=400,
            detail="Aforo insuficiente en el recinto"
        )

    evento.tickets_vendidos += compra.cantidad
    db.commit()
    db.refresh(evento)
    return evento
