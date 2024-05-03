import motor.motor_asyncio
import tornado
from tornado.web import Application, RequestHandler
import json
from bson import ObjectId

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017/")
db = client["flat"]
collection = db["toilet"]

class CreateDocumentHandler(RequestHandler):
    def set_default_headers(self) -> None:
        super().set_default_headers()
        # Set CORS headers
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "POST")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
    
    async def get(self, second_parameter_local_j_pani=None):
        if second_parameter_local_j_pani is None:
            documents = []
            
            async for document in collection.find({}):
                    documents.append({
                        "id": str(document["_id"]),
                        "name": document.get("name"),
                        "tape": document.get("tap")
                    })
            self.write(json.dumps(documents))

        else:
            # if collection.find({"name":second_parameter_local_j_pani}) is "[]":
            #             self.set_status(404)
            #             # self.write({"message": "Document not found"})
            #             self.write(json.dumps({"message": "Document not found"}))
                
            if collection.find({"name":second_parameter_local_j_pani}) is not None:
                async for document in collection.find({"name":second_parameter_local_j_pani}):
                    if document:    
                        thatrow = ({
                            "id": str(document["_id"]),
                            "name": document.get("name"),
                            "tape": document.get("tap")
                        })
                        self.write(json.dumps(thatrow))
           

    async def post(self, second):
        argkunai = self.get_argument("arg_key"); 
         
        document_id = ObjectId()  # Generate a unique ObjectId
        document = {"_id": document_id, "name": second, "tap": argkunai}
        result = await collection.insert_one(document)
        self.write({"message": "Document created successfully", "id": str(result.inserted_id)})


async def get_mongo_collection():
    return collection

if __name__ == "__main__":
    app = Application([
        (r"/create/([^/]+)", CreateDocumentHandler),
        (r"/create", CreateDocumentHandler)
        ]) 
    port = 8882
    app.listen(port)
    print("listening in {}".format(port))
    tornado.ioloop.IOLoop.current().start()
