# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 11:02:06 2020

@author: OHyic

"""
# Import libraries
import os
import concurrent.futures
from googleimages_service.GoogleImageScraper import GoogleImageScraper
from googleimages_service.patch import webdriver_executable


def worker_thread(search_key, keep_filenames, GISkwargs):
    image_scraper = GoogleImageScraper(search_key=search_key, **GISkwargs)
    image_urls = image_scraper.find_image_urls()
    paths = image_scraper.save_images(image_urls, keep_filenames)

    # Release resources
    del image_scraper

    return paths


def search_images(queries: list) -> list:
    # Define file path
    webdriver_path = os.path.normpath(
        os.path.join(__file__, "..", "webdriver", webdriver_executable())
    )
    image_path = os.path.normpath(os.path.join(__file__, "..", "photos"))

    # Parameters
    number_of_images = 2  # Desired number of images
    headless = True  # True = No Chrome GUI
    min_resolution = (0, 0)  # Minimum desired image resolution
    max_resolution = (9999, 9999)  # Maximum desired image resolution
    max_missed = 10  # Max number of failed images before exit
    number_of_workers = 2  # Number of "workers" used
    keep_filenames = False  # Keep original URL image filenames

    GISkwargs = {
        "webdriver_path": webdriver_path,
        "image_path": image_path,
        "number_of_images": number_of_images,
        "headless": headless,
        "min_resolution": min_resolution,
        "max_resolution": max_resolution,
        "max_missed": max_missed,
    }

    # Run each search_key in a separate thread
    # Automatically waits for all threads to finish
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=number_of_workers
    ) as executor:
        outputs = list(
            executor.map(
                worker_thread,
                queries,
                [keep_filenames] * len(queries),
                [GISkwargs] * len(queries),
            )
        )

    return [x[0] for x in outputs]


if __name__ == "__main__":
    # Add new search key into array ["cat","t-shirt","apple","orange","pear","fish"]
    search_keys = list(
        set(
            [
                "A person pushing a heavy rock uphill",
                "A person running away from a mountain",
                "Sisyphus pushing a rock uphill",
            ]
        )
    )

    print(search_images(search_keys))
