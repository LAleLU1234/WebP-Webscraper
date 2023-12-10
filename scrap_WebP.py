import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import os
import re

def download_image(url, folder):
    """Download an image from a URL and save it in the specified folder."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            file_path = os.path.join(folder, url.split('/')[-1])
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {url}")
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")

def scrape_images(start_url, target_folder):
    """Scrape images from a webpage and save them to a folder."""
    driver = webdriver.Firefox()
    driver.get(start_url)

    try:
        div_elements = driver.find_elements(By.CSS_SELECTOR, "Div.item.invisible")
        print(f"Found {len(div_elements)} div elements.")

        for div in div_elements:
            img = div.find_element(By.TAG_NAME, 'img')
            src = img.get_attribute('src')
            if src and re.match(r'https://xfs-.*\.batcg\.org/comic/', src):
                download_image(src, target_folder)
            else:
                print(f"Skipped image: {src}")
    except Exception as e:
        print(f"Error scraping website: {str(e)}")
    finally:
        driver.quit()

# Start URL and target folder
target_folder = "/home/mint/Schreibtisch/projekt/scrapit again"

# Create and run the application
app = tk.Tk()
app.title("WebP Image Scraper")

tk.Label(app, text="URL:").pack()
url_entry = tk.Entry(app)
url_entry.pack()

# Start scraping when the button is clicked
tk.Button(app, text="Scrape Images", command=lambda: scrape_images(url_entry.get(), target_folder)).pack()

app.mainloop()
