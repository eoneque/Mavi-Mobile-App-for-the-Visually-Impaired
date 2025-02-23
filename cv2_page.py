import cv2
print(cv2.__version__)
recognizer = cv2.face.EigenFaceRecognizer_create()
print("EigenFaceRecognizer created successfully.")
