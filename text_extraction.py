import pandas as pd
import re

def extract_transcript_data(full_output, output_excel_path):
    """
    Extracts relevant information from the OCR-processed text, creates a DataFrame, and saves it to an Excel file.

    Args:
        full_output (list): The full output from the OCR process.
        output_excel_path (str): The path to the output Excel file.
    """
    if full_output is not None:
        # Extract transcript data
        texts = [line[1][0] for line in full_output]
        transcript_data = get_transcript_data(texts)
        print(transcript_data)

        # Create a DataFrame and save to Excel
        df = pd.DataFrame(transcript_data.items(), columns=['Key', 'Value'])
        df.to_excel(output_excel_path, index=False, header=False)
        print(f"Transcript data saved to: {output_excel_path}")
    else:
        print("Error: Unable to process the image.")

def get_transcript_data(texts):
    """
    Extracts relevant information from the OCR-processed text and returns a dictionary.

    Args:
        texts (list): A list of extracted text lines from the OCR process.

    Returns:
        dict: A dictionary containing the extracted information.
    """
    print("\n # Initialize an empty dictionary to store the extracted information \n")
    data = {
        "Name": "",
        "University": "",
        "Course": "",
        "CGPA": "",
        "Percentage": "",
        "Autonomous": ""
    }

    # EXTRACTING NAME
    for i in range(len(texts)):
        if texts[i] == 'Name:' or texts[i] == 'Name':
            if i + 1 < len(texts):
                data["Name"] = texts[i + 1]
                break
    else:
        for text in texts:
            if 'mr./ms' in text.lower() or 'ms.' in text.lower():
                data["Name"] = text
                break

    # EXTRACTING UNIVERSITY NAME
    for text in texts:
        if 'university' in text.lower() or 'institute' in text.lower() or 'college' in text.lower():
            data["University"] = text
            break

    # EXTRACTING COURSE
    for text in texts:
        if 'engineering' in text.lower() and ('b.e.' in text.lower() or 'b.tech.' in text.lower() or 'computer' in text.lower() or 'metallurgical' in text.lower()):
            data["Course"] = text
            break
    else:
        for i in range(len(texts)):
            if texts[i] == 'Branch:' or texts[i] == 'Branch':
                if i + 1 < len(texts):
                    data["Course"] = texts[i + 1]
                    break

    # EXTRACTING CGPA
    for i in range(len(texts)):
        if texts[i] == 'CGPA:':
            if i + 1 < len(texts):
                data["CGPA"] = texts[i + 1]
                break
    else:
        for text in texts:
            if 'cgpa' in text.lower() or 'sgpa' in text.lower():
                match = re.search(r'\b(\d+\.\d+)\b', text, re.IGNORECASE)
                if match:
                    cgpa_value = match.group(1)
                    data["CGPA"] = cgpa_value
                    break

    # EXTRACTING PERCENTAGE
    for i in range(len(texts)):
        if texts[i] == 'PERCENTAGE:':
            if i + 1 < len(texts):
                data["Percentage"] = texts[i + 1]
                break
    else:
        for text in texts:
            if '%' in text and 'percentage' in text.lower():
                data["Percentage"] = text
                break

    # CHECK IF UNIVERSITY IS AUTONOMOUS OR NOT
    for text in texts:
        if 'autonomous' in text.lower():
            data["Autonomous"] = "Y"
            break

    return data