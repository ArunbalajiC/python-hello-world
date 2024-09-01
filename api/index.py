from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
from duckduckgo_search import DDGS

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Parse the query string to get the search term
        query_components = parse_qs(urlparse(self.path).query)
        search_term = query_components.get('q', None)
        
        if search_term:
            search_term = search_term[0]  # Get the first value if multiple are provided
            images = DDGS().images(search_term, max_results=10)
            image_url = None
            
            # Iterate through the images to find a valid one
            for image_data in images:
                image_url = image_data['image']
                try:
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        # Load the image and display it using matplotlib
                        img = Image.open(BytesIO(response.content))
                        plt.imshow(img)
                        plt.axis('off')
                        plt.show()
                        break
                except Exception as e:
                    print(f"Error checking image link: {image_url} - {e}")
                    continue

            if image_url:
                self.send_response(200)
                self.send_header('Content-type','text/plain')
                self.end_headers()
                self.wfile.write(f"Displayed image for search term: {search_term}".encode('utf-8'))
            else:
                self.send_response(404)
                self.send_header('Content-type','text/plain')
                self.end_headers()
                self.wfile.write(f"No valid images found for search term: {search_term}".encode('utf-8'))
        else:
            self.send_response(400)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write('Please provide a search term using the "q" query parameter.'.encode('utf-8'))

# To run the server:
def run(server_class=HTTPServer, handler_class=handler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
