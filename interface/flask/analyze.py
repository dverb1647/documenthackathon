from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.0/bin/tesseract'
print(pytesseract.image_to_boxes(Image.open('../data/IMG-1963.JPG')))

