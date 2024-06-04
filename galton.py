from manim import *
import random

class GaltonBoard(Scene):

    config = {
        "runTime": 5,
        "itemsTotal" : 150,
        "itemDelayFrames" : 2,
        "hexSize" : .2,
        "hexVerticalShift" : .6,
        "hexGorizontalShift" : .4,
        "hexRowsCount" : 7,
        "firstHexCenterX" : -3,
        "firstHexCenterY" : 3,
        "durationSeconds" : 2,
        "circleRadius" : .05
        }

    def construct(self):
        
        def updateFrameFunction(table):
            #updateCounter()
            #updateStackValue(1)
            durationSeconds = GaltonBoard.config["durationSeconds"]
            durationFrames = durationSeconds * self.camera.frame_rate

        def updateCounter():
            val = counter[0].get_value()
            val += 1
            counter[0].set_value(val)

        def updateStackValue(stackValueIndex):
            cell = table.get_entries((1, stackValueIndex + 1))
            val = cell.get_value()
            val += 1
            cell.set_value(val)

        table = self.createTable()
        counter = self.createCounter()
        hexagons = self.createHexagons()
        items = self.createItems()

        #print(self.camera.frame_rate)
        self.play(FadeIn(hexagons, run_time = 1))
        self.play(FadeIn(table, run_time = 1))
        self.play(FadeIn(counter, run_time = 1))

        self.play(UpdateFromFunc(table, updateFrameFunction), run_time=3)

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
                tmp = RegularPolygon(radius = hexSize, start_angle = .5)
                tmp.shift(UP * currentRowShiftUp)
                tmp.shift(RIGHT * elemShiftRight)
                hexagons.add(tmp)

        return hexagons
    
    def createItems(self):
        items = []
        #itemsTotal = GaltonBoard.config["itemsTotal"]
        #circleRadius = GaltonBoard.config["circleRadius"]
        #item = Item()
        #circle = Circle(radius=.05, color=GREEN, fill_opacity=1)

        return items   

class Item:
    circle = None
    path = None
    startFrame = 0
    stackIndex = 0
    isActive = True