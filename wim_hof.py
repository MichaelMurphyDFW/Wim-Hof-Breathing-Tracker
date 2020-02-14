import os
from PIL import Image
import cv2
import pytesseract
from time import sleep
import json

print(os.getcwd())

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

original_dir = os.path.abspath(f"{os.getcwd()}../../../../Wim Hof")
resized_dir = os.path.abspath(f"{os.getcwd()}../../../../Wim Hof/resized")

sessions = []

while True:
    sleep(5)
    print("Pausing for 5 seconds...")

    with open ("projects/wim_hof/processed_images.txt", "r") as processed:

        processed_files = processed.read().split("\n")
        num_recorded_files = len(processed_files)-1
        print("num recorded files:",num_recorded_files)
        print("files in folder:",len(os.listdir(original_dir)))

        if num_recorded_files != len(os.listdir(original_dir)):

            # with open("processed_images.txt", "a+") as processed:
            with open("projects/wim_hof/processed_images.txt", "a+") as processed:


                for image in os.listdir(original_dir):
                    if (image.endswith(".png") or image.endswith(".PNG")) and image not in processed_files:
                        cv_image = Image.open(f"{original_dir}/{image}")
                        (w,h) = cv_image.size
                        cropped = cv_image.crop((900,1450,w,2012))
                        cropped.show()

                        processed.write(f"{image}\n")

                        times = []
                        img_date = image.split(",")[0][6:]
                        print(img_date)
                        text = pytesseract.image_to_string(cropped,lang="SF-numsonly")

                        parsed = [text for text in text.split("\n") if ":" in text]
                        for time in parsed:
                            (min,sec) = time.split(":")
                            min = int(min)
                            sec = float(sec[:2])
                            if (60*min) + sec > 30:
                                times.append((min,round(sec)))
                        times.reverse()
                        session = {k+1:v for k,v in enumerate(times)}
                        to_json = list(img_date,session)
                        print(to_json)
                        with open('sessions.json', 'a+') as f:
                            json.dump(to_json,f)
