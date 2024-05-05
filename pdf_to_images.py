from pdf2image import convert_from_path
import cv2
import layoutparser as lp

def pdf_to_images(pdf_path, output_folder):
    print("\n Loading PDF: {}\n".format(pdf_path))
    images = convert_from_path(pdf_path)

    print("\n Converting PDF to images \n")
    for i, image in enumerate(images):
        image_path = "{}/page{}.jpg".format(output_folder, i)
        image.save(image_path, 'JPEG')
        print("Image saved: {}".format(image_path))