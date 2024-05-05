import pandas as pd
import json

def convert_excel_to_json(excel_file_path,  output_json_path):
    """
    Converts the data from an Excel file to a JSON format and saves it to a file.

    Args:
        excel_file_path (str): The path to the Excel file.
        sheet1_name (str): The name of the first sheet.
        sheet2_name (str): The name of the second sheet.
        output_json_path (str): The path to the output JSON file.
    """
    # Read the Excel data into pandas DataFrames
    df1 = pd.read_excel(excel_file_path, sheet_name='Sheet1', header=None)
    df2 = pd.read_excel(excel_file_path, sheet_name='Sheet2')

    # Get the column names from the second sheet
    df2_columns = df2.columns.tolist()

    # Convert the first DataFrame to a dictionary
    data1 = {
        "Name": df1.iloc[0, 1],
        "University": df1.iloc[1, 1],
        "Course": df1.iloc[2, 1],
        "CGPA": df1.iloc[3, 1],
        "Percentage": df1.iloc[4, 1],
        "Autonomous": df1.iloc[5, 1]
    }

    # Convert the second DataFrame to a list of dictionaries
    data2 = df2.to_dict(orient='records')

    # Combine the data from both sheets
    combined_data = {
        **data1,
        "Course Info": data2
    }

    return combined_data
    # Convert the combined data to JSON
    # json_data = json.dumps(combined_data, indent=2)
    # print(json_data)
    
    # Save the JSON data to a file
    # with open(output_json_path, 'a') as json_file:
        # json_file.write(json_data)
