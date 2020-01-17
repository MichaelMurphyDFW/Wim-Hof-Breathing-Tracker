import os
from PIL import Image
import cv2
import pytesseract
from time import sleep
import json

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

original_dir = os.path.abspath(f"{os.getcwd()}../../../../Wim Hof")
resized_dir = os.path.abspath(f"{os.getcwd()}../../../../Wim Hof/resized")

print(original_dir, resized_dir)

sessions = []


while True:
    with open ("processed_images.txt", "r") as processed:
        print("Pausing for 5 seconds...")
        sleep(5)

        processed_files = processed.read().split("\n")
        num_recorded_files = len(processed_files)
        print(num_recorded_files)
        print(len(os.listdir(original_dir)))

        if num_recorded_files != len(os.listdir(original_dir)):


            with open("processed_images.txt", "a+") as processed:


                for image in os.listdir(original_dir):
                    if image.endswith(".png") and image not in processed_files:
                        # print(f"Resizing {image}")
                        resized = Image.open(f"{original_dir}/{image}")
                        # print(f"size: {resized.size}")
                        (w,h) = resized.size
                        cropped = resized.crop((900,1450,w,2012))
                        cropped.save(f"{resized_dir}/{image}_600.png", dpi=(600,600))

                        processed.write(f"{image}\n")

                for image in os.listdir(resized_dir):
                    if image.endswith(".png"):
                        times = []
                        imgpath = f"{resized_dir}/{image}"
                        img_date = image.split(",")[0][6:]
                        print(img_date)
                        text = pytesseract.image_to_string(Image.open(imgpath),lang="SF-numsonly")

                        parsed = [text for text in text.split("\n") if ":" in text]
                        for time in parsed:
                            (min,sec) = time.split(":")
                            min = int(min)
                            sec = float(sec[:2])
                            if (60*min) + sec > 30:
                                times.append((min,round(sec)))
                        times.reverse()
                        session = {k+1:v for k,v in enumerate(times)}
                        sessions.append([img_date,session])
                        with open('sessions.json', 'w') as f:
                            json.dump(sessions,f)
