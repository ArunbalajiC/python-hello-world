from http.server import BaseHTTPRequestHandler, HTTPServer
from duckduckgo_search import DDGS
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import os

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Get the input from the URL query string
        query = self.path.split('?q=')[1] if '?q=' in self.path else ''

        if query:
            try:
                # Search for images using DuckDuckGo
                images = DDGS().images(query, max_results=10)

                # Iterate through the images
                for image_data in images:
                    image_url = image_data['image']
                    try:
                        response = requests.get(image_url)
                        if response.status_code == 200:
                            img = Image.open(BytesIO(response.content))
                            plt.imshow(img)
                            plt.axis('off')
                            plt.savefig('image.png')
                            plt.close()  # Close the plot to avoid display issues
                            
                            # Return the image in the HTML response
                            self.wfile.write(f"<html><body><h1>Search Results for '{query}'</h1>".encode('utf-8'))
                            self.wfile.write(f"<img src='file://{os.path.abspath('image.png')}' alt='Image'><br>".encode('utf-8'))
                            self.wfile.write(b"</body></html>")
                            break
                        else:
                            continue
                    except Exception as e:
                        print(f"Error checking image link: {image_url} - {e}")
            except Exception as e:
                self.wfile.write(f"<html><body><h1>Error: {e}</h1></body></html>".encode('utf-8'))
        else:
            self.wfile.write(b"<html><body><h1>Please provide a search query in the URL (e.g., ?q=cats)</h1></body></html>")

def run(server_class=HTTPServer, handler_class=Handler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
