from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method =='POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Login efetuado com sucesso!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Senha Incompativel, tente novamente!", category='error')
        else:
            flash('Usuario nao encontrado, tente se Cadastar.', category='error')

    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method=='POST':
        email = request.form.get('email')
        nome = request.form.get('name')
        senha1 = request.form.get('password1')
        senha2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user: 
            flash('Email ja cadastrado, tente outro email ou faca Login!', category='error')
        elif len(email) < 6 :
            flash('Email Invalido, tente novamente com outro.', category='error')
        elif len(nome) < 2 :
            flash('Nome Invalido, tente um nome maior', category='error')
        elif len(senha1) < 6:
            flash('Senha muito curta, minimo de 7 caracteres', category='error')
        elif senha1 != senha2:
            flash('Senhas incoerentes, tente novamente.', category='error')
        else:
            # add to database
            new_user = User(email=email, name=nome, password=generate_password_hash(senha2, method='pbkdf2'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Cadastro Realizado!', category='success')
            return redirect(url_for('views.home'))
    return render_template('sign_up.html', user=current_user)