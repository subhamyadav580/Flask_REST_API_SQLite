from flask import Flask,request
from flask_restful import Api,Resource,reqparse
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
api = Api(app)





def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#function creating connection with database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

#function to create table
def create_table(conn,create_table_sqlite):
    try:
        c = conn.cursor()
        c.execute(create_table_sqlite)  
    except Error as e:
        print(e)

#function inserting rows into table
def create_rows(conn,task):
    # conn.row_factory = dict_factory
    print(task)
    sql = ''' INSERT INTO books(id,published,author,title,first_sentence) VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql,task)
    print("helllo")
    return cur.lastrowid



#function select all rows from the table and display them
def select_all_tasks(conn):
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute('SELECT * FROM books')
    rows = cur.fetchall()
    # for rows in rows:
    #     print(rows)
    print(rows)
    return rows

#function query task by priority
def select_task_by_priority(conn,priority):
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute("SELECT * FROM books WHERE published=?",(priority,))
    rows = cur.fetchall()
    for rows in rows:
        print(rows)
    return rows

#function update a specific task
def update_task(conn,task):
    sql = '''UPDATE books SET priority = ? , begin_date = ? , end_date = ? WHERE ID = ? '''
    cur = conn.cursor()
    cur.execute(sql,task)
    conn.commit()

#function deletes a task 
def delete_task(conn,task):
    sql = 'DELETE FROM books WHERE published = ?'
    cur = conn.cursor()
    cur.execute(sql,(task,))
    conn.commit()

#delete all rows in the table
def delete_all_task(conn):
    sql = 'DELETE FROM books'
    cur = conn.cursor()
    cur.execute(sql)
    cur.commit() 


parser = reqparse.RequestParser()
parser.add_argument('')


class Todo(Resource):
    def get(self,task):
        conn = create_connection('books.db')
        rows = select_task_by_priority(conn,task)
        return rows
    def delete(self,task):
        conn = create_connection('books.db')
        rows = select_task_by_priority(conn,task)
        delete_task(conn,task)
        return rows,204
    def post(self):
        pass

class TodoList(Resource):
    def get(self):
        conn = create_connection('books.db')
        rows = select_all_tasks(conn)
        return rows
    def post(self):
        conn = create_connection('books.db')
        task = ('null',2014,'Shubham Yadav','Biodata','Hello myself shubham')
        rows = create_rows(conn,task)
        return rows
api.add_resource(Todo,'/<int:task>')
api.add_resource(TodoList,'/')
if __name__ == "__main__":
    app.run(debug=True)
        



