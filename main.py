
import requests
from bs4 import BeautifulSoup
import os
# URL of the webpage
url = 'https://efukt.com/'
DOWNLOADFOLDER ="downloads"

# Function to down load video from URL
def download_video(url, filename):
    # Send a GET request to the video URL
    video_response = requests.get(url, stream=True)

    # Check if the request was successful
    if video_response.status_code == 200:
        # Open a file in binary write mode to save the video
        with open(os.path.join(DOWNLOADFOLDER,filename), 'wb') as video_file:
            # Write the video content to the file in chunks
            for chunk in video_response.iter_content(1024):
                video_file.write(chunk)
        print(f"Video downloaded successfully: {filename}")
    else:
        print(f"Failed to download video from URL: {url}")

# Function to sanitize filename for Windows
def sanitize_filename(filename):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def check_download_folder():
    """ checks download folder exists if not creates it"""
    if not os.path.exists(DOWNLOADFOLDER):
        os.mkdir(DOWNLOADFOLDER)


if __name__ == "__main__":
    check_download_folder()
    # Send a GET request to the webpage
    response = requests.get(url)
    # List to store tuples of (title, url)
    title_url_tuples = []
    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all divs with class="col"
    col_divs = soup.find_all('div', class_='col')


    # Iterate over each div with class="col"
    for col_div in col_divs:
        # Find all divs with class="tile" inside the current col_div
        tile_divs = col_div.find_all('div', class_='tile')

        # Iterate over each div with class="tile" inside the current col_div
        for tile_div in tile_divs:
            # Find all divs with class="meta" inside the current tile_div
            meta_divs = tile_div.find_all('div', class_='meta')

            # Iterate over each meta_div
            for meta_div in meta_divs:
                # Find the <a> tag within the meta_div
                a_tag = meta_div.find('a')
                # Extract the href attribute value from the <a> tag
                href = a_tag['href']
                # Extract the text within the <a> tag
                title = a_tag.text.strip()
                # Create a tuple of (title, url) and append it to the list
                title_url_tuples.append((title, href))


    for title, url in title_url_tuples:
        # Send a GET request to the URL of the current tuple
        response = requests.get(url)

        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the <source> tag with type="video/mp4"
        video_source = soup.find('source', type='video/mp4')

        # Check if video_source is found
        if video_source:
            # Get the src attribute value of the <source> tag
            video_url = video_source['src']

            # Sanitize the filename
            sanitized_title = sanitize_filename(title)
            # Create a filename for the video
            filename = f"{sanitized_title}.mp4"

            # Download the video
            download_video(video_url, filename)
        else:
            print(f"No video source found for title: {title}")