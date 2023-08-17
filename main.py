"""Python project to pull a random comic from xkcd.com and display it in a window."""

import os
import sys
import random
import requests
import tkinter as tk
from PIL import Image, ImageTk

# Global variables
COMIC_DIR = os.path.join(os.getcwd(), "comics")
COMIC_URL = "https://xkcd.com/{}/info.0.json"
COMIC_MAX = 2473
COMIC_MIN = 1

# Function to get a random comic
def get_comic():
    """
    Function to get a random comic from xkcd.com.

    Returns:
        comic (dict): Dictionary of comic information.
    """
    comic_num = random.randint(COMIC_MIN, COMIC_MAX)
    comic = requests.get(COMIC_URL.format(comic_num)).json()
    return comic

# Function to download a comic
def download_comic(comic):
    """
    Function to download a comic from xkcd.com.

    Args:
        comic (dict): Dictionary of comic information.
    """
    comic_num = comic["num"]
    comic_img = comic["img"]
    comic_title = comic["title"]
    comic_alt = comic["alt"]

    comic_file = os.path.join(COMIC_DIR, f"{comic_num}.png")
    if not os.path.exists(comic_file):
        comic_data = requests.get(comic_img).content
        with open(comic_file, "wb") as file:
            file.write(comic_data)

    return comic_file, comic_title, comic_alt

# Function to display a comic
def display_comic(comic_file, comic_title, comic_alt):
    """
    Function to display a comic in a window.

    Args:
        comic_file (str): Path to comic file.
        comic_title (str): Title of comic.
        comic_alt (str): Alt text of comic.
    """
    window = tk.Tk()
    window.title(comic_title)
    window.geometry("800x600")

    comic_image = Image.open(comic_file)
    # comic_image = comic_image.resize((800, 600))
    comic_image = ImageTk.PhotoImage(comic_image)

    comic_label = tk.Label(window, image=comic_image)
    comic_label.pack()

    alt_label = tk.Label(window, text=comic_alt)
    alt_label.pack()

    window.mainloop()

# Main function
def main():
    """Main function."""

    # Check if comics directory exists
    if not os.path.exists(COMIC_DIR):
        os.mkdir(COMIC_DIR)
    comic = get_comic()
    comic_file, comic_title, comic_alt = download_comic(comic)
    display_comic(comic_file, comic_title, comic_alt)

# Main guard
if __name__ == "__main__":
    main()