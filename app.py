from flask import Flask, render_template, jsonify, abort, request
import json

with open('data.json') as file:
    tasks = json.load(file)

def save():
    with open('data.json', 'w') as file:
        json.dump(tasks, file)


persona = {'name' : 'Carlos', 'mat' : '193305'}

app = Flask(__name__)
uri = '/api/tasks'

@app.route("/")

def helow():
    return "Hola"

# API

@app.route(uri , methods = {'GET'})

def get_tasks():
    return jsonify({'tasks' : tasks})

@app.route(uri + '/<int:id>', methods = {'GET'})

def get_task(id):
    for task in tasks:
        if task['id'] == id:
            return jsonify({'task' : task})
    abort(404)

@app.route(uri, methods = {'POST'})

def create_task():
    if request.json:
        task = {
            'id' : len(tasks) + 1,
            'name' : request.json['name'],
            'status' : False
        }
        tasks.append(task)
        save()
        return jsonify({'tasks' : tasks}), 201
    else:
        abort(404)

@app.route(uri + '/<int:id>', methods = {'PUT'})

def update_task(id):
    if request.json:
        this_task = [task for task in tasks if task['id'] == id]
        if this_task:

            if request.json.get('name'):
                this_task[0]['name'] = request.json['name']
            
            if request.json.get('status'):
                this_task[0]['status'] = request.json['status']
            save()
            return jsonify({'task' : this_task}), 201
        else:
            abort(404)
    else:
        abort(404)

@app.route(uri + '/<int:id>', methods = {'DELETE'})
def delete_task(id):
    this_task = [task for task in tasks if task['id'] == id]
    if this_task:
        tasks.remove(this_task[0])
        save()
        return jsonify({'tasks' : tasks})
    else:
        abort(404)



if __name__ == '__main__':
    app.run(debug = True)

