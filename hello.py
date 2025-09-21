from flask import Flask, render_template
from datetime import datetime
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from flask import session, flash, redirect, url_for

try:
    from wtforms.fields import EmailField          # WTForms 3.x
except ImportError:
    from wtforms.fields.html5 import EmailField    # WTForms 2.x

# ensure bootstrap is installed
try:
    from flask_bootstrap import Bootstrap
except ImportError:
    Bootstrap = None

app = Flask(__name__)

# wtf
app.config['SECRET_KEY'] = 'hard to guess string'

# form input
class NameEmailForm(FlaskForm):
    name  = StringField('What is your name?', validators=[DataRequired()])
    email = EmailField('What is your UofT Email address?', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')


# init ext
moment = Moment(app)
if Bootstrap:
    bootstrap = Bootstrap(app)

# main /index share same vision，and pass in current_time
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    name = email = is_uoft = None
    form = NameEmailForm()
    if form.validate_on_submit():
        name = (form.name.data or '').strip()
        email = (form.email.data or '').strip()
        is_uoft = 'utoronto' in email.lower()

        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        old_email = session.get('email')
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')
        session['name']   = name
        session['email']  = email
        session['is_uoft'] = is_uoft
        return redirect(url_for('index'))

    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'), is_uoft=session.get('is_uoft'), current_time=datetime.utcnow())

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
