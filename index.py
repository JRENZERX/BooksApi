import sqlite3
from flask import *
import flask
from datetime import datetime
app = Flask(__name__)
# routes


@app.route('/delAll', methods=['GET', 'DELETE', 'POST'])
def delAll():
    with sqlite3.connect('./db/db.sqlite3') as db:
        cur = db.cursor()
        cur.execute('DELETE FROM Books')
        return redirect('/')


@app.route('/del', methods=['DELETE'])
@app.route('/del/<id>', methods=['GET', 'DELETE'])
def delete(id=0):
    with sqlite3.connect('./db/db.sqlite3') as db:
        finalizer = 'remember, for deleting with api, use the id form value and for deleting with URL, pass the id /del/:id <---- here'
        cur = db.cursor()
        if(request.method == 'DELETE' and id == 0):
            try:
                cur.execute('DELETE FROM Books WHERE bid = ?',
                            (request.form['id'],))
            except:
                # print(request.json) >> {'bid': '<bid>'}
                cur.execute('DELETE FROM Books WHERE bid = ?',
                            (request.json["bid"],))
            finalizer += ' 200 STATUS: ok. It was done'
        else:
            cur.execute('DELETE FROM Books WHERE bid = ?', (id,))
            finalizer += ' 200 STATUS: ok. It was done'
        db.commit()
        return finalizer


@app.route('/updateBook', methods=['GET'])
@app.route('/updateBook/<id>', methods=['PUT'])
@app.route('/updateBook/<id>/<column>', methods=['PATCH'])
def updateBook(id=0, column='title'):
    with sqlite3.connect('./db/db.sqlite3') as db:
        cur = db.cursor()
        # GET(docs)
        if request.method == 'GET':
            return f"""
      <h1>Update Book</h1>
      <p>if u are here, its because you wanna know how to update a book OR you were trying to find routes <hr>for updating a book completely, do PUT /updateBook/:id with the WHOLE book info in Form enctype<hr/>and for updating only one column, do PATCH /updateBook/:id/:column (which can be title, author or description) and a body of the value with the key 'value' for the column with any Form enctype.

      """
        # PUT
        if request.method == 'PUT':
            cur.execute('UPDATE Books set author = ?, title = ?, description = ? where bid = ?',
                        (request.form['author'] or request.json['author'],
                         request.form['title'] or request.form['title'],
                         request.form['description'] or request.json['description'],
                         id,))
            return 'OK'
        # PATCH
        else:
            if (column == 'author' or column == 'title' or column == 'description'):
                if(request.form):
                    cValue = request.form['value']
                print(request.get_json())
                if(request.get_json().get('value')):
                    cValue = request.json['value']
                query = 'UPDATE Books set ? = ? WHERE bid = ?'
                # cur.execute(query, (column, cValue, id,))
                cur.execute('UPDATE Books set '+column +
                            ' = ? WHERE bid = ?', (cValue, id, ))
                db.commit()

                print('UPDATE Books set '+column+' = \'' +
                      cValue + '\' WHERE bid =' + id)
                db.commit()
                # return redirect('/allBooks')
                return 'ok'

            else:
                return redirect('/updateBook', 400)
            db.commit()


@app.route('/addBookJson', methods=['POST'])
def bookJson():
    with sqlite3.connect('./db/db.sqlite3') as db:
        cur = db.cursor()
        print(request.get_json())
        cur.execute('INSERT INTO Books (title, description, author) VALUES (?,?,?)',
                    (request.json['title'], request.json['description'], request.json['author'],))
        db.commit()
        return redirect('/allBooks')


@app.route('/addBook', methods=['POST', 'GET', 'PATCH'])
def addBook():
    with sqlite3.connect('./db/db.sqlite3') as db:
        cur = db.cursor()
        if request.method == 'POST':
            try:
                cur.execute('INSERT INTO Books (title, description, author) VALUES (?,?,?)',
                            (request.form['title'], request.form['description'], request.form['author'],))
                db.commit()
                return redirect('/allBooks')
            except KeyError:
                return 'You used didnt use the correct encoding(Example: JSON or GraphQL) or the correct data (title, description, author). Try using form'
        elif request.method == 'GET':
            return 'GET'
        else:
            return 'WTF'


@app.route('/first')
def first():
    with sqlite3.connect('./db/db.sqlite3') as db:
        cur = db.cursor()

        first = cur.execute('SELECT * FROM Books LIMIT 1').fetchall()[0]
        return jsonify(first)


@app.route('/allBooks/<isClear>', methods=['GET', 'POST', 'DELETE'])
@app.route('/allBooks', methods=['GET', 'POST', 'DELETE'])
def all(isClear=False):
    if isClear == "False":
        isClear = False
    with sqlite3.connect('./db/db.sqlite3') as db:
        cur = db.cursor()
        print(bool(isClear))
        all = cur.execute('SELECT * FROM Books').fetchall()

        if(isClear == 'false'):
            return jsonify(all, {"msg": "first book in /first"})
        elif(bool(isClear) or isClear or isClear == 'true'):
            return jsonify(all)
        else:
            return jsonify(all, {"msg": "first book in /first"})


@app.route('/', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def RedirFromMain():
    with sqlite3.connect("./db/db.sqlite3") as db:
        cur = db.cursor()
        print("someone connected: "+ str(datetime.now().time()))
        cur.execute("INSERT INTO Publicips VALUES (?)", (request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)+":"+str(datetime.now().time()),))
        return redirect('/allBooks')


@app.route('/one/<bid>')
def getById(bid):
    with sqlite3.connect('./db/db.sqlite3') as db:
        cur = db.cursor()
        getTheOne = cur.execute(
            'SELECT * FROM Books WHERE bid = ? ', (bid,)).fetchall()
        return jsonify(getTheOne)


@app.route('/all')
def RedirFromAll(): return redirect('/allBooks')


# routes end
if __name__ == '__main__':
    app.run(debug=True, port=5000)
