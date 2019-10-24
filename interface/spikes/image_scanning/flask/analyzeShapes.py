import cv2
import imutils
from shapedetector import Shape, ShapeDetector

def main():
    font = cv2.FONT_HERSHEY_COMPLEX

    # load the image
    image = cv2.imread("/Users/sam.sloate/repo/image_scanning/data/IMG-1967.JPG")


    # convert the image to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = errosion(image)
    image = resizeImage(image)
    # ret, thresh = cv2.threshold(image,220,255,1)
    thresh = cv2.adaptiveThreshold(image, 70, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # find contours in the thresholded image
    cnts = cv2.findContours(thresh, cv2.RETR_TREE,
                            cv2.CHAIN_APPROX_SIMPLE)
    cv2.imshow()
    sd = ShapeDetector()
    #
    # print(len(cnts[0]))
    # print(len(cnts[1][0]))
    # print("**********")
    shapes = []
    for i in range(len(cnts[0])):

        c = cnts[0][i]
        h = cnts[1][0][i]
        # compute the center of the contour, then detect the name of the
        # shape using only the contour
        shape = sd.detect(c, h, cnts)

        # print(shape.getSailType())
        if shape.getSailType():
            shapes.append(shape)
        # print(approx)

    shapes.sort(key=lambda s:s.getMinY())
    print([shape.getSailType() for shape in shapes])

    # identify all intersecting groups
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

    print(groups)

    # identify all valid columns within each subgroup

def dilation(cv2_img, kernel_size=3, num_itr=1):
    #        kernel = np.ones((kernel_size, kernel_size), np.uint8)
    kernel = cv2.getStructuringElement(
        cv2.MORPH_CROSS, (kernel_size, kernel_size))
    cv2_img = cv2.dilate(cv2_img, kernel, iterations=num_itr)
    return cv2_img

def errosion(cv2_img, kernel_size=3, num_itr=1):
    #        kernel = np.ones((kernel_size, kernel_size), np.uint8)
    kernel = cv2.getStructuringElement(
        cv2.MORPH_CROSS, (kernel_size, kernel_size))
    cv2_img = cv2.erode(cv2_img, kernel, iterations=num_itr)
    return cv2_img

def resizeImage(cv2_img, factor=2):
    return cv2.resize(cv2_img, None, fx=factor, fy=factor, interpolation=cv2.INTER_CUBIC)


if __name__ == "__main__":
    main()
