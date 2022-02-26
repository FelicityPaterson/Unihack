from contextlib import nullcontext
from pyzbar import pyzbar
from cv2 import cv2
# import requests
barcode_number = -1

url = "https://barcode-lookup.p.rapidapi.com/v3/products"


# headers = {
#     'x-rapidapi-host': "barcode-lookup.p.rapidapi.com",
#     'x-rapidapi-key': "5d899471bbmsh7cab72ee0dc5c50p15121fjsna9ae1c87b523"
#     }

# response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)


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
    # decodes all barcodes from an image
    decoded_objects = pyzbar.decode(image)
    for obj in decoded_objects:
        # draw the barcode
        image = draw_barcode(obj, image)
        # print barcode type & data
        print("Type:", obj.type)
        print("Data:", obj.data.decode())
        barcode_number = obj.data.decode()
        querystring = {"barcode":obj.data}

        print()

    return image


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    while barcode_number == -1:
        print(barcode_number)
        # read the frame from the camera
        _, frame = cap.read()
        # decode detected barcodes & get the image
        # that is drawn
        frame = decode(frame)
        # show the image in the window
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) == ord("q"):
            break
        