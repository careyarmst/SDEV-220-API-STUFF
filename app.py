import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
db=SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(120), unique = True, nullable=False)
    author = db.Column(db.String(120), unique = True, nullable=False)
    publisher = db.Column(db.String(120), unique = True, nullable=False)

    def __repr__(self):
        return f"{self.book_name} - {self.author} - {self.publisher}"
    

@app.route('/')
def index():
    return 'Hello!'
@app.route('/books')
def get_books():
    books = Book.query.all()
    listofbooks = []
    for book in books:
        bookinfo = {'Name of book':book.book_name, 'Author':book.author, 'Publisher': book.publisher}
        listofbooks.append(bookinfo)

    return {"books": listofbooks}

@app.route('/books/<id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return {"Book name": book.book_name, "Author":book.author, "Publisher": book.publisher}

@app.route('/books', methods=['POST'])
def add_book():
    book = Book(book_name=request.json['book_name'], author=request.json['author'], publisher=request.json['publisher'])
    db.session.add(book)
    db.session.commit()
    return {"id": book.id}

@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return {"Oops":"that's not valid"}
    db.session.delete(book)
    db.session.commit
    return {"message":"Even though I'm old I like the word YEET!"}