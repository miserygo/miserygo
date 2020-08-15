# import datetime
# print(datetime.datetime.now())
# print(datetime.timedelta(seconds=10)
# )
# import logging
# logger = logging.getLogger(__name__)
# logger.info('123')
# import uuid
# uid = str(uuid.uuid4())
# print(uid)

from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

todos = {}

class TodoSimple(Resource):
    def get(self, todo_id):
        print(todo_id,"**************")
        return {todo_id: todos.get(todo_id)}

    def put(self, todo_id):
        todos[todo_id] = request.json['data']
        return {todo_id: todos[todo_id]}

api.add_resource(TodoSimple, '/<string:todo_id>')


if __name__ == '__main__':
    app.run(debug=True)