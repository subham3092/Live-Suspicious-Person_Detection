import cv2
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import tkinter as tk
from tkinter import messagebox

login_success = False

def login():

    global login_success

    username = username_entry.get()
    password = password_entry.get()

    if username == "Shubham" and password == "1234":
        login_success = True
        root.destroy()

    else:
        messagebox.showerror(
            "Login Failed",
            "Invalid Username or Password"
        )


root = tk.Tk()

root.title("Criminal Detection Login")
root.geometry("350x220")
root.resizable(False, False)

tk.Label(
    root,
    text="Criminal Detection System",
    font=("Arial", 14, "bold")
).pack(pady=15)

tk.Label(root, text="Username").pack()

username_entry = tk.Entry(root, width=30)
username_entry.pack()

tk.Label(root, text="Password").pack()

password_entry = tk.Entry(root, show="*", width=30)
password_entry.pack()

tk.Button(
    root,
    text="Login",
    command=login,
    width=15,
    bg="green",
    fg="white"
).pack(pady=15)

root.mainloop()

if not login_success:
    exit()

import cv2
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

dataset_path = r"C:\Users\Lenovo\OneDrive\Desktop\Face_Detection\dataset"

face_data = []
labels = []
names = {}

print("Loading Dataset...")

class_id = 0

for file in os.listdir(dataset_path):

    if not file.endswith(".npy"):
        continue

    parts = file[:-4].split("__")

    if len(parts) < 2:
        continue

    name = parts[0]
    crime = parts[1]

    names[class_id] = f"{name} | {crime}"

    data = np.load(os.path.join(dataset_path, file))

    for img in data:

        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        img = cv2.resize(img, (100, 100))
        face_data.append(img.flatten())
        labels.append(class_id)

    class_id += 1

face_data = np.array(face_data)
labels = np.array(labels)

print("Dataset Loaded")

X_train, X_test, y_train, y_test = train_test_split(
    face_data,
    labels,
    test_size=0.2,
    random_state=42
)

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)

# accuracy = model.score(X_test, y_test) * 100
# print(f"Accuracy: {accuracy:.2f}%")

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_alt.xml"
)

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    for (x, y, w, h) in faces:

        face = gray[y:y+h, x:x+w]

        try:
            face = cv2.resize(face, (100, 100))
        except:
            continue

        face = face.flatten().reshape(1, -1)

        prediction = model.predict(face)[0]

        label = names[prediction]

        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            label,
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    cv2.imshow("Criminal Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()