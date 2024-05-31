import os
from ultralytics import YOLO
import xml.etree.ElementTree as ET

import cv2
import matplotlib.pyplot as plt
import numpy as np

from PIL import Image

weigths_path = os.path.join(os.path.dirname(__file__), "..", "..", "model", "weigthts", "best.pt")
marked_path = os.path.join(os.path.dirname(__file__), "..", "temp", "marked_images")
model = YOLO(weigths_path)


def detect(images):
    results = []
    for image in images:
        results.append(model(image))
    return results


def convertToXML(results):
    print(results)
    root = ET.Element("signals")


    for result in results:
        print(result[0].boxes)
        for box in result[0].boxes:
            print(box)

            signal = ET.SubElement(root, "signal")
            cls = int(box.cls[0])
            label = f"{model.names[cls]}"
            signal.set("color", label)
            
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            coordinates = ET.SubElement(signal, "coordinates")
            coordinates.set("x1", str(x1))
            coordinates.set("x2", str(x2))
            coordinates.set('y1', str(y1))
            coordinates.set("y2", str(y2))
    
    with open("signals.xml", "w") as xml_file:
        xml_file.write(ET.tostring(root).decode())

def generate_xml(all_boxes, images_per_col, images_per_row):
    root = ET.Element("Signals")

    base_offset_left = 1200
    base_offset_up = 600

    row = -1
    for idx, boxes in enumerate(all_boxes):
        col = idx % images_per_row
        if (col == 0):
            row+=1
        print(f"col:{col} row:{row} boxes:{len(boxes)}")

        for box in boxes:
            signalElement = ET.SubElement(root, "Signal")
            cls = int(box.cls[0])
            label = f"{model.names[cls]}"
            
            colourElement = ET.SubElement(signalElement, "Color")
            colourElement.text = label

            coordinateElement = ET.SubElement(signalElement, "Coordinate")

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            xElement = ET.SubElement(coordinateElement, "XVal")
            x1Element = ET.SubElement(xElement, "X1Val")
            x1Element.text = str(x1 + col * base_offset_left)
            x2Element = ET.SubElement(xElement, "X2Val")
            x2Element.text = str(x2 + col * base_offset_left)
            yElement = ET.SubElement(coordinateElement, "YVal")
            y1Element = ET.SubElement(yElement, "Y1Val")
            y1Element.text = str(y1 + row * base_offset_up)
            y2Element = ET.SubElement(yElement, "Y2Val")
            y2Element.text = str(y2 + row * base_offset_up)

            confElement = ET.SubElement(signalElement, "Confidence")
            confElement.text = f"{box.conf[0]:.2f}"

    with open("signals.xml", "w") as xml_file:
        xml_file.write(ET.tostring(root).decode())

