from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, ForeignKey, Text, Enum, Boolean
from typing import List
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

db = SQLAlchemy()


class TipoUsuario(enum.Enum):
    paciente = "paciente"
    medico = "medico"


class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    tipo_usuario: Mapped[TipoUsuario] = mapped_column(
        Enum(TipoUsuario), nullable=False)

    paciente: Mapped['Paciente'] = relationship(
        back_populates="user", uselist=False)
    medico: Mapped['Medico'] = relationship(
        back_populates="user", uselist=False)

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "tipo_usuario": self.tipo_usuario.value
        }

from sqlalchemy import Date

class Paciente(db.Model):
    __tablename__ = "pacientes"
    id: Mapped[int] = mapped_column(primary_key=True)
    direccion: Mapped[str] = mapped_column(String(255))
    telefono: Mapped[str] = mapped_column(String(20))
    fecha_nacimiento: Mapped[datetime] = mapped_column(nullable=True)
    genero: Mapped[str] = mapped_column(String(20), nullable=True)
    tipo_sangre: Mapped[str] = mapped_column(String(5), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    user: Mapped['User'] = relationship(back_populates="paciente")
    citas: Mapped[List['Cita']] = relationship(back_populates="paciente")
    analisis: Mapped[List['Analisis']] = relationship(back_populates="paciente")
    historial: Mapped[List['HistorialMedico']] = relationship(back_populates="paciente")
    farmacos: Mapped[List['FarmacoAlergeno']] = relationship(back_populates="paciente")
    def serialize(self):
        return {
            "id": self.id,
            "direccion": self.direccion,
            "telefono": self.telefono,
            "user_id": self.user_id,
            "nombre": self.user.nombre if self.user else None,
            "email": self.user.email if self.user else None,
            "tipo_usuario": self.user.tipo_usuario.value if self.user else None,
            "citas": [cita.serialize() for cita in self.citas],
            "analisis": [a.serialize() for a in self.analisis],
            "historial": [h.serialize() for h in self.historial],
            "farmacos": [f.serialize() for f in self.farmacos]
        }



class Medico(db.Model):
    __tablename__ = "medicos"
    id: Mapped[int] = mapped_column(primary_key=True)
    especialidad: Mapped[str] = mapped_column(String(100))
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False)

    user: Mapped['User'] = relationship(back_populates="medico")
    citas: Mapped[List['Cita']] = relationship(back_populates="medico")


class Cita(db.Model):
    __tablename__ = "citas"
    id: Mapped[int] = mapped_column(primary_key=True)
    fecha_hora: Mapped[datetime] = mapped_column(nullable=False)
    estado: Mapped[str] = mapped_column(
        String(20))  # Ej: "pendiente", "confirmada"
    tipo: Mapped[str] = mapped_column(
        String(20))    # Ej: "programada", "libre"
    paciente_id: Mapped[int] = mapped_column(ForeignKey("pacientes.id"))
    medico_id: Mapped[int] = mapped_column(ForeignKey("medicos.id"))

    paciente: Mapped['Paciente'] = relationship(back_populates="citas")
    medico: Mapped['Medico'] = relationship(back_populates="citas")

    def serialize(self):
        return {
            "id": self.id,
            "fecha_hora": self.fecha_hora.isoformat() if self.fecha_hora else None,
            "estado": self.estado,
            "tipo": self.tipo,
            "paciente_id": self.paciente_id,
            "medico_id": self.medico_id
        }


class Analisis(db.Model):
    __tablename__ = "analisis"
    id: Mapped[int] = mapped_column(primary_key=True)
    tipo_analisis: Mapped[str] = mapped_column(String(100))
    resultado: Mapped[str] = mapped_column(nullable=False)
    fecha: Mapped[datetime] = mapped_column(nullable=False)
    paciente_id: Mapped[int] = mapped_column(ForeignKey("pacientes.id"))

    paciente: Mapped['Paciente'] = relationship(back_populates="analisis")

    def serialize(self):
        return {
            "id": self.id,
            "tipo_analisis": self.tipo_analisis,
            "resultado": self.resultado,
            "fecha": self.fecha.isoformat() if self.fecha else None,
            "paciente_id": self.paciente_id
        }


class HistorialMedico(db.Model):
    __tablename__ = "historiales"
    id: Mapped[int] = mapped_column(primary_key=True)
    diagnostico: Mapped[str] = mapped_column(Text)
    tratamiento: Mapped[str] = mapped_column(Text)
    fecha: Mapped[datetime] = mapped_column(nullable=False)
    paciente_id: Mapped[int] = mapped_column(ForeignKey("pacientes.id"))

    paciente: Mapped['Paciente'] = relationship(back_populates="historial")

    def serialize(self):
        return {
            "id": self.id,
            "diagnostico": self.diagnostico,
            "tratamiento": self.tratamiento,
            "fecha": self.fecha.isoformat() if self.fecha else None,
            "paciente_id": self.paciente_id
        }


class FarmacoAlergeno(db.Model):
    __tablename__ = "farmacos_alergenos"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre_farmaco: Mapped[str] = mapped_column(String(100))
    reaccion: Mapped[str] = mapped_column(Text)
    paciente_id: Mapped[int] = mapped_column(ForeignKey("pacientes.id"))

    paciente: Mapped['Paciente'] = relationship(back_populates="farmacos")

    def serialize(self):
        return {
            "id": self.id,
            "nombre_farmaco": self.nombre_farmaco,
            "reaccion": self.reaccion,
            "paciente_id": self.paciente_id
        }
