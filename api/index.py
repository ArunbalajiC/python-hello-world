def do_GET(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

    # Get the input from the URL query string
    query = self.path.split('?q=')[1] if '?q=' in self.path else ''

    if query:
        try:
            # Install and import the required libraries
            !pip install -U -q duckduckgo_search
            from duckduckgo_search import DDGS
            from duckduckgo_search import AsyncDDGS
            import requests
            from PIL import Image
            from io import BytesIO
            import matplotlib.pyplot as plt

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
                        self.wfile.write(f"<img src='file:///{os.path.abspath('image.png')}'>".encode('utf-8'))
                        break
                    else:
                        continue
                except Exception as e:
                    print(f"Error checking image link: {image_url} - {e}")
        except Exception as e:
            self.wfile.write(f"Error: {e}".encode('utf-8'))
    else:
        self.wfile.write(b"Please provide a search query in the URL (e.g., ?q=cats)")

    return
