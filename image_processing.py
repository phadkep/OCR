import cv2
from paddleocr import PaddleOCR, draw_ocr
import tensorflow as tf
import numpy as np
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd


def perform_text_detection_and_recognition(image_path, det_model_dir, rec_model_dir, cls_model_dir):

    ocr = PaddleOCR(lang='en', det_model_dir=det_model_dir, rec_model_dir=rec_model_dir, cls_model_dir=cls_model_dir)
    image_cv = cv2.imread(image_path)
    output = ocr.ocr(image_path)[0]
    
    boxes = [line[0] for line in output]
    texts = [line[1][0] for line in output]
    probabilities = [line[1][1] for line in output]
    print("cropped output", texts)

    # Draw bounding boxes and text on the image
    image_boxes = image_cv.copy()
    for box, text in zip(boxes, texts):
        cv2.rectangle(image_boxes, (int(box[0][0]), int(box[0][1])), (int(box[2][0]), int(box[2][1])), (0, 0, 255), 1)
        # cv2.putText(image_boxes, text, (int(box[0][0]), int(box[0][1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (222, 0, 0), 1)

    cv2.imwrite('Images/detections.jpg', image_boxes)
    return boxes, texts, probabilities


def extract_horizontal_and_vertical_box(image_path, boxes):
    """
    Extracts the horizontal and vertical lines from the detected text boxes.

    Args:
        image_path (str): The path to the image file.
        boxes (list): A list of bounding boxes for the detected text.
    """
    image_cv = cv2.imread(image_path)
    image_width = image_cv.shape[1]
    image_height = image_cv.shape[0]

    horiz_boxes = []
    vert_boxes = []

    for box in boxes:
        x_h, x_v = 0, int(box[0][0])
        y_h, y_v = int(box[0][1]), 0
        width_h, width_v = image_width, int(box[2][0] - box[0][0])
        height_h, height_v = int(box[2][1] - box[0][1]), image_height

        horiz_boxes.append([x_h,y_h,x_h+width_h,y_h+height_h])
        vert_boxes.append([x_v,y_v,x_v+width_v,y_v+height_v])

        cv2.rectangle(image_cv, (x_h, y_h), (x_h + width_h, y_h + height_h), (0, 0, 255), 1)
        cv2.rectangle(image_cv, (x_v, y_v), (x_v + width_v, y_v + height_v), (0, 255, 0), 1)

    cv2.imwrite('Images/horiz_vert.jpg', image_cv)
    return horiz_boxes, vert_boxes



def extract_lines_using_nms(image_path, horiz_boxes, vert_boxes, probabilities):
    # Non-maximum suppression on horizontal lines
    horiz_out = tf.image.non_max_suppression(
        horiz_boxes,
        probabilities,
        max_output_size=1000,
        iou_threshold=0.1,
        score_threshold=float('-inf'),
        name=None
    )

    horiz_lines = np.sort(np.array(horiz_out))

    # Draw the filtered horizontal lines on the image
    im_nms = cv2.imread(image_path)
    for val in horiz_lines:
        cv2.rectangle(im_nms, (int(horiz_boxes[val][0]), int(horiz_boxes[val][1])), (int(horiz_boxes[val][2]), int(horiz_boxes[val][3])), (0, 0, 255), 1)

    cv2.imwrite('Images/im_nms.jpg', im_nms)

    # Non-maximum suppression on vertical lines
    vert_out = tf.image.non_max_suppression(
        vert_boxes,
        probabilities,
        max_output_size=10,
        iou_threshold=0.1,
        score_threshold=float('-inf'),
        name=None
    )

    vert_lines = np.sort(np.array(vert_out))

    # Draw the filtered vertical lines on the image
    for val in vert_lines:
        cv2.rectangle(im_nms, (int(vert_boxes[val][0]), int(vert_boxes[val][1])), (int(vert_boxes[val][2]), int(vert_boxes[val][3])), (255, 0, 0), 1)

    cv2.imwrite('Images/im_nms.jpg', im_nms)

    return horiz_lines, vert_lines



def convert_to_csv(horiz_lines, vert_lines, horiz_boxes, vert_boxes, boxes, texts):

    out_array = [["" for i in range(len(vert_lines))] for j in range(len(horiz_lines))]

    unordered_boxes = []
    for i in vert_lines:
        unordered_boxes.append(vert_boxes[i][0])

    ordered_boxes = np.argsort(unordered_boxes)

    for i in range(len(horiz_lines)):
        for j in range(len(vert_lines)):
            resultant = intersection(horiz_boxes[horiz_lines[i]], vert_boxes[vert_lines[ordered_boxes[j]]])

            for b in range(len(boxes)):
                the_box = [boxes[b][0][0], boxes[b][0][1], boxes[b][2][0], boxes[b][2][1]]
                if iou(resultant, the_box) > 0.1:
                    out_array[i][j] = texts[b]

    return np.array(out_array)

def intersection(box_1, box_2):
    x_min = max(box_1[0], box_2[0])
    y_min = max(box_1[1], box_2[1])
    x_max = min(box_1[2], box_2[2])
    y_max = min(box_1[3], box_2[3])

    if x_min > x_max or y_min > y_max:
        return []
    else:
        return [x_min, y_min, x_max, y_max]

def iou(box_1, box_2):
    x_1 = max(box_1[0], box_2[0])
    y_1 = max(box_1[1], box_2[1])
    x_2 = min(box_1[2], box_2[2])
    y_2 = min(box_1[3], box_2[3])

    inter = abs(max((x_2 - x_1, 0)) * max((y_2 - y_1), 0))
    if inter == 0:
        return 0

    box_1_area = abs((box_1[2] - box_1[0]) * (box_1[3] - box_1[1]))
    box_2_area = abs((box_2[2] - box_2[0]) * (box_2[3] - box_2[1]))

    return inter / float(box_1_area + box_2_area - inter)

