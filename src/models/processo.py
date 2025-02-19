from datetime import datetime
import src.date_funcs as date_funcs
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Processo(db.Model):
    __tablename__ = 'processos'
    
    numero_processo = db.Column(db.String(100), primary_key=True)
    link = db.Column(db.String(100), nullable=False)
    tribunal = db.Column(db.String(50), nullable=False)
    last_change= db.Column(db.String(500), nullable=False)
    last_verificacion = db.Column(db.DateTime, default=datetime.today())
    verificacao_diaria = db.Column(db.Boolean, default=False, nullable=False)
    separado = db.Column(db.Boolean, default=False, nullable=False)
    
    def __init__(self, numero_processo, link, last_change, tribunal, verificacao_diaria=False, separado=False):
        self.numero_processo = numero_processo
        self.link = link
        self.tribunal = tribunal
        self.last_change = last_change
        self.verificacao_diaria = verificacao_diaria
        self.separado = separado
        
    def __repr__(self) -> str:
        return f'<Processo {self.numero_processo} - {self.tribunal}>'

    # Método para serialização/dicionário (útil para APIs)
    def to_dict(self):# -> dict[str, Any]:
        return {
            'numero_processo': self.numero_processo,
            'link': self.link,
            'tribunal': self.tribunal,
            'verificacao_diaria': self.verificacao_diaria,
            'separado': self.separado,
            'última verificação': date_funcs.date_to_str(self.last_verificacion)
        }

    # Método para atualização de verificação
    def update_verification(self, html):
        self.last_verificacion = datetime.today()
        self.last_change = html
        db.session.commit()

    @classmethod
    def listar_todos(cls):
        """Retorna todos os processos do banco em ordem de cadastro"""
        return cls.query.order_by(cls.last_verificacion).all()

    @classmethod
    def listar_verificacao_diaria(cls):
        """Filtra apenas processos marcados para verificação diária"""
        return cls.query.filter_by(verificacao_diaria=True).order_by(cls.last_verificacion).all()

    @classmethod
    def listar_verificacao_diaria_dict(cls):
        """Versão serializada para APIs/JSON"""
        processos = cls.listar_verificacao_diaria()
        return [processo.to_dict() for processo in processos]
