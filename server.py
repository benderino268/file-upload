#!-*- coding: utf-8 -*-
from tornado import gen
from tornado.httputil import parse_multipart_form_data
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url, stream_request_body, asynchronous, StaticFileHandler
from conf import FORM
import os


class Download(dict):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Download, cls).__new__(cls, args, kwargs)
            cls._instance = {'length': 0, 'writed': 0}
            return cls._instance


REG = Download()

class StatusHandler(RequestHandler):

    def get(self):
        print(REG)
        self.write("%s" % REG)
        #self.write('%s' % (REG['writed']*100/REG['length']))


@stream_request_body
class FormHandler(RequestHandler):
    tmp_buffer = bytes()

    def get(self):
        self.write(FORM)

    #@asynchronous
    @gen.coroutine
    def post(self):
        boundary = self.request.headers['Content-Type'].split('boundary=',1)[1]
        args = {}
        files = {}
        data = parse_multipart_form_data(boundary , self.tmp_buffer, args, files)
        f = open('uploads/%s' % files['to_upload'][0]['filename'], 'wb+')
        f.write(files['to_upload'][0]['body'])
        f.close()
        # curpos = 0
        # chunk = 1024
        # file = self.request.files['to_upload'][0]['body']
        # length = len(file)
        # REG['length'] = length
        # f = open(self.request.files['to_upload'][0]['filename'], 'wb+')
        # while curpos < length:
        #     part = file[curpos:min(curpos+chunk, length)]
        #     f.write(part)
        #     curpos += chunk
        #     REG['writed'] = curpos
        #
        # # DOWNLOAD['writed'] = 0

        self.write('Done!')
        self.finish()

    # @asynchronous
    # @gen.coroutine
    def prepare(self):
        #print dir(self.request.connection)
        self.request.connection.set_max_body_size(400*1024*1024)


    @gen.coroutine
    def data_received(self, chunk):
        self.tmp_buffer += chunk
        REG['writed'] = REG.get('writed', 0) + len(chunk)
        #yield REG
        #print REG
        #time.sleep(0.01)
        #DOWNLOAD['writed'] += len(chunk)
        #print len(chunk)

def make_app():
    return Application([
        url(r"/", FormHandler),
        url(r'/status/$', StatusHandler),
        url(r"/static/(.*)", StaticFileHandler,
            {"path": os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')}),])

app = make_app()
app.listen(8888)
IOLoop.current().start()

