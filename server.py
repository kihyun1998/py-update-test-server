from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import json

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)

    def do_GET(self):
        if self.path == '/update/updatefilename':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            update_folder = 'update'
            files = os.listdir(update_folder)
            zip_files = [f for f in files if f.endswith('.zip')]
            if zip_files:
                latest_file = max(zip_files, key=lambda f: os.path.getmtime(os.path.join(update_folder, f)))
                self.wfile.write(json.dumps({"filename": latest_file}).encode())
            else:
                self.wfile.write(json.dumps({"error": "No update file found"}).encode())
        else:
            super().do_GET()

def run(server_class=HTTPServer, handler_class=CORSRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Serving on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    run()