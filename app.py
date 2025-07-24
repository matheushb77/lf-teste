from flask import Flask, render_template, request, redirect, url_for, flash, session
from config import Config
from models import db, Usuario
import re

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'chave-secreta-lf-test'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    erros = []
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        cpf = request.form.get('cpf', '').strip()
        telefone = request.form.get('telefone', '').strip()
        senha = request.form.get('senha', '').strip()
        confirmar_senha = request.form.get('confirmar_senha', '').strip()

        if not nome:
            erros.append("O nome completo é obrigatório.")

        if not cpf or not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf):
            erros.append("O CPF deve estar no formato 000.000.000-00.")

        if not telefone or not re.match(r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$', telefone):
            erros.append("O telefone deve estar no formato (DDD) 99999-9999.")

        if not senha or len(senha) < 6 or not re.search(r'[A-Za-z]', senha) or not re.search(r'\d', senha):
            erros.append("A senha deve conter no mínimo 6 caracteres, com pelo menos uma letra e um número.")

        if senha != confirmar_senha:
            erros.append("As senhas não coincidem.")

        usuario_existente = Usuario.query.filter_by(cpf=cpf).first()
        if usuario_existente:
            erros.append("Já existe um usuário cadastrado com este CPF.")

        if erros:
            return render_template('cadastro.html', erros=erros)

        novo_usuario = Usuario(nome=nome, cpf=cpf, telefone=telefone, senha=senha)
        db.session.add(novo_usuario)
        db.session.commit()

        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('login'))

    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cpf = request.form['cpf']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(cpf=cpf, senha=senha).first()

        if usuario:
            return redirect(url_for('dashboard'))
        else:
            flash('CPF ou senha inválidos!', 'error')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# ======== ÁREA ADMIN ========

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        senha = request.form.get('senha')
        if senha == 'minhaSenhaForte123!':  # TROQUE POR UMA SENHA SÓ SUA!
            session['admin'] = True
            return redirect(url_for('admin_usuarios'))
        else:
            flash('Senha de administrador incorreta!', 'error')
    return '''
        <h2>Login do Administrador</h2>
        <form method="post">
            <input type="password" name="senha" placeholder="Senha admin">
            <button type="submit">Entrar</button>
        </form>
    '''

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/usuarios')
def admin_usuarios():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    usuarios = Usuario.query.all()
    return render_template('admin_usuarios.html', usuarios=usuarios)

# ==============================

if __name__ == '__main__':
    app.run(debug=True)
