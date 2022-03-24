from tkinter import *
import sqlite3

root = Tk()
root.title('Todo List')
root.geometry('500x500')

conn = sqlite3.connect('todo.db')

c = conn.cursor()

c.execute('''
      CREATE TABLE if not exists todo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        description TEXT NOT NULL,
        completed BOOLEAN NOT NULL
      );
''')

conn.commit()

# FUNCIONES
def remove(id):
    def _remove():
        c.execute('DELETE FROM todo WHERE id = ?', (id, ))
        conn.commit()
        render_todos()
    return _remove

def complete(id): # Currying!
    def _complete():
        todo = c.execute('SELECT * FROM todo WHERE id = ?', (id, )).fetchone()
        c.execute('UPDATE todo SET completed = ? WHERE id = ?', (not todo[3], id))
        conn.commit()
        render_todos()
    return _complete

def render_todos():
    rows = c.execute('SELECT * FROM todo').fetchall()

    for widget in frame.winfo_children():
        widget.destroy()
    for i in range(0, len(rows)):
        id = rows[i][0]
        completed = rows[i][3]
        description = rows[i][2]
        color = '#666666' if completed else '#000000'
        l = Checkbutton(frame, text = description, fg = color, width = 53, anchor = 'w', command = complete(id))
        l.grid(row = i, column = 0, sticky = 'w')
        b = Button(frame, text = 'Eliminar', command = remove(id))
        b.grid(row = i, column = 1)
        l.select() if completed else l.deselect()

def add_todo():
    todo = e.get()
    if todo:
        c.execute('''
              INSERT INTO todo (description, completed) VALUES (?, ?)
        ''', (todo, False))
        conn.commit()
        e.delete(0, END)
        render_todos()
    else:
        pass

# ELEMENTOS DE INTERFAZ

l = Label(root, text = 'Tarea')
l.grid(row = 0, column = 0)

e = Entry(root, width = 40)
e.grid(row = 0, column = 1)

btn = Button(root, text = 'Agregar', command = add_todo)
btn.grid(row = 0, column = 2)

frame = LabelFrame(root, text = 'Mis tareas', padx = 5, pady = 5)
frame.grid(row = 1, column = 0, columnspan = 3, sticky = 'nswe', padx = 5)

e.focus()

root.bind('<Return>', lambda x: add_todo())

render_todos()

root.mainloop()
