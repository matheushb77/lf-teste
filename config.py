import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Caminho do banco de dados SQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'lf_test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
