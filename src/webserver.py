import flask
from threading import Thread
from multiprocessing import Queue
class webserver:
    def __init__(self, safe_control, server_stats):
        self.safe_control = safe_control
        self.flask_app = flask.Flask("Room Led Webserver", root_path="web_files")
        self.flask_app.add_url_rule("/","page_index",self.page_index)
        self.flask_app.add_url_rule("/api/<path:api_path>","api_handle",self.api_handle)
        self.flask_app.add_url_rule("/css/<path:file>","css_handle",self.css_handle)
        self.flask_app.add_url_rule("/javascript/<path:file>","javascript_handle",self.javascript_handle)

        self.get_server_stats = server_stats

        self.thread = Thread(target=self.flask_app.run, kwargs={"host":"0.0.0.0","port":80})
        self.thread.start()
    
    def _get_flask_response_object(self,content="",content_type="",status=500):
        return flask.Response(response=content,mimetype=content_type,headers={"content-type":"text/html"},status=200)
    
    def javascript_handle(self, file):
        return flask.send_file("javascript/%s"%(file))

    def css_handle(self, file):
        return flask.send_file("css/%s"%(file))

    def page_index(self):
        return flask.send_file("main.html")

    def api_handle(self, api_path):
        split_path = api_path.split("/")

        if(split_path[0] == "set_brightness"):
            try:
                self.safe_control.set_brightness(float(split_path[1]))
                return self._get_flask_response_object(status=200)
            except ValueError:
                return self._get_flask_response_object(status=400)
            except:
                return self._get_flask_response_object(status=500)
        
        #check if its power, if it is then make sure its valid, else return a status; 400 - bad request
        if(split_path[0] == "power"):
            split_path[1] = int(split_path[1])
            if(split_path[1] == 1):
                self.safe_control.turn_on()
                return self._get_flask_response_object(status=200)
            elif(split_path[1] == 0):
                self.safe_control.turn_off()
                return self._get_flask_response_object(status=200)
            else:
                return self._get_flask_response_object(status=400)
        
        if(split_path[0] == "server_stats"):
            return flask.jsonify(self.get_server_stats())