# import cv2
# import numpy as np
# import os

# name = input("Enter person name: ")
# crime = input("Enter crime: ")
# age = input("Enter age: ")

# dataset_path = r"C:\Users\Lenovo\OneDrive\Desktop\Face_Detection\dataset"

# os.makedirs(
#     dataset_path,
#     exist_ok=True
# )

# person_folder = os.path.join(
#     dataset_path,
#     name.replace(" ", "_")
# )

# os.makedirs(
#     person_folder,
#     exist_ok=True
# )

# cap = cv2.VideoCapture(0)

# if not cap.isOpened():
#     print("Camera not found")
#     exit()

# face_cascade = cv2.CascadeClassifier(
#     cv2.data.haarcascades +
#     "haarcascade_frontalface_alt.xml"
# )

# if face_cascade.empty():
#     print("Face detector not loaded")
#     exit()

# sharpen_kernel = np.array([
#     [0,-1,0],
#     [-1,5,-1],
#     [0,-1,0]
# ])

# face_data = []

# count = 0

# max_faces = 50

# def is_blurry(image):

#     variance = cv2.Laplacian(
#         image,
#         cv2.CV_64F
#     ).var()

#     return variance < 50

# print("\nCamera Started")

# while True:
#     ret, frame = cap.read()

#     if not ret:
#         continue

#     gray = cv2.cvtColor(
#         frame,
#         cv2.COLOR_BGR2GRAY
#     )

#     faces = face_cascade.detectMultiScale(
#         gray,
#         scaleFactor=1.3,
#         minNeighbors=5
#     )

#     for (x,y,w,h) in faces:

#         offset = 10

#         x1 = max(0, x-offset)
#         y1 = max(0, y-offset)

#         x2 = min(
#             gray.shape[1],
#             x+w+offset
#         )

#         y2 = min(
#             gray.shape[0],
#             y+h+offset
#         )

#         face_section = gray[y1:y2, x1:x2]

#         face_section = cv2.resize(
#             face_section,
#             (100,100)
#         )

#         face_section = cv2.filter2D(
#             face_section,
#             -1,
#             sharpen_kernel
#         )

#         if is_blurry(face_section):
#             continue

#         face_data.append(
#             face_section
#         )

#         img_path = os.path.join(
#             person_folder,
#             f"{name}_{count}.jpg"
#         )

#         cv2.imwrite(
#             img_path,
#             face_section
#         )

#         count += 1

#         cv2.rectangle(
#             frame,
#             (x,y),
#             (x+w,y+h),
#             (0,255,0),
#             2
#         )

#         cv2.putText(
#             frame,
#             f"Captured: {count}",
#             (x,y-10),
#             cv2.FONT_HERSHEY_SIMPLEX,
#             0.8,
#             (0,255,0),
#             2
#         )

#     cv2.imshow(
#         "Face Capture",
#         frame
#     )



#     if (
#         cv2.waitKey(1) & 0xFF == ord('q')
#         or count >= max_faces
#     ):
#         break
# cap.release()
# cv2.destroyAllWindows()

# if len(face_data) == 0:

#     print("No face captured")
#     exit()

# face_data = np.array(
#     face_data
# )

# safe_name = name.replace(
#     " ",
#     "_"
# )

# safe_crime = crime.replace(
#     " ",
#     "_"
# )

# safe_age = age.replace(
#     " ",
#     "_"
# )

# filename = (
#     f"{safe_name}__{safe_crime}__{safe_age}.npy"
# )

# save_path = os.path.join(
#     dataset_path,
#     filename
# )

# np.save(
#     save_path,
#     face_data
# )

# print("\n========== DATA SAVED ==========")
# print("Name :", name)
# print("File:", save_path)

# with gui

import cv2
import numpy as np
import os

DATASET_PATH = r"C:\My_Projects\Criminal_detection\Data_set"
os.makedirs(DATASET_PATH, exist_ok=True)

print("=" * 55)
print("     CRIMINAL BIOMETRIC DATA ENROLLMENT SYSTEM      ")
print("=" * 55)

name = input("Enter Person Name: ").strip()
crime = input("Enter Crime / Charge: ").strip()
fir = input("Enter FIR / Case No: ").strip()

safe_name = name.replace(" ", "_")
safe_crime = crime.replace(" ", "_")
safe_fir = fir.replace(" ", "_")

person_folder = os.path.join(DATASET_PATH, safe_name)
os.makedirs(person_folder, exist_ok=True)

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_alt.xml"
)

sharpen_kernel = np.array([
    [0, -1, 0],
    [-1,  5, -1],
    [0, -1, 0]
])

face_data = []
count = 0
max_faces = 50
mugshot_saved = False

def is_blurry(image):
    return cv2.Laplacian(image, cv2.CV_64F).var() < 50

print("\n[+] Camera starting... Look at the camera.")
print("[+] Press 'q' to stop early.\n")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        offset = 10
        y1 = max(0, y - offset)
        y2 = min(frame.shape[0], y + h + offset)
        x1 = max(0, x - offset)
        x2 = min(frame.shape[1], x + w + offset)

        face_section = gray[y1:y2, x1:x2]
        if face_section.size == 0:
            continue

        face_section = cv2.resize(face_section, (100, 100))
        face_section = cv2.filter2D(face_section, -1, sharpen_kernel)

        if is_blurry(face_section):
            continue

        face_data.append(face_section)

        if not mugshot_saved:
            mugshot_filename = f"{safe_name}__{safe_crime}__{safe_fir}.jpg"
            mugshot_path = os.path.join(DATASET_PATH, mugshot_filename)
            color_crop = frame[y1:y2, x1:x2]
            if color_crop.size > 0:
                cv2.imwrite(mugshot_path, color_crop)
                mugshot_saved = True

        sample_path = os.path.join(person_folder, f"{safe_name}_{count}.jpg")
        cv2.imwrite(sample_path, face_section)

        count += 1

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, f"Capturing: {count}/{max_faces}", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Face Enrollment - VisionShield", frame)

    if cv2.waitKey(1) & 0xFF == ord('q') or count >= max_faces:
        break

if len(face_data) > 0:
    npy_filename = f"{safe_name}__{safe_crime}__{safe_fir}.npy"
    npy_path = os.path.join(DATASET_PATH, npy_filename)
    
    np.save(npy_path, np.array(face_data))
    
    print("\n" + "=" * 55)
    print(f"[✓] ENROLLMENT COMPLETE FOR: {name.upper()}")
    print(f"[✓] Samples Saved : {len(face_data)}")
    print(f"[✓] Target Folder  : {DATASET_PATH}")
    print(f"[✓] NPY File       : {npy_filename}")
    if mugshot_saved:
        print(f"[✓] Mugshot Photo  : {mugshot_filename}")
    print("=" * 55)
else:
    print("\n[-] Koi face capture nahi hua. Dubara run karein.")

cap.release()
cv2.destroyAllWindows()
