import cv2
from shapedetector import Shape, ShapeDetector
import numpy as np
import SailGenerator


def main(body):
    font = cv2.FONT_HERSHEY_COMPLEX
    kernel = np.ones((5, 5), np.uint8)
    # b = open("/Users/michael.kochubeevsky/repo/documenthackathon/interface/IMG-1969.jpg", "rb")
    file_bytes = np.asarray(bytearray(body.read()), dtype=np.uint8)
   
    image = cv2.imdecode(file_bytes, cv2.IMREAD_UNCHANGED)

    dst = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
    bg = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)

    retval, threshold = cv2.threshold(bg, 90, 255, cv2.THRESH_BINARY)
    letsee = cv2.GaussianBlur(threshold, (3,3), cv2.BORDER_DEFAULT)

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
    b = open("/Users/sam.sloate/repo/documenthackathon/interface/flask/IMG_20191024_175610.jpg", "rb")

    main(b)
