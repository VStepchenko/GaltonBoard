from manim import *
import random

class GaltonBoard(Scene):

    config = {
        "runTime": 16,
        "itemsTotal" : 200,
        "itemDelayFrames" : 1,
        "hexSize" : .2,
        "hexVerticalShift" : .6,
        "hexGorizontalShift" : .4,
        "hexRowsCount" : 7,
        "firstHexCenterX" : -3,
        "firstHexCenterY" : 3,
        "durationSeconds" : 2,
        "circleRadius" : .05,
        "firstDot" : [-3, 4.3, 0]
        }
    
    frameNumber = 0

    def construct(self):
        
        # uncomment to show dots on the plain every 1 point in both directions.
        # also pass (True) to show axes and (False) without axes
        #self.showDotMap(False)

        table = self.createTable()
        counter = self.createCounter()
        hexagons = self.createHexagons()
        vertices = self.createVertices()
        items = self.createItems(vertices)

        def updateFrameFunction(table):
            durationSeconds = GaltonBoard.config["durationSeconds"]
            durationFrames = durationSeconds * self.camera.frame_rate
            self.frameNumber += 1

            for item in items:
                if item.isActive and self.frameNumber > item.startFrame:
                    alpha = (self.frameNumber - item.startFrame) / durationFrames
                    if (alpha <= 1.0) :
                        point = item.path.point_from_proportion(rate_functions.linear(alpha))
                        item.circle.move_to(point)     
                    else:
                        updateCounter()
                        updateStackValue(item.stackIndex)
                        item.isActive = False


        def updateCounter():
            val = counter[0].get_value()
            val += 1
            counter[0].set_value(val)

        def updateStackValue(stackValueIndex):
            cell = table.get_entries((1, stackValueIndex + 1))
            val = cell.get_value()
            val += 1
            cell.set_value(val)

        self.play(FadeIn(hexagons, run_time = 1))
        self.play(FadeIn(table, run_time = 1))
        self.play(FadeIn(counter, run_time = 1))

        #group = VGroup(hexagons, table, counter)
        #self.play(FadeIn(group, run_time = 1))

        # we need pass to the UpdateFromFunc the special object that should be updated every frame
        # without it where will (under some unpredictable conditions) be problems with animation
        wrapper = VGroup(table, counter)
        for item in items:
            wrapper.add(item.circle)

        runTime = GaltonBoard.config["runTime"]
        self.play(UpdateFromFunc(wrapper, updateFrameFunction), run_time=runTime)

        self.wait(3)

    def createTable(self):
        table = IntegerTable(
            [[0, 0, 0, 0, 0, 0, 0, 0],],
            line_config={"stroke_width": 1, "color": YELLOW},
            include_outer_lines=False
            )
        table.scale(.5)
        table.shift(DOWN * 3.7).shift(LEFT * 3)

        return table
    
    def createCounter(self):
        counter = Integer(0).shift(RIGHT * 4).shift(DOWN * .6)
        text = Text('Items count:', font_size = 28)
        text.next_to(counter, LEFT)

        return VGroup(counter, text)   
    
    def createHexagons(self):
        rows = GaltonBoard.config["hexRowsCount"]
        hexSize = GaltonBoard.config["hexSize"]
        hexVerticalShift = GaltonBoard.config["hexVerticalShift"]
        hexGorizontalShift = GaltonBoard.config["hexGorizontalShift"]
        firstHexCenterX = GaltonBoard.config["firstHexCenterX"]
        firstHexCenterY = GaltonBoard.config["firstHexCenterY"]

        hexagons = VGroup()

        for row in range(rows):
            currentRowShiftUp = (firstHexCenterY - row * hexVerticalShift)
            currentRowShiftRight = (firstHexCenterX - row * hexGorizontalShift)
            for elem in range(row + 1):
                elemShiftRight = currentRowShiftRight + (elem * hexGorizontalShift) * 2
                tmp = RegularPolygon(n=6, radius = hexSize, start_angle = .5)
                # uncomment the following lines to get triangles of circles instead of hexagons
                #tmp = RegularPolygon(n=3, radius = hexSize)
                #tmp = Circle(radius = hexSize)
                tmp.shift(UP * currentRowShiftUp)
                tmp.shift(RIGHT * elemShiftRight)
                hexagons.add(tmp)

        return hexagons
    
    def createVertices(self):
        rows = GaltonBoard.config["hexRowsCount"]
        hexSize = GaltonBoard.config["hexSize"]
        hexVerticalShift = GaltonBoard.config["hexVerticalShift"]
        hexGorizontalShift = GaltonBoard.config["hexGorizontalShift"]
        firstHexCenterX = GaltonBoard.config["firstHexCenterX"]
        firstHexCenterY = GaltonBoard.config["firstHexCenterY"]

        vertices = [[None for i in range(rows + 1)] for j in range(rows + 1)]

        for row in range(rows + 1):
            currentRowShiftUp = (firstHexCenterY - row * hexVerticalShift)
            currentRowShiftRight = (firstHexCenterX - row * hexGorizontalShift)
            for elem in range(row + 1):
                elemShiftRight = currentRowShiftRight + (elem * hexGorizontalShift) * 2
                vertices[row][elem] = [elemShiftRight, currentRowShiftUp + hexSize + .1, 0]

        # uncomment to show all the vertices
        #for row in range(rows + 1):
        #    for col in range(rows + 1):
        #        tmp = vertices[row][col]
        #        if tmp is not None:
        #            t = Dot(tmp, radius=.05)
        #            self.add(t)

        return vertices
    
    def createItems(self, vertices):

        itemsTotal = GaltonBoard.config["itemsTotal"]
        circleRadius = GaltonBoard.config["circleRadius"]
        itemDelayFrames = GaltonBoard.config["itemDelayFrames"]
        firstDot = GaltonBoard.config["firstDot"]

        items = []
        startFrame = 0
        stackValues = [0, 0, 0, 0, 0, 0, 0, 0]

        for k in range (itemsTotal):
            item = Item()
            circle = Circle(radius=circleRadius, color=GREEN, fill_opacity=1)
            pathIndex = self.createPathIndex()
            stackIndex = pathIndex.bit_count()
            stackValues[stackIndex] += 1

            path = self.createPath(vertices, pathIndex, stackValues[stackIndex])

            item.path = path
            item.circle = circle
            item.stackIndex = stackIndex
            item.startFrame = startFrame
            
            startFrame += itemDelayFrames

            self.add(circle)
            circle.move_to(firstDot)

            items.append(item)

            # uncomment to show the path
            #self.add(path)

        return items  

    def createPathIndex(self):
        pathIndex = random.randrange(128)
        return pathIndex
    
        # the following code shows how to change probability 
        # to 1/3 for left and 2/3 for right directions
        pathIndex = 0
        for x in range(0, 7):
            tmp = random.randrange(3)
            if (tmp == 0):
                pathIndex += (2 ** x) * tmp
            if (tmp > 0):
                pathIndex += (2 ** x) * 1
        return pathIndex

    def createPath(self, vertices, pathIndex, itemsCountInStack):

        firstDot = GaltonBoard.config["firstDot"]
        rowCapacity = 3

        lastDotRowIndex = (itemsCountInStack - 1) // rowCapacity
        lastDotColIndex = (itemsCountInStack - 1) % rowCapacity 
        
        path = Line(firstDot, vertices[0][0], stroke_width=1)
        previousDot = vertices[0][0]
        binary = bin(pathIndex)[2:].zfill(7)
        rowIndex = 1
        colIndex = 0
        for digit in binary:
            if digit == '0':
                pathTmp = ArcBetweenPoints(previousDot, vertices[rowIndex][colIndex], angle=PI/2, stroke_width=1)
                previousDot = vertices[rowIndex][colIndex]
            else:
                colIndex += 1
                pathTmp = ArcBetweenPoints(previousDot, vertices[rowIndex][colIndex], angle=-PI/2, stroke_width=1)
                previousDot = vertices[rowIndex][colIndex]
            path.append_vectorized_mobject(pathTmp)
            rowIndex += 1

        lastDotWidth = .1
        lastDotHeight = .1

        lastDotX = previousDot[0]
        
        if lastDotColIndex == 0:
            lastDotX = lastDotX - lastDotWidth
        elif lastDotColIndex == 2:
            lastDotX = lastDotX + lastDotWidth

        lastDotY = previousDot[1] - 2.4 + lastDotHeight * lastDotRowIndex

        pathLast = Line(previousDot, [lastDotX, lastDotY, 0] , stroke_width=1)
        path.append_vectorized_mobject(pathLast)

        return path           


    def showDotMap(self, showAxes):
        for x in range(-7, 8):
            for y in range(-4, 5):
                dot = Dot(np.array([x, y, 0]), radius=0.02)
                self.add(dot) 

        if (showAxes):
            ax = Axes(x_range=[-7, 7], y_range=[-4, 4], x_length=14, y_length=8)
            self.add(ax)

class Item:
    circle = None
    path = None
    startFrame = 0
    stackIndex = 0
    isActive = True
    