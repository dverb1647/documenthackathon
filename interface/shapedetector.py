import cv2


class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c, hierarchy, cnts):
        # initialize the shape name and approximate the contour
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        # if the shape is a triangle, it will have 3 vertices
        if len(approx) == 3:
            shape = "triangle"

        # if the shape has 4 vertices, it is either a square or
        # a rectangle
        elif len(approx) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)

            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"

        # if the shape is a pentagon, it will have 5 vertices
        elif len(approx) == 5:
            shape = "pentagon"

        # otherwise, we assume the shape is a circle
        elif len(approx) > 5:
            shape = "circle"
        else:
            shape = None

        # return the name of the shape
        return Shape(approx, hierarchy, shape, cnts)


class Shape:
    def __init__(self, approx, hierarchy, shape, cnts):
        self.approx = approx
        self.hierarchy = hierarchy
        self.shape = shape
        self.cnts = cnts

    def __str__(self):
        return "approx: " + str(self.approx) + "\nhierarchy: " + str(self.hierarchy) + "\nshape: " + self.shape

    def getSailType(self):
        if self.shape == "rectangle" or self.shape == "square":
            parent = self.hierarchy[3]
            first_child = self.hierarchy[2]
            if parent == -1 or parent == 0:
                # We care about this
                if self.getArea() < 100:
                    return None
                if first_child != -1:  # If there are any children.
                    h = self.cnts[1][0][first_child]
                    if h[0] != -1:  # IF there are no siblings to the child (if the inner countour is the only child)
                        return "GRID"
                    # Some math on the size of the square
                    # Check the size here
                    return self.getTextFieldType()
                return self.getTextFieldType()
        elif self.shape == "circle":
            parent = self.hierarchy[3]
            if self.getArea() > 150 and (parent == -1 or parent == 0):
                return "PIECHART"
            return None
        else:  # Currently ignore any nested boxes
            return None

    def getArea(self):
        return (self.getMaxX() - self.getMinX()) * (self.getMaxY() - self.getMinY())

    def getTextFieldType(self):
        if self.getMaxY() - self.getMinY() > (1200 / 1200 * 300):  # Compare height, heuristic is 300 can be tweaked
            return "PARAGRAPH"
        return "TEXT"

    def getMinY(self):
        return min(point[0][1] for point in self.approx)

    def getMaxY(self):
        return max(point[0][1] for point in self.approx)

    def getMinX(self):
        return min(point[0][0] for point in self.approx)

    def getMaxX(self):
        return max(point[0][0] for point in self.approx)

    def to_sail_expression(self):
        type = self.getSailType()
        if type == "TEXT":
            return """a!textField(
            label: "Text",
            labelPosition: "ABOVE",
            saveInto: {},
            refreshAfter: "UNFOCUS",
            validations: {}
          )"""
        if type == "PARAGRAPH":
            return """a!paragraphField(
            label: "Paragraph",
            labelPosition: "ABOVE",
            saveInto: {},
            refreshAfter: "UNFOCUS",
            height: "MEDIUM",
            validations: {}
          )"""
        if type == "PIECHART":
            return """a!pieChartField(
    label: "Pie Chart",
    labelPosition: "ABOVE",
    series: {
      a!chartSeries(label: "Chart Series 1", data: 1),
      a!chartSeries(label: "Chart Series 2", data: 2),
      a!chartSeries(label: "Chart Series 3", data: 3)
    },
    showDataLabels: true
  )"""
        if type == 'GRID':
            return """a!localVariables(
    local!data: {
      {
        customer: "Disney",
        status: "Happy"
      },
      {
        customer: "S&P",
        status: "Super Happy"
      }
    },
  a!gridField(
    label: "Customers",
    labelPosition: "ABOVE",
    data: local!data,
    pagesize: 10,
    columns: {
      a!gridColumn(
        label: "Customer",
        value: fv!row.customer
      ),
      a!gridColumn(
        label: "Status",
        value: fv!row.status
      ),
    },
    validations: {}
  )
  )"""
        return None
