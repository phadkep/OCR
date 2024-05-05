# OCR-Transcript-Project

This project serves as my capstone, a university assignment. It involves translating or converting transcript PDF data into Excel and JSON formats. This enables the university to efficiently filter applications and conduct post-processing, streamlining the admission process.

## Dataset
We utilize images of student transcripts provided by the university. Using Label Studio, we annotate these transcripts by creating bounding boxes for text and saving the annotations as JSON files.
Label Studio link 
```bash
 https://labelstud.io/
```
![Annotation]([image-path](https://github.com/phadkep/OCR/blob/main/Documents/Annotation.png))



# How to run?
### STEPS:

Clone the repository

```bash
https://github.com/phadkep/OCR.git
```
### STEP 01- Create a conda environment after opening the repository

```bash
conda create -n ocr python=3.8 -y
```

```bash
conda activate ocr
```


### STEP 02- Run below Commands
```bash
pip install paddlepaddle-gpu==2.3.0.post110 -f https://www.paddlepaddle.org.cn/whl/linux/mkl/avx/stable.html

pip install pdf2image

apt-get update

apt-get install poppler-utils

pip install "paddleocr>=2.0.1"

pip install protobuf==3.20.0

wget https://paddleocr.bj.bcebos.com/whl/layoutparser-0.0.0-py3-none-any.whl

pip install -U layoutparser-0.0.0-py3-none-any.whl

apt-get update

apt-get install libgomp1

pip install paddlepaddle

pip install paddleocr

pip install paddleclas

pip install tensorflow

pip install numpy
```


```bash
# Setup
In “app.py”, UPLOAD_FOLDER= '/Users/payal/Downloads/capstone/Modular' Here gives your directory path.
```

```bash
# Finally run the following command
python app.py
```
