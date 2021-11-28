from imutils.face_utils import FaceAligner
import imutils
import dlib
import cv2

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
fa = FaceAligner(predictor, desiredFaceWidth=128)


def imaginate(file):
    try:

        image = cv2.imread(file)
        image = imutils.resize(image, width=800)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        rects = detector(gray, 2)

        if len(rects) > 1:
            return 2

        rect = rects[0]
        face_aligned = fa.align(image, gray, rect)
        cv2.imwrite(file, face_aligned)

        return 1

    except IndexError:
        return 0
