import math
from PIL import Image, ImageDraw, ImageFont
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap
import face_recognition
import face_recognition

# Image for opening
nameImage = "C:\\Users\\Nika Kim\\Desktop\\faces\\K.jpg"


def find_red_pixel(image_name):
    # Set the value you want for these variables
    r_min = 255
    g_min = 0
    b_min = 0

    red_pixels = set()

    img = image_name
    img = Image.open(image_name)
    rgb = img.convert('RGB')
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            r, g, b = rgb.getpixel((x, y))
            if r == r_min and b == b_min and g == g_min:
                red_pixels.add((x, y))

    return red_pixels


# Load the jpg file into a numpy array
image = face_recognition.load_image_file(nameImage)

# Find all facial features in all the faces in the image
face_landmarks_list = face_recognition.face_landmarks(image)

pil_image = Image.fromarray(image)


def analys(imageForAnalys):

    red_pixels = set()
    red_pixels = find_red_pixel(imageForAnalys)
    redPoint = red_pixels.pop()

    #find_red_pixel(image)
    print("red: ", len(red_pixels))


    # Make the eyebrows into a nightmare

    var = face_landmarks['right_eye']

    print('left', var)
    print('right', face_landmarks['right_eye'])
    print('left', face_landmarks['left_eye'])
    print('noise', face_landmarks['nose'])
    print('border', face_landmarks['border'])
    print('lips middle', face_landmarks['lips_middle'])

    betweenEyes = face_landmarks['right_eye'][0][0] - face_landmarks['left_eye'][3][0]
    leftEyeLength = face_landmarks['left_eye'][3][0] - face_landmarks['left_eye'][0][0]
    rightEyeLength = face_landmarks['right_eye'][3][0] - face_landmarks['right_eye'][0][0]
    noseLength = face_landmarks['nose'][4][1] - face_landmarks['right_eye'][0][1]
    faceLengthWithoutForehead = face_landmarks['border'][1][1] - face_landmarks['border'][0][1]
    fromChinToLips = face_landmarks['border'][1][1] - face_landmarks['lips_middle'][0][1]
    meanEyebrowBegining = (face_landmarks['left_eyebrow'][4][1] + face_landmarks['right_eyebrow'][0][1])/2

    forehead = meanEyebrowBegining - redPoint[1]
    allFace = face_landmarks['chin'][8][1] - red_pixels.pop()[1]

    print("----------------------------------------------------------------------------\n")

    print("Length of eyes", betweenEyes)
    print("Length of left eye", leftEyeLength)
    print("Length of right eye", rightEyeLength)
    print("Length of nose", noseLength)
    print("Length face without forehead", faceLengthWithoutForehead)
    print("Length from chin to lips", fromChinToLips)

    print("----------------------------------------------------------------------------\n")

    # ------------------------- lips -------------------------

    devLips = fromChinToLips - faceLengthWithoutForehead / 3
    deltaLips: float
    kLips: float = 1

    if math.fabs(devLips) < 0.05 * fromChinToLips:
        deltaLips = 0.2
    elif math.fabs(devLips) < 0.10 * fromChinToLips:
        deltaLips = 0.3
    elif math.fabs(devLips) < 0.15 * fromChinToLips:
        deltaLips = 0.4
    elif math.fabs(devLips) < 0.2 * fromChinToLips:
        deltaLips = 0.5
    else:
        deltaLips = 0

    kLips += deltaLips if devLips > 0 else -deltaLips

    print("k lips: ", kLips)

    #print("dev from ideal lips: ", devLips)


    # ------------------------- nose -------------------------

    devNose = noseLength - faceLengthWithoutForehead / 3
    deltaNose: float
    kNose: float = 1

    if (math.fabs(devNose) > 0.05 * noseLength) & (math.fabs(devNose) < 0.1 * noseLength):
        deltaNose = 0.3
    elif math.fabs(devNose) < 0.15 * noseLength:
        deltaNose = 0.4
    elif math.fabs(devNose) < 0.2 * noseLength:
        deltaNose = 0.5
    elif math.fabs(devNose) < 0.3 * noseLength:
        deltaNose = 0.8
    else:
        deltaNose = 0

    kNose += deltaNose if devNose < 0 else -deltaNose

    print("k nose: ", kNose)

    #print("dev from ideal nose: ", devNose)

    # ------------------------- eyes -------------------------

    eyeLength = 1.5 * (rightEyeLength+leftEyeLength)/2
    devEyes = betweenEyes - eyeLength
    deltaEyes: float
    kEyes: float = 1

    if (math.fabs(devEyes) > 0.005 * eyeLength) & (math.fabs(devEyes) < 0.05 * eyeLength):
        deltaEyes = 0.3
    elif math.fabs(devEyes) < 0.05 * eyeLength:
        deltaEyes = 0.5
    elif math.fabs(devEyes) < 0.15 * eyeLength:
        deltaEyes = 0.6
    elif math.fabs(devEyes) < 0.2 * eyeLength:
        deltaEyes = 0.8
    else:
        deltaEyes = 0

    kEyes += deltaEyes if devEyes > 0 else -deltaEyes

    print("k eyes: ", kEyes)


    # ------------------------- forehead -------------------------

    idealForehead = allFace/3
    devForehead = forehead - idealForehead
    deltaForehead: float
    kForehead: float = 1

    if (math.fabs(devForehead) > 0.1 * idealForehead) & (math.fabs(devForehead) < 0.25 * idealForehead):
        deltaForehead = 0.3
    elif math.fabs(devForehead) < 0.33 * idealForehead:
        deltaForehead = 0.5
    elif math.fabs(devForehead) < 0.5 * idealForehead:
        deltaForehead = 0.75
    else:
        deltaForehead = 0

    kForehead += deltaForehead if devForehead > 0 else -deltaForehead

    print("k forehead: ", kForehead)

    k = 0.34*kLips + 0.22*(kNose + kEyes + kForehead)

    # Show lines of values on face
    d = ImageDraw.Draw(pil_image, 'RGBA')

    im = Image.open(nameImage)
    (width, height) = im.size

    print(width)

    if(width < 600 or height < 600):
        lineWidth = 2
        ellipsRad = 1
    elif(width < 1000 or height < 1000):
        lineWidth = 5
        ellipsRad = 5
    else:
        lineWidth = 8
        ellipsRad = 10

    # Eyes
    d.line([(face_landmarks['left_eye'][3][0], face_landmarks['left_eye'][3][1]),
            (face_landmarks['right_eye'][0][0], face_landmarks['right_eye'][0][1])],
            fill=(150, 0, 0, 64), width=lineWidth)

    d.ellipse((face_landmarks['left_eye'][3][0] - ellipsRad, face_landmarks['left_eye'][3][1] - ellipsRad,
               face_landmarks['left_eye'][3][0] + ellipsRad, face_landmarks['left_eye'][3][1] + ellipsRad),
               fill="red", outline="red")

    d.ellipse((face_landmarks['right_eye'][0][0] - ellipsRad, face_landmarks['right_eye'][0][1] - ellipsRad,
               face_landmarks['right_eye'][0][0] + ellipsRad, face_landmarks['right_eye'][0][1] + ellipsRad),
               fill="red", outline="red")

    # Forehead
    d.line([(face_landmarks['nose'][0][0], redPoint[1]), (face_landmarks['nose'][0][0], face_landmarks['nose'][0][1])],
           fill=(150, 0, 0, 64), width=lineWidth)

    d.ellipse((face_landmarks['nose'][0][0] - ellipsRad, redPoint[1] - ellipsRad,
               face_landmarks['nose'][0][0] + ellipsRad, redPoint[1] + ellipsRad),
              fill="red", outline="red")

    d.ellipse((face_landmarks['nose'][0][0] - ellipsRad, face_landmarks['nose'][0][1] - ellipsRad,
               face_landmarks['nose'][0][0] + ellipsRad, face_landmarks['nose'][0][1] + ellipsRad),
              fill="red", outline="red")

    # Nose
    d.line([(face_landmarks['nose'][0][0], face_landmarks['nose'][0][1]),
            (face_landmarks['nose'][0][0], face_landmarks['nose_tip'][3][1])],
           fill=(150, 0, 0, 64), width=lineWidth)

    d.ellipse((face_landmarks['nose'][0][0] - ellipsRad, face_landmarks['nose_tip'][3][1] - ellipsRad,
               face_landmarks['nose'][0][0] + ellipsRad, face_landmarks['nose_tip'][3][1] + ellipsRad), fill="red", outline="red")

    # Cheekbones
    d.line([(face_landmarks['cheekbones'][0][0], face_landmarks['cheekbones'][0][1]),
            (face_landmarks['cheekbones'][1][0], face_landmarks['cheekbones'][0][1])],
           fill=(150, 0, 0, 64), width=lineWidth)

    d.ellipse((face_landmarks['cheekbones'][0][0] - ellipsRad, face_landmarks['cheekbones'][0][1] - ellipsRad,
               face_landmarks['cheekbones'][0][0] + ellipsRad, face_landmarks['cheekbones'][0][1] + ellipsRad),
              fill="red", outline="red")

    d.ellipse((face_landmarks['cheekbones'][1][0] - ellipsRad, face_landmarks['cheekbones'][0][1] - ellipsRad,
               face_landmarks['cheekbones'][1][0] + ellipsRad, face_landmarks['cheekbones'][0][1] + ellipsRad),
              fill="red", outline="red")

    # Lips
    d.line([(face_landmarks['nose'][0][0], face_landmarks['lips_middle'][0][1]),
            (face_landmarks['nose'][0][0], face_landmarks['border'][1][1])],
           fill=(150, 0, 0, 64), width=lineWidth)

    d.ellipse((face_landmarks['nose'][0][0] - ellipsRad, face_landmarks['lips_middle'][0][1] - ellipsRad,
               face_landmarks['nose'][0][0] + ellipsRad, face_landmarks['lips_middle'][0][1] + ellipsRad),
              fill="red", outline="red")

    d.ellipse((face_landmarks['nose'][0][0] - ellipsRad, face_landmarks['border'][1][1] - ellipsRad,
               face_landmarks['nose'][0][0] + ellipsRad, face_landmarks['border'][1][1] + ellipsRad),
              fill="red", outline="red")

    # All length

    d.line([(face_landmarks['nose'][0][0] + lineWidth*3, redPoint[1]),
            (face_landmarks['nose'][0][0] + lineWidth*3, face_landmarks['border'][1][1])],
           fill=(150, 0, 0, 64), width=lineWidth)

    d.ellipse((face_landmarks['nose'][0][0] - ellipsRad, redPoint[1] - ellipsRad,
               face_landmarks['nose'][0][0] + ellipsRad, redPoint[1] + ellipsRad),
              fill="red", outline="red")

    d.ellipse((face_landmarks['nose'][0][0] + lineWidth*3 - ellipsRad, face_landmarks['border'][1][1] - ellipsRad,
               face_landmarks['nose'][0][0] + lineWidth*3 + ellipsRad, face_landmarks['border'][1][1] + ellipsRad),
              fill="red", outline="red")

    if (k < 0.9):
        result = "Согласно лицевым конфигурационным эффектам Брунсвика, данное лицо соответствует графической схеме, вызывающей СИЛЬНОЕ ВПЕЧАТЛЕНИЕ ЭКСПРЕССИИ ГРУСТИ "
    elif(0.9 < k < 0.95):
        result = "Согласно лицевым конфигурационным эффектам Брунсвика, данное лицо соответствует графической схеме, вызывающей УМЕРЕННОЕ ВПЕЧАТЛЕНИЕ ЭКСПРЕССИИ ГРУСТИ "
    elif (0.95 < k < 1.05):
        result = "Согласно лицевым конфигурационным эффектам Брунсвика, данное лицо соответствует графической схеме, вызывающей ВПЕЧАТЛЕНИЕ ЭКСПРЕССИВНО НЕЙТРАЛЬНОГО ЛИЦА "
    elif (1.05 < k < 1.15):
        result = "Согласно лицевым конфигурационным эффектам Брунсвика, данное лицо соответствует графической схеме, вызывающей УМЕРЕННОЕ ВПЕЧАТЛЕНИЕ ЭКСПРЕССИИ РАДОСТИ "
    elif (k > 1.15):
        result = "Согласно лицевым конфигурационным эффектам Брунсвика, данное лицо соответствует графической схеме, вызывающей СИЛЬНОЕ ВПЕЧАТЛЕНИЕ ЭКСПРЕССИИ РАДОСТИ "
    else:
        result = "Hard to determine"

    print("k: ", k)
    print("Результат: ", result)

    #print("dev from ideal eyes: ", devEyes)

    pil_image.show()