from sklearn.cluster import DBSCAN
def readXmlAndAggregateInSemaphores():
    tree = ET.parse("signals.xml")
    root = tree.getroot()

    coordinates = []
    signals = []
    for signal in root.findall('Signal'):
        x1 = int(signal.find('Coordinate/XVal/X1Val').text)
        x2 = int(signal.find('Coordinate/XVal/X2Val').text)
        y1 = int(signal.find('Coordinate/YVal/Y1Val').text)
        y2 = int(signal.find('Coordinate/YVal/Y2Val').text)
        signals.append({
            "signal_type": signal.find('Color').text,
            "x1" : x1,
            "x2" : x2,
            "y1" : y1,
            "y2" : y2,
            "confidence" : float(signal.find("Confidence").text) 
        })
        coordinates.append([x1, x2, y1, y2])

    X = np.array(coordinates)

    dbscan = DBSCAN(eps=100, min_samples=2) 
    clusters = dbscan.fit_predict(X)

    image = cv2.imread('original.png')
    _ , width, _ = image.shape
    img = image[:, :width - width%1200]

    for cluster in clusters:
        print(cluster)

    import random    
    colors = {}
    for cluster in set(clusters):
        if cluster == -1:
            colors[cluster] = (0, 0, 255)  # Красный цвет для шума
        else:
            colors[cluster] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    for i, cluster in enumerate(clusters):
        signals[i]["sem_id"] = cluster

    from functools import reduce
    from collections import defaultdict
    grouped_by_semaphore = list(reduce(
        lambda acc, item: acc[item["sem_id"]].append(item) or acc,
        signals,
        defaultdict(list)
    ).values())

    root = ET.Element("Semaphores")

    for semaphore in grouped_by_semaphore:
        semaphore_el = ET.SubElement(root, "Semaphore")

        filtered_sem = list(filter(lambda x: x["sem_id"] != -1 and x["confidence"] >= 0.5, semaphore))
        if (len(filtered_sem) == 0):
            continue

        box = ET.SubElement(semaphore_el, "Box")
        print(filtered_sem)
        min_x1 = min(filtered_sem, key=lambda x : x["x1"])["x1"]
        min_y1 = min(filtered_sem, key=lambda x: x["y1"])["y1"]

        bottom_left = ET.SubElement(box, "BottomLeft")
        x1 = ET.SubElement(bottom_left, "XVal")
        y1 = ET.SubElement(bottom_left, "YVal")
        x1.text = str(min_x1)
        y1.text = str(min_y1)

        max_x2 = max(filtered_sem, key=lambda x: x["x2"])["x2"]
        max_y2 = max(filtered_sem, key=lambda x: x["y2"])["y2"]
        upper_right = ET.SubElement(box, "UpperRight")
        x2 = ET.SubElement(upper_right, "XVal")
        y2 = ET.SubElement(upper_right, "YVal")
        x2.text = str(max_x2)
        y2.text = str(max_y2)

        signals_el = ET.SubElement(semaphore_el, "Signals")

        for signal in sorted(semaphore, key=lambda x: x["x1"]):
            signal_el = ET.SubElement(signals_el, "Signal")
            color_el = ET.SubElement(signal_el, "Color")
            color_el.text = signal["signal_type"]


        cv2.rectangle(img, (min_x1, min_y1), (max_x2, max_y2), colors[filtered_sem[0]["sem_id"]], 2)

    
    cv2.imwrite("semaphores.png", img)
    with open("semaphores.xml", "wb") as xml_file:
        tree = ET.ElementTree(root)
        tree.write(xml_file, encoding="utf-8", xml_declaration=True)


def process_slices(pathes, wer, hor):
    images = []
    all_boxes = []

    for path in pathes:
        boxes, image = process_image_slice(path)
        images.append(image)
        all_boxes.append(boxes)
    
    stitch_images(images, hor)
    generate_xml(all_boxes, wer, hor)
    validateXml()
    readXmlAndAggregateInSemaphores()

def validateXml():
    tree = ET.parse('signals.xml')
    root = tree.getroot()

    img = cv2.imread("result.png")

    for signal in root.findall('Signal'):
        x1 = int(signal.find('.//X1Val').text)
        x2 = int(signal.find('.//X2Val').text)
        y1 = int(signal.find('.//Y1Val').text)
        y2 = int(signal.find('.//Y2Val').text)
        
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), thickness=5)
    
    cv2.imwrite("validate.png", img)
    
def stitch_images(images, images_per_row):
    if not images:
        return None

    slice_height, slice_width = images[0].shape[:2]
    num_rows = len(images) // images_per_row

    # Create a blank image with the correct size
    merged_image = np.zeros((num_rows * slice_height, images_per_row * slice_width, 3), dtype=np.uint8)

    for idx, img in enumerate(images):
        row = idx // images_per_row
        col = idx % images_per_row
        merged_image[row * slice_height:(row + 1) * slice_height, col * slice_width:(col + 1) * slice_width] = img
    
    merged_image_pil = Image.fromarray(cv2.cvtColor(merged_image, cv2.COLOR_RGB2RGBA))
    merged_image_pil.save("result.png")
    return merged_image

def process_image_slice(image_path):
    results = model(image_path)

    class_colors = {
        'Green_signal': (0, 255, 0),   # green
        'Blue_signal': (0, 0, 255),    # blue
        'Yellow_signal': (255, 255, 0),# yellow
        'White_Signal': (0, 0, 0),     # black
        'Red_signal': (255, 0, 0)      # red
    }

    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    predictions = results[0]

    for box in predictions.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = box.conf[0]
        cls = int(box.cls[0])
        label = f"{model.names[cls]}: {conf:.2f}"
        class_color = class_colors.get(model.names[cls], (255, 255, 255))

        cv2.rectangle(image, (x1, y1), (x2, y2), class_color, 2)
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, class_color, 2)

    cv2.imwrite(image_path.replace("images", "marked_images"), cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

    return predictions.boxes, image
    

if __name__ == "__main__":
    process_image_slice("C:/Users/soriv/Desktop/signals/Searching-Signals/temp/images/6f4922f45568161a8cdf4ad2299f6d23_0-0.png")
