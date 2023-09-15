from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Note



views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 3:
            flash("Esta nota esta muito curta!", category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Nota adicionada com sucesso!", category="success")
        
    return render_template('home.html', user=current_user)


@views.route('/delete-note', methods=['GET', 'POST'])
def delete_note():
    if request.method == 'POST':
        noteid = request.form.get('noteid')
        print(noteid)
        note = Note.query.get(noteid)
        if note:
            if note.user_id == current_user.id:
                flash(f'Nota "{note.data}" removida com sucesso!', category='success')
                db.session.delete(note)
                db.session.commit()
            
    return redirect(url_for("views.home"))