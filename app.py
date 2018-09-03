from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base
from flask_cors import CORS


Base = declarative_base()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/bible-sqlite.db'

db = SQLAlchemy(app)


class Key(db.Model):
    __tablename__ = 'key_english'
    __table_args__ = {'extend_existing': True}
    b = db.Column(db.Integer, primary_key=True)
    n = db.Column(db.String(80), unique=False, nullable=True)
    c_number = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Book %r>' % self.n

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


def Passage(table):
    class PassageClass(db.Model):
        __tablename__ = table
        __table_args__ = {'extend_existing': True}
        id = db.Column(db.Integer, primary_key=True)
        b = db.Column(db.Integer, unique=False, nullable=True)
        c = db.Column(db.Integer, unique=False, nullable=True)
        v = db.Column(db.Integer, unique=False, nullable=True)
        t = db.Column(db.Text, unique=False, nullable=True)

        def __repr__(self):
            return '<Version %r>' % self.abbreviation

        def toDict(self):
            return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    return PassageClass()


class Version(db.Model):
    __tablename__ = 'bible_version_key'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    table = db.Column(db.String(80), unique=False, nullable=True)
    abbreviation = db.Column(db.String(4), unique=False, nullable=True)
    language = db.Column(db.String(10), unique=False, nullable=True)
    version = db.Column(db.String(80), unique=False, nullable=True)
    info_text = db.Column(db.String(120), unique=False, nullable=True)
    info_url = db.Column(db.String(80), unique=False, nullable=True)
    publisher = db.Column(db.String(80), unique=False, nullable=True)
    copyright = db.Column(db.String(80), unique=False, nullable=True)
    copyright_info = db.Column(db.String(200), unique=False, nullable=True)

    def __repr__(self):
        return '<Version %r>' % self.abbreviation

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/')
def index():
    return jsonify(message="Hello, world!")


# http://localhost:5000/read?from=1001001&to=1001009
# http://localhost:5000/read?book=1&chapter=1&verse=1
@app.route('/read')
def read():
    ref_from = request.args.get('from')
    ref_to = request.args.get('to')
    data = []

    if ref_from and ref_to:
        results = db.engine.execute(f"SELECT * FROM t_kjv WHERE id BETWEEN {int(ref_from)} AND {int(ref_to)}")
        for row in results:
            data.append({
                "id": row[0],
                "b": row[1],
                "c": row[2],
                "v": row[3],
                "t": row[4]
            })
    else:
        book = request.args.get('book')
        chapter = request.args.get('chapter')
        data = [ver.toDict() for ver in Passage('t_kjv').query.filter_by(c=chapter, b=book).all()]

    return jsonify(data)


@app.route('/versions')
def versions():
    data = [ver.toDict() for ver in Version.query.all()]
    return jsonify(data)


@app.route('/books')
def books():
    data = [book.toDict() for book in Key.query.all()]
    return jsonify(data)


# if __name__ == "__main__":
#     app.run(debug=False, host='0.0.0.0', port=8080)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
