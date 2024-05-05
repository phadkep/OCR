import cv2
import layoutparser as lp
from paddleocr import PaddleOCR

def detect_layout_and_ocr(image_path, det_model_dir, rec_model_dir, cls_model_dir):
    image = cv2.imread(image_path)
    image = image[..., ::-1]

    print("\n # load model\n")
    model = lp.PaddleDetectionLayoutModel(config_path="lp://PubLayNet/ppyolov2_r50vd_dcn_365e_publaynet/config",
                                    threshold=0.5,
                                    label_map={0: "Text", 1: "Title", 2: "List", 3:"Table", 4:"Figure"},
                                    enforce_cpu=False,
                                    enable_mkldnn=True)#math kernel library
    print("\n # detect\n")
    layout = model.detect(image)
    print(layout)


    print("\n ## Detect and Recognize full page\n")
    first_text_block = layout._blocks[0]
    block = first_text_block.block
    x_1 = block.x_1
    x_2 = block.x_2
    y_1 = block.y_1
    y_2 = block.y_2

    for l in layout:
        if l.type == 'Table':
            x_1 = int(l.block.x_1)
            print(l.block.x_1)
            y_1 = int(l.block.y_1)
            x_2 = int(l.block.x_2)
            y_2 = int(l.block.y_2)
            break

    im = cv2.imread(image_path)
    cropped_image = im[int(y_1):int(y_2), int(x_1):int(x_2)]
    try:
        cv2.imwrite('/Users/payal/Downloads/capstone/Modular/Images/ext_im_full.jpg', cropped_image)
        print("Image saved successfully!")
    except Exception as e:
        print(f"Error saving image: {e}")

    print("\n # Load the detection, recognition, and classification models \n")
    ocr = PaddleOCR(lang='en', det_model_dir=det_model_dir, rec_model_dir=rec_model_dir, cls_model_dir=cls_model_dir)
    full_img = 'Images/ext_im_full.jpg'

    print("\n # Perform OCR on the cropped image \n")
    image_cv = cv2.imread(full_img)
    image_height = image_cv.shape[0]
    image_width = image_cv.shape[1]
    full_output = ocr.ocr(full_img)[0]

    return full_output