from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Dieta(Base):
    __tablename__ = 'dietas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    firebase_uuid = Column(String(128), unique=True, nullable=False)
    refeicoes = relationship('Refeicao', back_populates='dieta', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'firebase_uuid': self.firebase_uuid,
            'refeicoes': [refeicao.to_dict() for refeicao in self.refeicoes]
        }

class Refeicao(Base):
    __tablename__ = 'refeicoes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String(128), nullable=False)
    dieta_id = Column(Integer, ForeignKey('dietas.id'), nullable=False)
    dieta = relationship('Dieta', back_populates='refeicoes')
    alimentos = relationship('Alimento', back_populates='refeicao', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'tipo': self.tipo,
            'alimentos': [alimento.to_dict() for alimento in self.alimentos]
        }

class Alimento(Base):
    __tablename__ = 'alimentos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    quantidade = Column(String(255), nullable=False)
    refeicao_id = Column(Integer, ForeignKey('refeicoes.id'), nullable=False)
    refeicao = relationship('Refeicao', back_populates='alimentos')

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'quantidade': self.quantidade
        }
