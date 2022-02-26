from contextlib import nullcontext
from pyzbar import pyzbar
from cv2 import cv2
from bs4 import BeautifulSoup as BSoup
import requests

barcode_number = -1
url = "https://au.openfoodfacts.org/cgi/search.pl?search_terms="



def draw_barcode(decoded, image):
    # n_points = len(decoded.polygon)
    # for i in range(n_points):
    #     image = cv2.line(image, decoded.polygon[i], decoded.polygon[(i+1) % n_points], color=(0, 255, 0), thickness=5)
    image = cv2.rectangle(image, (decoded.rect.left, decoded.rect.top), 
                            (decoded.rect.left + decoded.rect.width, decoded.rect.top + decoded.rect.height),
                            color=(0, 255, 0),
                            thickness=5)
    return image

def decode(image):
    global url
    global barcode_number
    # decodes all barcodes from an image
    decoded_objects = pyzbar.decode(image)
    for obj in decoded_objects:
        # draw the barcode
        image = draw_barcode(obj, image)
        # print barcode type & data
        print("Type:", obj.type)
        print("Data:", obj.data.decode())
        barcode_number = obj.data.decode()
        url += str(barcode_number)
        webpageContent = requests.get(url).text
        title = BSoup(webpageContent, "html.parser").title.text
        if title == "Search results - Australia" or title == "Error":
            print("error")
        else:
            print(title)
    return image




if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    while barcode_number == -1:
        # read the frame from the camera
        _, frame = cap.read()
        # decode detected barcodes & get the image
        # that is drawn
        frame = decode(frame)
        # show the image in the window
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) == ord("q"):
            break
        