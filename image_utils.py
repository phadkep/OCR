import cv2
import layoutparser as lp

def find_item(full_output):
    for i, item in enumerate(full_output):
        text = item[1][0].lower()  # Get the text string (case-insensitive)
        if 's.no.' in text:
            try:
                next_item = full_output[i+1]
                return next_item
            except IndexError:
                return None
        elif 'subject' in text:
            return item
    return None

def crop_and_save_image(full_output, image_path, output_path):
    image = cv2.imread(image_path)
    image = image[..., ::-1]

    print("\n # load model\n")
    model = lp.PaddleDetectionLayoutModel(config_path="lp://PubLayNet/ppyolov2_r50vd_dcn_365e_publaynet/config",
                                    threshold=0.5,
                                    label_map={0: "Text", 1: "Title", 2: "List", 3:"Table", 4:"Figure"},
                                    enforce_cpu=False,
                                    enable_mkldnn=True)#math kernel library


    layout = model.detect(image)
    result = find_item(full_output)

    x_1, y_1 = result[0][0]
    x_2 = 1500.663330078125
    y_2 = 1300.96630859375

    print(x_1, y_1, x_2, y_2)

    for l in layout:
        #print(l)
        if l.type == 'Table':
            x_1 = int(l.block.x_1)
            print(l.block.x_1)
            y_1 = int(l.block.y_1)
            x_2 = int(l.block.x_2)
            y_2 = int(l.block.y_2)

            break

    # Crop the image based on the coordinates
    cropped_image = image[int(y_1):int(y_2), int(x_1):int(x_2)]

    # Save the cropped image to a file
    cv2.imwrite(output_path, cropped_image)