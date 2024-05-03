import tornado.web
import tornado.ioloop
import motor.motor_tornado
from bson.objectid import ObjectId

# MongoDB connection setup
mongo_client = motor.motor_tornado.MotorClient('mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false')
mongo_db = mongo_client['your_database_name']
mongo_collection = mongo_db['student_data']

class GetHandler(tornado.web.RequestHandler):
    async def get(self, id):
        try:
            document = await mongo_collection.find_one({'_id': ObjectId(id)})
            if document:
                self.write(document)
            else:
                self.set_status(404)
                self.write({"error": "Document not found"})
        except Exception as e:
            self.set_status(500)
            self.write({"error": str(e)})

class PostHandler(tornado.web.RequestHandler):
    async def post(self):
        try:
            data = self.request.body_arguments
            result = await mongo_collection.insert_one(data)
            self.write({"id": str(result.inserted_id)})
        except Exception as e:
            self.set_status(500)
            self.write({"error": str(e)})

class UpdateHandler(tornado.web.RequestHandler):
    async def put(self, id):
        try:
            data = self.request.body_arguments
            await mongo_collection.update_one({'_id': ObjectId(id)}, {'$set': data})
            self.write({"message": "Document updated successfully"})
        except Exception as e:
            self.set_status(500)
            self.write({"error": str(e)})

class DeleteHandler(tornado.web.RequestHandler):
    async def delete(self, id):
        try:
            result = await mongo_collection.delete_one({'_id': ObjectId(id)})
            if result.deleted_count:
                self.write({"message": "Document deleted successfully"})
            else:
                self.set_status(404)
                self.write({"error": "Document not found"})
        except Exception as e:
            self.set_status(500)
            self.write({"error": str(e)})

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/student/([^/]+)", GetHandler),
            (r"/student", PostHandler),
            (r"/student/([^/]+)", UpdateHandler),
            (r"/student/([^/]+)", DeleteHandler),
        ]
        super().__init__(handlers)

if __name__ == "__main__":
    app = Application()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
