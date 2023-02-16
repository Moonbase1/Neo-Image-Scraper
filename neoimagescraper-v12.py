import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from tqdm import tqdm

# check for required libraries and install if necessary
try:
    import requests
    from bs4 import BeautifulSoup
    from tqdm import tqdm
except ImportError as e:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "beautifulsoup4", "tqdm"])
    import requests
    from bs4 import BeautifulSoup
    from tqdm import tqdm

logo = """
     __                  _____                             
  /\ \ \___  ___         \_   \_ __ ___   __ _  __ _  ___  
 /  \/ / _ \/ _ \ _____   / /\/ '_ ` _ \ / _` |/ _` |/ _ \ 
/ /\  /  __/ (_) |_____/\/ /_ | | | | | | (_| | (_| |  __/ 
\_\ \/ \___|\___/      \____/ |_| |_| |_|\__,_|\__, |\___| 
                                               |___/       
 __                                                        
/ _\ ___ _ __ __ _ _ __   ___ _ __                         
\ \ / __| '__/ _` | '_ \ / _ \ '__|                        
_\ \ (__| | | (_| | |_) |  __/ |                           
\__/\___|_|  \__,_| .__/ \___|_|                           
                  |_|                                      
-By NeoRobo

How to Use: Enter a website directory and it saves each image that is linked. It does not scrape for images on the page itself.

"""

while True:
    print(logo)

    # prompt for the URL and output directory
    url = input('Enter URL of directory: ')
    output_dir = input('Enter image output directory: ')

    # create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # make request to the URL directory
    response = requests.get(url)

    # parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # find all image links with extensions .jpg, .jpeg, .png, .gif
    image_urls = [urljoin(url, node['href']) for node in soup.find_all('a') if node.has_attr('href') and node['href'].lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]

    # get the folder name from the output directory
    foldername = os.path.basename(output_dir)

    # download each image and write the HTML embed tags to a text file
    embed_tags = ""
    with open(os.path.join(os.getcwd(), f'{foldername}.html'), 'w') as f:
        with tqdm(total=len(image_urls), desc='Downloading images') as pbar:
            for url in image_urls:
                try:
                    response = requests.get(url)
                    filename = os.path.basename(url)
                    filepath = os.path.join(output_dir, filename)
                    with open(filepath, 'wb') as img_file:
                        img_file.write(response.content)
                    embed_tags += f'<img src="{foldername}/{filename}">\n'
                    pbar.set_postfix_str(f'Downloading {filename}')
                    pbar.update(1)
                except KeyboardInterrupt:
                    print('\nDownload interrupted.')
                    break

    # replace PLACEHOLDER and CODE placeholders
    template = ""
    with open("template.html") as t:
        template = t.read()

    with open('pictures.html', 'r') as f:
        html = f.read()

    index = html.find('<!-- LIST -->')
    if index == -1:
        print('Cannot find <!-- LIST --> in pictures.html. Please add it manually.')
    else:
        # parse the HTML content of pictures.html
        soup = BeautifulSoup(html, 'html.parser')

        # create a new anchor tag for the folder and insert it in the correct alphabetical order
        new_link = soup.new_tag('a', href=f'{foldername}.html')
        new_link.string = foldername

        # get all the existing anchor tags under the "LIST" section
        list_tags = soup.select('div#LIST a')

        # find the index where the new link should be inserted based on alphabetical order
        insert_index = len(list_tags)
        for i, tag in enumerate(list_tags):
            if foldername < tag.string:
                insert_index = i
                break

        # insert the new anchor tag in the correct alphabetical order
        soup.select('div#LIST')[0].insert(insert_index, new_link)

        # update pictures.html with the modified HTML content
        updated_html = str(soup)
        with open('pictures.html', 'w') as f:
            f.write(updated_html)

        # replace PLACEHOLDER and CODE placeholders in the template with the new values
        template = template.replace("PLACEHOLDER", foldername).replace("CODE", embed_tags)

        # write the final HTML file
        with open(f'{foldername}.html', 'w') as f:
            f.write(template)

    # print completion message
    print(f'Done! Images saved in {output_dir} and HTML file saved in {os.getcwd()}.')
    print(f'Link to {foldername}.html added to pictures.html.')
    print('')

    # prompt to continue or exit
    try:
        choice = input('Press ENTER to download another directory or type "q" to quit: ')
        if choice.lower() == 'q':
            break
    except KeyboardInterrupt:
        print('\nExiting program.')
        break
