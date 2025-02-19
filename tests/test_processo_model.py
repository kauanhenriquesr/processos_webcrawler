import pytest
from src import app, db, Processo

@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()

def test_processo_creation(test_client):
    processo = Processo(
        numero_processo='123456',
        link='https://example.com/processo/123456',
        last_change = ' ',
        tribunal='STJ',
        verificacao_diaria=True
    )
    
    db.session.add(processo)
    db.session.commit()
    
    retrieved = db.session.get(Processo, '123456')
    assert retrieved.tribunal == 'STJ'
    assert retrieved.verificacao_diaria is True
    assert retrieved.separado is False