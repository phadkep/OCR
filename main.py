import os
import glob
from pdf_to_images import pdf_to_images
from layout_detection import detect_layout_and_ocr
from text_extraction import extract_transcript_data
from image_utils import find_item, crop_and_save_image
from image_processing import perform_text_detection_and_recognition, extract_horizontal_and_vertical_box, extract_lines_using_nms, convert_to_csv
from excel_utils import write_to_excel, merge_duplicate_rows, merge_columns_with_identical_text
from excel_to_json import convert_excel_to_json
import json

def main(pdf_path):
    pdf_path = pdf_path
    #pdf_path = 'Transcript.pdf'
    output_folder = 'pages'
    det_model_dir = 'Model/en_PP-OCRv3_det_infer'
    rec_model_dir = 'Model/models/en_PP-OCRv4_rec_infer'
    cls_model_dir = 'Model/models/ch_ppocr_mobile_v2.0_cls_infer'
    image_path = 'pages/page0.jpg'
    output_excel_path = 'ExcelsSheets/Transcript_output.xlsx'
    output_json_path = 'excelToJson.json'

    # Convert PDF to images
    pdf_to_images(pdf_path, output_folder)
    # Detect layout and perform OCR on the cropped image
    
    final_output = {}
    sem=1
    # Process each page
    all_csv_outputs = []
    page_count = len(glob.glob(f"{output_folder}/page*.jpg"))
    for page_num in range(page_count):
        
        image_path = f'{output_folder}/page{page_num}.jpg'
        img_path = f'{output_folder}/page{page_num}.jpg'
        output_image_path = f'Images/ext_im_page{page_num}.jpg'
        page_excel_path = output_excel_path
        full_output = detect_layout_and_ocr(image_path, det_model_dir, rec_model_dir, cls_model_dir)
        extract_transcript_data(full_output, output_excel_path)

        try:
            # Crop and save the image
            crop_and_save_image(full_output, img_path, output_image_path)

            # Perform text detection and recognition
            boxes, texts, probabilities = perform_text_detection_and_recognition(output_image_path, det_model_dir, rec_model_dir, cls_model_dir)

            # Extract horizontal and vertical boxes
            horiz_boxes, vert_boxes = extract_horizontal_and_vertical_box(output_image_path, boxes)

            # Extract lines using non-maximum suppression
            horiz_lines, vert_lines = extract_lines_using_nms(output_image_path, horiz_boxes, vert_boxes, probabilities)

            # Convert the output to CSV format
            csv_output = convert_to_csv(horiz_lines, vert_lines, horiz_boxes, vert_boxes, boxes, texts)

            # Write the CSV-like output to the Excel file
            write_to_excel(csv_output, page_excel_path)

            # Merge duplicate rows and columns with identical text
            merge_duplicate_rows(page_excel_path)
            merge_columns_with_identical_text(page_excel_path)
            # Convert the combined Excel file to JSON
            json_data = convert_excel_to_json(output_excel_path, output_json_path)
        except Exception as e:
            print(f"Error processing page {page_num}: {e}")
        sem_name = "Semester " + str(sem)
        final_output[sem_name] = json_data
        sem += 1 
    
    json_data = json.dumps(final_output, indent=2)
    # Save the JSON data to a file
    with open(output_json_path, 'w') as json_file:
        json_file.write(json_data)
 
    

    return json_data

if __name__ == "__main__":
    main()
