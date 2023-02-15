# Neo-Image-Scraper

This script will require you to install beautifulsoup4, requessts and tqdm libaries. 
Enter a website directory and it saves each image that is linked. It does not scrape for images on the page itself. Then it generates a photo gallery of the images scraped, and a directory to all of the image galleries.

This tool is more for personal use but others may find it useful. It will prompt for the URL of a directory and look for links ending in .jpg, .jpeg, .gif, and .png. You can easily add other extensions in the code. It will prompt you for the image output directory, then download those images to that directory. 

In the directory the script is ran from, you should also have a template.html file, and a pictures.html file. I've included blank ones in this. 

Your template.html file should have two things prior: PLACEHOLDER and CODE. The script will generate a copy of template.html in the same folder as the script and rename it to the same name as the image output folder. The script will look for a line with the word PLACEHOLDER and then replace that with the image directory name. Then it will generate image embed HTML tags to display every image in the image directory and inject them into the new html file replacing where the line CODE is. The script then looks at pictures.html and finds the line <!-- LIST --> and will place embedded links to the newly created HTML document. 

Once it's done, the script points to the directories for each of the generated files and directories and prompts to push enter to scrape another directory or type q to exit.
