import tornado.web
import tornado.ioloop

#another part
import json



class YourHandler(tornado.web.RequestHandler):
    async def get(self):
        try:
            # Example of querying MongoDB
            cursor = self.application.db.your_collection.find({})
            async for document in cursor:
                self.write(document)
        except Exception as e:
            self.set_status(500)
            self.write({"error": str(e)})


class basicRequestHandler(tornado.web.RequestHandler):
    def get(self):#method
        self.write("hello world from python backend")
 
class queryRenderHandler(tornado.web.RequestHandler):
     def get(self, something_for_arko_request=None,arkowala =None): # method
        if something_for_arko_request is None and arkowala is None:
            # Handling the /isEven?num=2 request
            attribute_ko_name = self.get_argument("num")
            if attribute_ko_name.isdigit():
                varlocal = "odd" if int(attribute_ko_name) % 2 else "even"
                self.write(f"{attribute_ko_name} is {varlocal}")
            else:
                self.write(f"{attribute_ko_name} is not a valid integer")
        elif something_for_arko_request is not None and arkowala is None:
            # Handling the /isEven/{req_param}?name=nirajan request
            attribute_ko_name = self.get_argument("name")
            if attribute_ko_name.isalpha():
                self.write(f"your name is {attribute_ko_name} and your third parameter is {arkowala}")
            else:
                self.write(f"{attribute_ko_name} is not a string")
        else :
              # Handling the /isEven/{req_param}/{arkowala}?name=123 request
            attribute_ko_name = self.get_argument("name")
            if attribute_ko_name.isalpha():
                self.write(f"your name is {attribute_ko_name} and your parameter is {arkowala}")
            else:
                self.write(f"{attribute_ko_name} is not a string")
                


#below process includes destructuring the parameter not argument(eg: parameter/?key=value)
#parameter doesnot contain ? symbol it is the arrangement of parameter and subparameters.
#we are not retriving the data from get_argument from the parameter.
#instead we are using the regex to match and map the parameter directly to the method function.
class resourceHandler(tornado.web.RequestHandler):
    def get(self, studentName,courseId):#method /oneparameter, two /kei_name
        
        self.write("welcome {}, The course id is {}".format(studentName, courseId))

    #url: localhost :8882 and, self: key 
    #self is the parameter after the url


class jsongetHandler(tornado.web.RequestHandler):
#header setting
    def set_default_headers(self):
        # Allow requests from all origins
        self.set_header("Access-Control-Allow-Origin", "*")
        # Allow GET requests with the Content-Type header
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")

#parameter setting
    def get(self):#method
        fh= open("list.txt","r")
        fruits = fh.read().splitlines()
        fh.close()
        self.write(json.dumps(fruits))

    def post(self):#method   
        fruitname = self.get_argument("fruit")#url/?fruit
        fh= open("list.txt","a")
        fh.write(f"{fruitname}\n")
        fh.close()
        self.write(json.dumps({"message":"fruit added successfully"}))




if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", basicRequestHandler),
        (r"/isEven", queryRenderHandler),
        (r"/isEven/([a-z]+)", queryRenderHandler),
        (r"/isEven/([a-z]+)/([A-Z]+)", queryRenderHandler),
        #key is the (a-z) is the parameter and (0-9) is the value that the parameter must contains
        (r"/students/([a-z]+)/([0-9]+)", resourceHandler),
        (r"/isEven/([a-z]+)/([a-z]+)", queryRenderHandler),
        (r"/fruitslist", jsongetHandler),#did it with accessing file.txt,

    ])


    port = 8882
    app.listen(port)
    print("listening in {}".format(port))
    tornado.ioloop.IOLoop.current().start()