class Widget(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle('Analyser')

        self.point = None

        hbox = QVBoxLayout(self)
        pixmap = QPixmap(nameImage)

        self.lbl = QLabel(self)
        self.lbl.setPixmap(pixmap)

        hbox.addWidget(self.lbl)
        self.setLayout(hbox)

        btn1 = QPushButton("Готово", self)
        hbox.addWidget(btn1)
        btn2 = QPushButton("Очистить", self)
        hbox.addWidget(btn2)


        btn1.clicked.connect(self.button1Clicked)
        btn2.clicked.connect(self.button2Clicked)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()

    def drawText(self, event, qp):
        qp.setPen(QColor(168, 34, 3))
        qp.setFont(QFont('Decorative', 10))
        qp.drawText(event.rect(), Qt.AlignCenter, self.text)

    def button1Clicked(self):
        newName = "C:\\Users\\Nika Kim\\Desktop\\faces\\K.png"
        self.lbl.pixmap().save(newName, 'png')
        analys(newName)
        self.close()

    def button2Clicked(self):
        pixmap = QPixmap(nameImage)
        self.lbl.setPixmap(pixmap)


    def mousePressEvent(self, event):

        self.point = event.pos()

        # Вызов перерисовки виджета
        self.update()


    def mouseReleaseEvent(self, event):

        self.point = None


    def paintEvent(self, event):

        super().paintEvent(event)

        # Если нет
        if not self.point:
            return

        painter = QPainter(self.lbl.pixmap())
        painter.setPen(QPen(Qt.red, 10.0))
        painter.drawPoint(self.point)



for face_landmarks in face_landmarks_list:

    app = QApplication(sys.argv)
    ex = Widget()
    ex.show()
    sys.exit(app.exec_())

