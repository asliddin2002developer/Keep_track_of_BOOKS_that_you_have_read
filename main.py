from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

# Flask APP - Bootstrap - SQLAlchemy Code Config
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
db = SQLAlchemy(app)


#### Create Book Form Class from FlaskForm ####
class BookForm(FlaskForm):
    book_name = StringField(u'Book Name:', validators=[DataRequired()])
    book_author = StringField(u'Book Author: ', validators=[DataRequired()])
    book_rating = StringField(u'Book Rating: ', validators=[DataRequired()])
    submit = SubmitField(u'Submit')


class EditForm(FlaskForm):
    new_rating = StringField(u'New Rating: ', validators=[DataRequired()])
    submit = SubmitField(u'Submit')


class Books(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    author = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Float, nullable=False)

db.create_all()


@app.route('/')
def home():

    all_books = Books.query.all()

    return render_template('index.html', books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    ### Creates form from the class we created above ###
    form = BookForm()
    if form.validate_on_submit() and request.method == "POST":
        add_book = Books(name=form.book_name.data, author=form.book_author.data,
                         rating=form.book_rating.data)
        db.session.add(add_book)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('add.html', form=form)


@app.route("/edit", methods=['GET', 'POST'])
def edit_rating():
    # New Edit-Form To Use To Update Rating
    edit_form = EditForm()
    if edit_form.validate_on_submit() and request.method == "POST":
        book_id = request.args.get('id')
        query_to_update = Books.query.get(book_id)
        query_to_update.rating = edit_form.new_rating.data
        db.session.commit()
        print(query_to_update.rating)

        return redirect(url_for('home'))

    # Retrieves the ID from DB with all its values
    book_id = request.args.get('id')
    book_query = Books.query.get(book_id)
    print(book_query)
    return render_template('edit_rating.html', form=edit_form, book=book_query)


@app.route('/delete', methods=['GET', 'POST'])
def delete_entry():
    book_id = request.args.get('id')
    query_to_delete = Books.query.get(book_id)
    db.session.delete(query_to_delete)
    db.session.commit()

    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
