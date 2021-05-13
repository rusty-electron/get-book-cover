import requests
import argparse
import json
import os
import sys

import numpy as np
import cv2

BK_API = "https://openlibrary.org/search.json"
COVER_API = "http://covers.openlibrary.org/b/isbn/"

def get_response(query):
    url_dict = {
    'q': query
    }

    response = requests.request("GET", BK_API, params=url_dict)
    b_list = json.loads(response.text)
    return b_list

def get_cover(isbn):
    resp = requests.get(COVER_API + isbn + "-L.jpg", stream=True).raw
    img = np.asarray(bytearray(resp.read()), dtype="uint8")
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return img

def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def handle_key(image, save_dir):
    while True:
        key = cv2.waitKey(0)
        if key == ord("y") or key == ord("Y"):
            cv2.destroyAllWindows()
            filename = input("Save image as: ")
            create_dir(save_dir)
            cv2.imwrite(os.path.join(save_dir, filename), image)
            break
        elif key == ord("n") or key == ord("n"):
            cv2.destroyAllWindows()
            print("[INFO] getting the next image...")
            break
        elif key == ord("q") or key == ord("Q"):
            print("[INFO] exiting...")
            cv2.destroyAllWindows()
            sys.exit()
        else:
            continue

if __name__ == "__main__":
    ag = argparse.ArgumentParser()
    ag.add_argument("-q", "--query", required=True, help="search term")
    ag.add_argument("-d", "--dir", default="./img", help="image save path")
    args = vars(ag.parse_args())

    book_list = get_response(args["query"])
    num_found = len(book_list.get('docs'))

    if num_found == 0:
        print("[INFO] no results found, exiting...")
        sys.exit()

    print(f"[INFO] {num_found} total results")

    for i, book_item in enumerate(book_list.get("docs")):
        try:
            current_isbn = book_item.get("isbn")[0]
        except TypeError:
            print("[warning] empty ISBN list")
            continue

        # show image
        try:
            image = get_cover(current_isbn)
            cv2.imshow(f'image #{i}', image)
            handle_key(image, args["dir"])
        except cv2.error:
            print("[warning] received weird image")
            continue
    print("[INFO] end of results")
