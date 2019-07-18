
from PIL import Image, ImageDraw, ImageFont
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap
import face_recognition

# Image for opening
nameImage = "C:\\Users\\Nika Kim\\Desktop\\faces\\Без названия.jpg"

# Load the png file into a numpy array
image = face_recognition.load_image_file(nameImage)

# Find all facial features in all the faces in the image
face_landmarks_list = face_recognition.face_landmarks(image)

pil_image = Image.fromarray(image)


def find_red_pixel(image_name):

    # Set the value you want for these variables
    r_min = 255
    g_min = 0
    b_min = 0

    pixels = set()

    img = Image.open(image_name)
    rgb = img.convert('RGB')
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            r, g, b = rgb.getpixel((x, y))
            if r == r_min and b == b_min and g == g_min:
                pixels.add((x, y))

    return pixels


def analys(imageForAnalys):

    # Find red point
    red_pixels = set()
    red_pixels = find_red_pixel(imageForAnalys)

    if len(red_pixels) == 0:
        print("ERROR: PUT RED POINT IN THE FOREHEAD")

    redPoint = red_pixels.pop()

    print('left', face_landmarks['right_eye'])
    print('right', face_landmarks['right_eye'])
    print('left', face_landmarks['left_eye'])
    print('noise', face_landmarks['nose'])
    print('border', face_landmarks['border'])
    print('lips middle', face_landmarks['lips_middle'])

    # Calculate main items
    betweenEyes = face_landmarks['right_eye'][0][0] - face_landmarks['left_eye'][3][0]
    leftEyeLength = face_landmarks['left_eye'][3][0] - face_landmarks['left_eye'][0][0]
    rightEyeLength = face_landmarks['right_eye'][3][0] - face_landmarks['right_eye'][0][0]
    eyeLength = 1.5 * (rightEyeLength + leftEyeLength) / 2
    noseLength = face_landmarks['nose'][4][1] - face_landmarks['right_eye'][0][1]
    faceLengthWithoutForehead = face_landmarks['border'][1][1] - face_landmarks['border'][0][1]
    fromChinToLips = face_landmarks['border'][1][1] - face_landmarks['lips_middle'][0][1]
    meanEyebrowBegining = (face_landmarks['left_eyebrow'][4][1] + face_landmarks['right_eyebrow'][0][1])/2
    forehead = meanEyebrowBegining - redPoint[1]
    allFace = face_landmarks['chin'][8][1] - red_pixels.pop()[1]
    cheekbones = face_landmarks['cheekbones'][1][0] - face_landmarks['cheekbones'][0][0]
    yPupil =  (face_landmarks['right_eye'][5][1] + face_landmarks['right_eye'][1][1])/2

    # Values
    pui = (betweenEyes + eyeLength)/cheekbones
    puti = (yPupil - redPoint[1])/allFace
    nsi = noseLength/allFace
    stoi = fromChinToLips/allFace


    # Show lines of values on face
    d = ImageDraw.Draw(pil_image, 'RGBA')

    im = Image.open(nameImage)
    (width, height) = im.size


    if (width < 600 or height < 600):
        lineWidth = 2
        ellipsRad = 1
    elif (width < 1000 or height < 1000):
        lineWidth = 5
        ellipsRad = 5
    else:
        lineWidth = 8
        ellipsRad = 10


    # Eyes
    d.line([(face_landmarks['left_eye'][3][0]-leftEyeLength/2, face_landmarks['left_eye'][3][1]),
            (face_landmarks['right_eye'][0][0]+rightEyeLength/2, face_landmarks['right_eye'][0][1])],
            fill=(150, 0, 0, 64), width=lineWidth)

    d.ellipse((face_landmarks['left_eye'][3][0]-leftEyeLength/2 - ellipsRad, face_landmarks['left_eye'][3][1] - ellipsRad,
               face_landmarks['left_eye'][3][0]-leftEyeLength/2 + ellipsRad, face_landmarks['left_eye'][3][1] + ellipsRad),
               fill="red", outline="red")

    d.ellipse((face_landmarks['right_eye'][0][0]+rightEyeLength/2 - ellipsRad, face_landmarks['right_eye'][0][1] - ellipsRad,
               face_landmarks['right_eye'][0][0]+rightEyeLength/2 + ellipsRad, face_landmarks['right_eye'][0][1] + ellipsRad),
               fill="red", outline="red")

    # font = ImageFont.truetype(<font-file>, <font-size>)
    # font = ImageFont.truetype("sans-serif.ttf", 16)
    # draw.text((x, y),"Sample Text",(r,g,b))


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
    d.line([(face_landmarks['nose'][0][0], face_landmarks['nose'][0][1]), (face_landmarks['nose'][0][0], face_landmarks['nose_tip'][3][1])],
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

    d.line([(face_landmarks['nose'][0][0] + lineWidth*3, redPoint[1]), (face_landmarks['nose'][0][0] + lineWidth*3, face_landmarks['border'][1][1])],
             fill=(150, 0, 0, 64), width=lineWidth)

    d.ellipse((face_landmarks['nose'][0][0] + lineWidth*3 - ellipsRad, redPoint[1] - ellipsRad,
               face_landmarks['nose'][0][0] + lineWidth*3 + ellipsRad, redPoint[1] + ellipsRad),
               fill="red", outline="red")

    d.ellipse((face_landmarks['nose'][0][0] + lineWidth*3 - ellipsRad, face_landmarks['border'][1][1] - ellipsRad,
               face_landmarks['nose'][0][0] + lineWidth*3 + ellipsRad, face_landmarks['border'][1][1] + ellipsRad),
               fill="red", outline="red")


    #d.line(face_landmarks['right_eye'] + [face_landmarks['right_eye'][0]], fill=(0, 0, 0, 110), width=6)

    print("----------------------------------------------------------------------------\n")

    print("Length of eyes ", betweenEyes)
    print("Length of left eye ", leftEyeLength)
    print("Length of right eye ", rightEyeLength)
    print("Length of nose ", noseLength)
    print("Length face without forehead ", faceLengthWithoutForehead)
    print("Length from chin to lips ", fromChinToLips)
    print("Mean eyebrow begining ", meanEyebrowBegining)
    print("Length of forehead ", forehead)
    print("Length of face ", allFace)
    print("Length of cheekbones  ", cheekbones)
    print("Pupil ", yPupil)

    print("pui: ", pui)
    print("puti: ", puti)
    print("nsi: ", nsi)
    print("stoi: ", stoi)

    print("----------------------------------------------------------------------------\n")

    interested = 0.357*nsi + 0.544/puti
    happy = 0.4*pui + 0.285*stoi + 0.409*puti
    impressed = 0.386*nsi + 0.432/puti
    sad = 0.356/pui + 0.423/stoi
    despised = 0.287/nsi
    scared = 0.499*nsi + 0.317/stoi + 0.495/puti
    guilty = 0.435*nsi +0.472/stoi

    print("interested: ", interested)
    print("happy: ", happy)
    print("impressed: ", impressed)
    print("sad: ", sad)
    print("despised: ", despised)
    print("scared: ", scared)
    print("guilty: ", guilty)

    interested0 = 0.357 * 0.33 + 0.544 / 0.33
    happy0 = 0.4 * 0.5 + 0.285 * 0.25 + 0.409 * 0.33
    impressed0 = 0.386 * 0.33 + 0.432 / 0.33
    sad0 = 0.356 / 0.5 + 0.423 / 0.25
    despised0 = 0.287 / 0.33
    scared0 = 0.499 * 0.33 + 0.317 / 0.25 + 0.495 / 0.33
    guilty0 = 0.435 * 0.33 + 0.472 / 0.25

    devInterested = 100 * (1 - interested/interested0)
    devHappy = 100 * (1 - happy/happy0)
    devImpressed = 100 * (1 - impressed/impressed0)
    devSad = 100 * (1 - sad/sad0)
    devDespised = 100 * (1 - despised/despised0)
    devScared = 100 * (1 - scared/scared0)
    devGuilty = 100 * (1 - guilty/guilty0)

    print("")
    print("devInterested: ", devInterested, "%")
    print("devHappy: ", devHappy, "%")
    print("devImpressed: ", devImpressed, "%")
    print("devSad: ", devSad, "%")
    print("devDespised: ", devDespised, "%")
    print("devScared: ", devScared, "%")
    print("devGuilty: ", devGuilty, "%")

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
        newName = "C:\\Users\\Nika Kim\\Desktop\\faces\\Без названия.png"
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
    analys()





