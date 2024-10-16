import http.server
import socketserver
import io
import urllib.parse
from GPT import GPT
import time
import json

gpt = GPT(api_key="sk-6JIeIbQP1Jn5bFWSZuqKVnoFzjf095cWT76eYObD75fJ4q3f")
# type = 'judgement' or 'multiple' or 'single'
class HTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        info = self.parse_path(self.path)
        ans = gpt.get_anwser(info)
        print(ans)
        response = {
                    "code": 1,
                    "data":
                        {"question": "",
                        "answer": ""}
                    }
        response["data"]["question"] = info["title"]
        response["data"]["answer"] = ans
        response = json.dumps(response).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-Length', str(len(response)))
        # self.send_header("{", "}")
        self.end_headers()
        self.wfile.write(response)
        return super().do_GET()
    
    def parse_path(self, path):
        query_string = path.split('?', 1)[1] if '?' in path else ''
        query_string = query_string.split('&')
        decoded_params = [urllib.parse.unquote(p).split('=') for p in query_string]
        info = dict(decoded_params)
        return info

class HTTPServer(socketserver.TCPServer):
    def __init__(self, port):
        super().__init__(("", port), HTTPRequestHandler)

def run_server(port):
    with HTTPServer(port) as httpd:
        print(f"Serving on port {port}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server(5000)
