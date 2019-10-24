import cv2
from shapedetector import Shape, ShapeDetector
import numpy as np
import SailGenerator


def main(body):
    font = cv2.FONT_HERSHEY_COMPLEX
    kernel = np.ones((5, 5), np.uint8)
    file_bytes = np.asarray(bytearray(body), dtype=np.uint8)
   
    image = cv2.imdecode(file_bytes, cv2.IMREAD_UNCHANGED)
    # image = cv.fromarray(img_data_ndarray)
    # image = cv2.imread("/Users/sam.sloate/repo/image_scanning/data/IMG_20191024_175610.jpg")

    bg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    dst = cv2.fastNlMeansDenoising(bg, None, 10, 10, 7, 21)
    # scale_percent = 20  # percent of original size
    # width = dst.shape[1]
    # height = dst.shape[0]
    # width = int(width * scale_percent / 100)
    # height = int(height * scale_percent / 100)
    # dim = (width, height)
    #
    # resized = cv2.resize(dst, dim, interpolation=cv2.INTER_AREA) Slow but who cares
    retval, threshold = cv2.threshold(dst, 120, 255, cv2.THRESH_BINARY)
    letsee = cv2.GaussianBlur(threshold, (3,3), cv2.BORDER_DEFAULT)


    # cv2.imshow("hey", bg)
    # cv2.waitKey(0)
    cnts = cv2.findContours(letsee, cv2.RETR_TREE,
                            cv2.CHAIN_APPROX_SIMPLE)

    sd = ShapeDetector()
    shapes = []
    for i in range(1, len(cnts[0])):
        c = cnts[0][i]
        h = cnts[1][0][i]
        shape = sd.detect(c, h, cnts)

        if shape.getSailType():
            shapes.append(shape)

    shapes.sort(key=lambda s:s.getMinY())

    groups=[]
    #Assume nothing is emoty
    s1 = shapes[0]
    minY = s1.getMinY()
    maxY = s1.getMaxY()
    currGroup = [s1]
    for i in range(1, len(shapes)):
        currShape = shapes[i]
        if minY <= currShape.getMinY() <= maxY:
            currGroup.append(currShape)
        else:
            groups.append(currGroup)
            currGroup = [currShape]
        minY = currShape.getMinY()
        maxY = currShape.getMaxY()
    groups.append(currGroup)

    generatedSail = SailGenerator.generateSail(groups)
    print(generatedSail)
    return generatedSail


if __name__ == "__main__":
    main()
