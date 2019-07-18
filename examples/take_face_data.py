from PIL import Image, ImageDraw
import face_recognition

# Load the jpg file into a numpy array
image = face_recognition.load_image_file("C:\\Users\\Nika Kim\\Desktop\\8ymvX-zPmFs.jpg")

# Find all facial features in all the faces in the image
face_landmarks_list = face_recognition.face_landmarks(image)

pil_image = Image.fromarray(image)
for face_landmarks in face_landmarks_list:
    d = ImageDraw.Draw(pil_image, 'RGBA')

    # Make the eyebrows into a nightmare

    var = face_landmarks['right_eye']

    print('left', var)

    print('left', face_landmarks['right_eye'])
    print('left', face_landmarks['left_eye'])

    # print('')

    d.polygon(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 128))
    d.polygon(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 128))
    d.line(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 150), width=5)
    d.line(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 150), width=5)

    # Gloss the lips
    d.polygon(face_landmarks['top_lip'], fill=(150, 0, 0, 128))
    d.polygon(face_landmarks['bottom_lip'], fill=(150, 0, 0, 128))
    d.line(face_landmarks['top_lip'], fill=(150, 0, 0, 64), width=8)
    d.line(face_landmarks['bottom_lip'], fill=(150, 0, 0, 64), width=8)

    # Sparkle the eyes
    d.polygon(face_landmarks['left_eye'], fill=(255, 255, 255, 30))
    d.polygon(face_landmarks['right_eye'], fill=(255, 255, 255, 30))

    # Apply some eyeliner
    d.line(face_landmarks['left_eye'] + [face_landmarks['left_eye'][0]], fill=(0, 0, 0, 110), width=6)
    d.line(face_landmarks['right_eye'] + [face_landmarks['right_eye'][0]], fill=(0, 0, 0, 110), width=6)

    d.line(var, fill=(150, 0, 0, 128), width=5)

    betweenEyeBrows: object = face_landmarks['right_eyebrow'][0][0] - face_landmarks['left_eyebrow'].pop()[0]
    # betweenEyes = face_landmarks['right_eye'][0][0] - face_landmarks['left_eye'].pop()[0]

    eyesLength = face_landmarks['right_eye'][0][0] - face_landmarks['left_eye'][3][0]

    leftEyeLength = face_landmarks['left_eye'][3][0] - face_landmarks['left_eye'][0][0]
    rightEyeLength = face_landmarks['right_eye'][3][0] - face_landmarks['right_eye'][0][0]

    print("tjfr", face_landmarks['right_eye'][3])

    print("Length of eyes", eyesLength)
    print("Length of left eye", leftEyeLength)
    print("Length of right eye", rightEyeLength)

    print("Between eyebrows", face_landmarks['left_eyebrow'][face_landmarks['left_eyebrow'].count(int) - 1][0])

    pil_image.show()
