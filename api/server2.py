import tornado.httpserver, tornado.ioloop, tornado.options, tornado.web, os.path, random, string

from cluster import *
import time

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/upload", UploadFile),
            (r"/cluster",MyFileHandler,{'path':'output.zip'})
        ]
        tornado.web.Application.__init__(self, handlers)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("webpage.html")

class MyFileHandler(tornado.web.StaticFileHandler):
    def initialize(self, path):
        self.dirname, self.filename = os.path.split(path)
        super(MyFileHandler, self).initialize(self.dirname)

    def get(self, path=None, include_body=True):
        # Ignore 'path'.
        super(MyFileHandler, self).get(self.filename, include_body)


class UploadFile(tornado.web.RequestHandler):
  # handle a post request
  def post(self):
    files = []
    # check whether the request contains files that should get uploaded
    try:
      files = self.request.files['files']
    except:
      pass
    # for each file that should get uploaded
    for xfile in files:
      # get the default file name
      file = xfile['filename']
      index = file.rfind(".")
      filename = file[:index].replace(".", "") + str(time.time()).replace(".", "") + file[index:]
      filename = filename.replace("/", "")
      with open("uploads/%s" % (filename), "wb") as out:
        out.write(xfile['body'])
    main()
    self.redirect('/cluster')
    # self.finish("All files written, Download will begin shortly")

settings = {
'template_path': 'templates',
'static_path': 'templates/creators/',
"xsrf_cookies": False

}
application = tornado.web.Application([
   (r"/", IndexHandler),
            (r"/upload", UploadFile),
    (r"/cluster", MyFileHandler, {'path': 'output.zip'})
        ], debug=True,**settings)
print ("Server started.")

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()