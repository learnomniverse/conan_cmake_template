import http.server
import socketserver

PORT = 8000
# files_to_serve = {
#     "kit-sdk@105.1.0+release.51.a7407fb5.tc.linux-x86_64.release.7z",
#     "nv-usd@22.11.nv.0.2.1195.84b2e524-linux64_py310-centos_release-releases-105-1.7z"
# }

Handler = http.server.SimpleHTTPRequestHandler


class CustomHandler(Handler):
    def do_GET(self):
        # # drop the leading '/' in '/filename.7z' before comparing
        # if self.path[1:] in files_to_serve:
        #     print(f"-> requested file {self.path[1:]}, serving..")
        #     self.send_response(200)
        #     self.send_header('Content-type', 'application/x-7z-compressed')
        #     self.end_headers()

        #     with open(self.path[1:], 'rb') as file:
        #         self.wfile.write(file.read())
        #     print("-> DONE")
        # else:
        #     print("unhandled GET request")
        print(f"Responding to GET for {self.path}")
        super().do_GET()


with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
