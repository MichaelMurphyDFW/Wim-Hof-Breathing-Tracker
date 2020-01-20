import os
from PIL import Image
import cv2
import pytesseract
from time import sleep
import json

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Laptop
# original_dir = os.path.abspath(f"{os.getcwd()}../../Wim Hof")

# Desktop
original_dir = os.path.abspath(f"{os.getcwd()}../../../../Wim Hof")
# project_dir = os.path.abspath(f"{os.getcwd()})

print(os.path.abspath("projects/wim_hof/processed_images.txt"))

print(os.getcwd())
print(original_dir)

while True:
    sessions = {}
    sleep(5)

    with open ("sessions.json") as f:
        try:
            processed_files = json.load(f)
        except:
            processed_files = {}

        completed_filenames = []
        for session in processed_files:
            completed_filenames.append(processed_files[session]['filename'])


        if len(completed_filenames) < len(os.listdir(original_dir)):

            for image in os.listdir(original_dir):
                if (image.endswith(".png") or image.endswith(".PNG")) and image not in completed_filenames:
                    cv_image = Image.open(f"{original_dir}/{image}")
                    (w,h) = cv_image.size
                    cropped = cv_image.crop((900,1450,w,2012))
                    # cropped.show()

                    img_date = image.split(",")[0][6:]

                    text = pytesseract.image_to_string(cropped,lang="SF-numsonly")
                    parsed = [text for text in text.split("\n") if ":" in text]

                    sessions[img_date] = {}
                    sessions[img_date]['rounds'] = {}

                    stage = 1
                    for time in reversed(parsed):
                        (min,sec) = time.split(":")
                        min = int(min)
                        sec = float(sec[:2])
                        if (60*min) + sec > 30:
                            times = {}
                            times['min'] = min
                            times['sec'] = round(sec)
                            sessions[img_date]['rounds'][stage] = times
                            sessions[img_date]['filename'] = image
                            stage += 1

            if completed_filenames:
                with open('sessions.json') as f:
                    in_data = json.load(f)
                    in_data.update(sessions)
                    with open('sessions.json',"w") as f:
                        json.dump(in_data,f, indent=4)
            else:
                print("JSON file empty. Adding new data.")
                with open('sessions.json',"w") as f:
                    json.dump(sessions,f, indent=4)
