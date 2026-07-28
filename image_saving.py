import cv2
import numpy as np
import os

name = input("Enter person name: ")
crime = input("Enter crime: ")
age = input("Enter age: ")

dataset_path = r"C:\Users\Lenovo\OneDrive\Desktop\Face_Detection\dataset"

os.makedirs(
    dataset_path,
    exist_ok=True
)

person_folder = os.path.join(
    dataset_path,
    name.replace(" ", "_")
)

os.makedirs(
    person_folder,
    exist_ok=True
)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not found")
    exit()

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_alt.xml"
)

if face_cascade.empty():
    print("Face detector not loaded")
    exit()

sharpen_kernel = np.array([
    [0,-1,0],
    [-1,5,-1],
    [0,-1,0]
])

face_data = []

count = 0

max_faces = 50

def is_blurry(image):

    variance = cv2.Laplacian(
        image,
        cv2.CV_64F
    ).var()

    return variance < 50

print("\nCamera Started")

while True:
    ret, frame = cap.read()

    if not ret:
        continue

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    for (x,y,w,h) in faces:

        offset = 10

        x1 = max(0, x-offset)
        y1 = max(0, y-offset)

        x2 = min(
            gray.shape[1],
            x+w+offset
        )

        y2 = min(
            gray.shape[0],
            y+h+offset
        )

        face_section = gray[y1:y2, x1:x2]

        face_section = cv2.resize(
            face_section,
            (100,100)
        )

        face_section = cv2.filter2D(
            face_section,
            -1,
            sharpen_kernel
        )

        if is_blurry(face_section):
            continue

        face_data.append(
            face_section
        )

        img_path = os.path.join(
            person_folder,
            f"{name}_{count}.jpg"
        )

        cv2.imwrite(
            img_path,
            face_section
        )

        count += 1

        cv2.rectangle(
            frame,
            (x,y),
            (x+w,y+h),
            (0,255,0),
            2
        )

        cv2.putText(
            frame,
            f"Captured: {count}",
            (x,y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,0),
            2
        )

    cv2.imshow(
        "Face Capture",
        frame
    )



    if (
        cv2.waitKey(1) & 0xFF == ord('q')
        or count >= max_faces
    ):
        break
cap.release()
cv2.destroyAllWindows()

if len(face_data) == 0:

    print("No face captured")
    exit()

face_data = np.array(
    face_data
)

safe_name = name.replace(
    " ",
    "_"
)

safe_crime = crime.replace(
    " ",
    "_"
)

safe_age = age.replace(
    " ",
    "_"
)

filename = (
    f"{safe_name}__{safe_crime}__{safe_age}.npy"
)

save_path = os.path.join(
    dataset_path,
    filename
)

np.save(
    save_path,
    face_data
)

print("\n========== DATA SAVED ==========")
print("Name :", name)
print("File:", save_path)