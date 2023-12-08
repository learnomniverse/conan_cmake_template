import http.server
import socketserver

PORT = 8000
FILE_TO_SERVE = "kit-sdk@105.1.0+release.51.a7407fb5.tc.linux-x86_64.release.7z"

Handler = http.server.SimpleHTTPRequestHandler


class CustomHandler(Handler):
    def do_GET(self):
        if self.path == f'/{FILE_TO_SERVE}':
            self.send_response(200)
            self.send_header('Content-type', 'application/x-7z-compressed')
            self.end_headers()

            with open(FILE_TO_SERVE, 'rb') as file:
                self.wfile.write(file.read())
            print("Done serving GET!")
        else:
            super().do_GET()


with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
