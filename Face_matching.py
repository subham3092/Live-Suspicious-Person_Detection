# import cv2
# import os
# import numpy as np
# from sklearn.model_selection import train_test_split
# from sklearn.neighbors import KNeighborsClassifier
# import tkinter as tk
# from tkinter import messagebox

# login_success = False

# def login():

#     global login_success

#     username = username_entry.get()
#     password = password_entry.get()

#     if username == "Subham" and password == "1234":
#         login_success = True
#         root.destroy()

#     else:
#         messagebox.showerror(
#             "Login Failed",
#             "Invalid Username or Password"
#         )


# root = tk.Tk()

# root.title("Criminal Detection Login")
# root.geometry("350x220")
# root.resizable(False, False)

# tk.Label(
#     root,
#     text="Criminal Detection System",
#     font=("Arial", 14, "bold")
# ).pack(pady=15)

# tk.Label(root, text="Username").pack()

# username_entry = tk.Entry(root, width=30)
# username_entry.pack()

# tk.Label(root, text="Password").pack()

# password_entry = tk.Entry(root, show="*", width=30)
# password_entry.pack()

# tk.Button(
#     root,
#     text="Login",
#     command=login,
#     width=15,
#     bg="green",
#     fg="white"
# ).pack(pady=15)

# root.mainloop()

# if not login_success:
#     exit()

# import cv2
# import os
# import numpy as np
# from sklearn.model_selection import train_test_split
# from sklearn.neighbors import KNeighborsClassifier

# dataset_path = r"C:\Users\Lenovo\OneDrive\Desktop\Face_Detection\dataset"

# face_data = []
# labels = []
# names = {}

# print("Loading Dataset...")

# class_id = 0

# for file in os.listdir(dataset_path):

#     if not file.endswith(".npy"):
#         continue

#     parts = file[:-4].split("__")

#     if len(parts) < 2:
#         continue

#     name = parts[0]
#     crime = parts[1]

#     names[class_id] = f"{name} | {crime}"

#     data = np.load(os.path.join(dataset_path, file))

#     for img in data:

#         if len(img.shape) == 3:
#             img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#         img = cv2.resize(img, (100, 100))
#         face_data.append(img.flatten())
#         labels.append(class_id)

#     class_id += 1

# face_data = np.array(face_data)
# labels = np.array(labels)

# print("Dataset Loaded")

# X_train, X_test, y_train, y_test = train_test_split(
#     face_data,
#     labels,
#     test_size=0.2,
#     random_state=42
# )

# model = KNeighborsClassifier(n_neighbors=5)
# model.fit(X_train, y_train)

# # accuracy = model.score(X_test, y_test) * 100
# # print(f"Accuracy: {accuracy:.2f}%")

# face_cascade = cv2.CascadeClassifier(
#     cv2.data.haarcascades +
#     "haarcascade_frontalface_alt.xml"
# )

# cap = cv2.VideoCapture(0)

# while True:

#     ret, frame = cap.read()

#     if not ret:
#         continue

#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     faces = face_cascade.detectMultiScale(
#         gray,
#         scaleFactor=1.3,
#         minNeighbors=5
#     )

#     for (x, y, w, h) in faces:

#         face = gray[y:y+h, x:x+w]

#         try:
#             face = cv2.resize(face, (100, 100))
#         except:
#             continue

#         face = face.flatten().reshape(1, -1)

#         prediction = model.predict(face)[0]

#         label = names[prediction]

#         cv2.rectangle(
#             frame,
#             (x, y),
#             (x+w, y+h),
#             (0, 255, 0),
#             2
#         )

#         cv2.putText(
#             frame,
#             label,
#             (x, y-10),
#             cv2.FONT_HERSHEY_SIMPLEX,
#             0.7,
#             (0, 255, 0),
#             2
#         )

#     cv2.imshow("Criminal Detection", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

# with GUI

import cv2
import os
import time
import math
import threading
from collections import deque
import numpy as np
from datetime import datetime
from PIL import Image, ImageTk, ImageDraw
import winsound
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

DATASET_PATH = r"C:\My_Projects\Criminal_detection\Data_set"
ALERTS_DIR = r"C:\My_Projects\Criminal_detection\alerts_log"

os.makedirs(DATASET_PATH, exist_ok=True)
os.makedirs(ALERTS_DIR, exist_ok=True)

THEMES = {
    "indigo": {
        "name": "Midnight Indigo",
        "bg_root": "#070B14",
        "panel_bg": "#0D1424",
        "card_bg": "#131C31",
        "card_border": "#212F4A",
        "input_bg": "#0B1120",
        "input_border": "#263554",
        "primary": "#6366F1",         
        "primary_hover": "#4F46E5",
        "primary_glow": "#818CF8",
        "secondary": "#38BDF8",       
        "success": "#10B981",         
        "success_hover": "#059669",
        "alert": "#F43F5E",           
        "alert_hover": "#E11D48",
        "warning": "#F59E0B",         
        "text_primary": "#F8FAFC",
        "text_muted": "#94A3B8",
        "text_dim": "#64748B",
        "radar_circle": "#1E2C44",
        "radar_sweep": "#6366F1",
        "hud_wanted": (94, 63, 244),  
        "hud_citizen": (129, 185, 16),
        "hud_jitter": (11, 158, 245)
    },
    "cyber_teal": {
        "name": "Nordic Teal",
        "bg_root": "#060D13",
        "panel_bg": "#0B1721",
        "card_bg": "#102230",
        "card_border": "#1A364C",
        "input_bg": "#08131B",
        "input_border": "#1D3B53",
        "primary": "#06B6D4",         
        "primary_hover": "#0891B2",
        "primary_glow": "#67E8F9",
        "secondary": "#2DD4BF",
        "success": "#10B981",
        "success_hover": "#059669",
        "alert": "#EF4444",
        "alert_hover": "#DC2626",
        "warning": "#F59E0B",
        "text_primary": "#F0FDF4",
        "text_muted": "#7DD3FC",
        "text_dim": "#475569",
        "radar_circle": "#163042",
        "radar_sweep": "#06B6D4",
        "hud_wanted": (40, 40, 240),
        "hud_citizen": (80, 210, 80),
        "hud_jitter": (0, 180, 255)
    },
    "obsidian_gold": {
        "name": "Imperial Gold",
        "bg_root": "#0B0C10",
        "panel_bg": "#13151D",
        "card_bg": "#1B1E29",
        "card_border": "#2D3244",
        "input_bg": "#0E1017",
        "input_border": "#272C3D",
        "primary": "#EAB308",         
        "primary_hover": "#CA8A04",
        "primary_glow": "#FDE047",
        "secondary": "#A78BFA",
        "success": "#10B981",
        "success_hover": "#059669",
        "alert": "#F43F5E",
        "alert_hover": "#E11D48",
        "warning": "#F59E0B",
        "text_primary": "#FAFAF9",
        "text_muted": "#CBD5E1",
        "text_dim": "#64748B",
        "radar_circle": "#262B3B",
        "radar_sweep": "#EAB308",
        "hud_wanted": (94, 63, 244),
        "hud_citizen": (129, 185, 16),
        "hud_jitter": (8, 179, 234)
    }
}

CURRENT_THEME_KEY = "indigo"
T = THEMES[CURRENT_THEME_KEY]

FONT_MAIN = "Segoe UI"
FONT_CODE = "Consolas"

class BiometricEngine:
    def __init__(self):
        self.face_detector = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        self.suspect_profiles = {}
        self.pos_history = deque(maxlen=25)

    def extract_feature(self, img_gray_or_rgb):
        if len(img_gray_or_rgb.shape) == 3:
            gray = cv2.cvtColor(img_gray_or_rgb, cv2.COLOR_BGR2GRAY)
        else:
            gray = img_gray_or_rgb

        resized = cv2.resize(gray, (100, 100))
        equalized = cv2.equalizeHist(resized)
        
        hog = cv2.HOGDescriptor((100, 100), (20, 20), (10, 10), (10, 10), 9)
        feat = hog.compute(equalized)
        norm = np.linalg.norm(feat)
        return (feat / norm).flatten() if norm > 0 else feat.flatten()

    def load_all_datasets(self, dataset_dir):
        self.suspect_profiles.clear()
        total_samples = 0

        if not os.path.exists(dataset_dir):
            return 0

        for file in os.listdir(dataset_dir):
            full_path = os.path.join(dataset_dir, file)

            if file.endswith(".npy"):
                parts = file[:-4].split("__")
                name = parts[0].replace("_", " ")
                crime = parts[1].replace("_", " ") if len(parts) > 1 else "Wanted Suspect"
                fir = parts[2].replace("_", " ") if len(parts) > 2 else f"FIR-2026-{file[:4]}"

                try:
                    data = np.load(full_path, allow_pickle=True)
                    if name not in self.suspect_profiles:
                        self.suspect_profiles[name] = {"crime": crime, "fir": fir, "templates": [], "img_path": None}

                    for raw_face in data:
                        vec = self.extract_feature(raw_face)
                        self.suspect_profiles[name]["templates"].append(vec)
                        total_samples += 1
                except Exception as e:
                    print(f"[-] Error loading {file}: {e}")

            elif file.lower().endswith((".jpg", ".jpeg", ".png")):
                parts = os.path.splitext(file)[0].split("__")
                name = parts[0].replace("_", " ")
                crime = parts[1].replace("_", " ") if len(parts) > 1 else "Wanted Suspect"
                fir = parts[2].replace("_", " ") if len(parts) > 2 else f"FIR-2026-{name}"

                img = cv2.imread(full_path)
                if img is not None:
                    if name not in self.suspect_profiles:
                        self.suspect_profiles[name] = {"crime": crime, "fir": fir, "templates": [], "img_path": full_path}
                    else:
                        self.suspect_profiles[name]["img_path"] = full_path
                    
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = self.face_detector.detectMultiScale(gray, 1.1, 4, minSize=(60, 60))
                    if len(faces) > 0:
                        x, y, w, h = max(faces, key=lambda b: b[2] * b[3])
                        crop = gray[y:y+h, x:x+w]
                    else:
                        crop = gray

                    vec = self.extract_feature(crop)
                    self.suspect_profiles[name]["templates"].append(vec)
                    total_samples += 1

        print(f"[+] Biometric Database Loaded: {len(self.suspect_profiles)} Suspects ({total_samples} templates)")
        return len(self.suspect_profiles)

    def find_match(self, face_crop, threshold=0.52):
        if not self.suspect_profiles:
            return None, 0.0

        query_vec = self.extract_feature(face_crop)
        best_overall_sim = 0.0
        matched_suspect = None

        for name, profile in self.suspect_profiles.items():
            for tpl in profile["templates"]:
                norm_prod = np.linalg.norm(query_vec) * np.linalg.norm(tpl)
                if norm_prod == 0:
                    continue
                sim = float(np.dot(query_vec, tpl) / norm_prod)
                if sim > best_overall_sim:
                    best_overall_sim = sim
                    matched_suspect = {
                        "name": name,
                        "crime": profile["crime"],
                        "fir": profile["fir"],
                        "img_path": profile.get("img_path")
                    }

        conf_pct = round(best_overall_sim * 100, 1)

        if best_overall_sim >= threshold:
            return matched_suspect, conf_pct
        return None, conf_pct

    def analyze_motion_jitter(self, center_pt):
        self.pos_history.append(center_pt)
        if len(self.pos_history) < 8:
            return False, 0

        displacements = []
        for i in range(1, len(self.pos_history)):
            p1 = self.pos_history[i-1]
            p2 = self.pos_history[i]
            dist = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
            displacements.append(dist)

        velocity = np.mean(displacements)
        jitter = np.std(displacements)
        motion_score = int(min(100, (velocity * 2.8) + (jitter * 4.5)))
        is_suspicious = motion_score > 48

        return is_suspicious, motion_score

class ModernCanvasSlider(tk.Canvas):
    def __init__(self, parent, from_=30, to=85, initial=52, width=260, height=26, bg="#141D30", active_color="#6366F1", command=None):
        super().__init__(parent, width=width, height=height, bg=bg, highlightthickness=0)
        self.from_val = from_
        self.to_val = to
        self.current_val = initial
        self.slider_width = width
        self.slider_height = height
        self.active_color = active_color
        self.command = command
        self.pad_x = 12
        self.is_dragging = False

        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.draw_slider()

    def set_active_color(self, color, bg_color):
        self.active_color = color
        self.configure(bg=bg_color)
        self.draw_slider()

    def val_to_x(self, val):
        ratio = (val - self.from_val) / (self.to_val - self.from_val)
        return self.pad_x + ratio * (self.slider_width - 2 * self.pad_x)

    def x_to_val(self, x):
        clamped_x = max(self.pad_x, min(self.slider_width - self.pad_x, x))
        ratio = (clamped_x - self.pad_x) / (self.slider_width - 2 * self.pad_x)
        return self.from_val + ratio * (self.to_val - self.from_val)

    def draw_slider(self):
        self.delete("all")
        cy = self.slider_height // 2
        track_h = 6

        self.create_line(self.pad_x, cy, self.slider_width - self.pad_x, cy, fill="#212F4A", width=track_h, capstyle="round")
        thumb_x = self.val_to_x(self.current_val)
        self.create_line(self.pad_x, cy, thumb_x, cy, fill=self.active_color, width=track_h, capstyle="round")

        r = 8
        self.create_oval(thumb_x - r - 2, cy - r - 2, thumb_x + r + 2, cy + r + 2, fill=self.active_color, outline="")
        self.create_oval(thumb_x - r, cy - r, thumb_x + r, cy + r, fill="#FFFFFF", outline=self.active_color, width=2)

    def on_click(self, event):
        self.is_dragging = True
        self.update_from_x(event.x)

    def on_drag(self, event):
        if self.is_dragging:
            self.update_from_x(event.x)

    def on_release(self, event):
        self.is_dragging = False

    def update_from_x(self, x):
        new_val = int(round(self.x_to_val(x)))
        if new_val != self.current_val:
            self.current_val = new_val
            self.draw_slider()
            if self.command:
                self.command(self.current_val)


def create_card(parent, title="", theme=T, pady=12, padx=14):
    card = tk.Frame(parent, bg=theme["card_bg"], highlightbackground=theme["card_border"], highlightthickness=1, bd=0)
    if title:
        head_box = tk.Frame(card, bg=theme["card_bg"])
        head_box.pack(fill="x", padx=padx, pady=(pady, 8))
        tk.Label(head_box, text="◆", font=(FONT_MAIN, 7), fg=theme["primary_glow"], bg=theme["card_bg"]).pack(side="left", padx=(0, 6))
        tk.Label(head_box, text=title.upper(), font=(FONT_MAIN, 9, "bold"), fg=theme["secondary"], bg=theme["card_bg"]).pack(side="left")
    return card


def create_luxury_button(parent, text, bg, hover_bg, fg="#FFFFFF", font=None, command=None):
    if font is None:
        font = (FONT_MAIN, 10, "bold")
    btn = tk.Button(parent, text=text, font=font, bg=bg, fg=fg, activebackground=hover_bg, activeforeground=fg, relief="flat", bd=0, cursor="hand2", command=command)
    def on_enter(e):
        if btn["state"] != "disabled": btn.config(bg=hover_bg)
    def on_leave(e):
        if btn["state"] != "disabled": btn.config(bg=bg)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

class VisionShieldApp:
    def __init__(self, root):
        self.root = root
        self.theme = T
        self.root.title("VisionShield Pro | Tactical Biometric Intelligence Console")
        self.root.geometry("1440x870")
        self.root.minsize(1280, 760)
        self.root.configure(bg=self.theme["bg_root"])

        self.ai = BiometricEngine()
        self.cap = None
        self.is_running = False
        self.match_threshold = 0.52
        self.last_beep_time = 0
        self.last_motion_alert_time = 0
        self.current_officer = "Subham Kumar"
        self.fps_time = time.time()
        self.fps_counter = 0
        self.current_fps = 0

        self.radar_angle = 0
        self.radar_timer = None

        self.login_laser_y = 50
        self.login_laser_dir = 2
        self.login_scan_timer = None
        self.password_visible = False

        self.num_suspects = self.ai.load_all_datasets(DATASET_PATH)
        self.create_login_screen()

    def apply_theme(self, theme_key):
        global CURRENT_THEME_KEY, T
        if theme_key in THEMES:
            CURRENT_THEME_KEY = theme_key
            self.theme = THEMES[theme_key]
            T = self.theme
            self.root.configure(bg=self.theme["bg_root"])

            was_running = self.is_running
            if was_running:
                self.toggle_camera()

            if hasattr(self, 'dash_frame') and self.dash_frame.winfo_exists():
                self.dash_frame.destroy()
                self.create_dashboard(self.current_officer)
                if was_running:
                    self.toggle_camera()
            elif hasattr(self, 'login_frame') and self.login_frame.winfo_exists():
                self.stop_login_animation()
                self.login_frame.destroy()
                self.create_login_screen()

    def create_login_screen(self):
        t = self.theme
        self.login_frame = tk.Frame(self.root, bg=t["bg_root"])
        self.login_frame.pack(fill="both", expand=True)

        outer_container = tk.Frame(self.login_frame, bg=t["bg_root"])
        outer_container.place(relx=0.5, rely=0.5, anchor="center")

        top_banner = tk.Frame(outer_container, bg=t["bg_root"])
        top_banner.pack(pady=(0, 16))

        tk.Label(
            top_banner,
            text="FEDERAL LAW ENFORCEMENT BIOMETRIC CLEARANCE PORTAL",
            font=(FONT_CODE, 9, "bold"),
            fg=t["primary_glow"],
            bg=t["bg_root"]
        ).pack()

        master_card = tk.Frame(
            outer_container,
            bg=t["panel_bg"],
            highlightbackground=t["card_border"],
            highlightthickness=1,
            bd=0
        )
        master_card.pack()

        left_pane = tk.Frame(master_card, bg="#070D18", width=420, height=520, highlightbackground=t["card_border"], highlightthickness=1)
        left_pane.pack(side="left", fill="both")
        left_pane.pack_propagate(False)

        lp_header = tk.Frame(left_pane, bg="#070D18", height=46)
        lp_header.pack(fill="x", padx=16, pady=(14, 0))

        tk.Label(lp_header, text="● SENSOR LINKED", font=(FONT_CODE, 8, "bold"), fg=t["success"], bg="#070D18").pack(side="left")
        tk.Label(lp_header, text="BIO-ID // V2.5", font=(FONT_CODE, 8), fg=t["secondary"], bg="#070D18").pack(side="right")

        self.bio_canvas = tk.Canvas(left_pane, width=380, height=330, bg="#070D18", highlightthickness=0)
        self.bio_canvas.pack(pady=4)

        lp_footer = tk.Frame(left_pane, bg="#0A1324", padx=14, pady=10, highlightbackground=t["card_border"], highlightthickness=1)
        lp_footer.pack(fill="x", padx=16, pady=(8, 14))

        tk.Label(
            lp_footer,
            text="HOG VECTOR ENGINE: ARMED",
            font=(FONT_CODE, 8, "bold"),
            fg=t["secondary"],
            bg="#0A1324"
        ).pack(anchor="w")

        tk.Label(
            lp_footer,
            text="ENCRYPTION: AES-256 GCM  |  NODE: SECURE-09",
            font=(FONT_CODE, 7),
            fg=t["text_dim"],
            bg="#0A1324"
        ).pack(anchor="w", pady=(2, 0))

        right_pane = tk.Frame(master_card, bg=t["panel_bg"], width=460, height=520)
        right_pane.pack(side="left", fill="both")
        right_pane.pack_propagate(False)

        rp_body = tk.Frame(right_pane, bg=t["panel_bg"], padx=34, pady=24)
        rp_body.pack(fill="both", expand=True)

        badge_row = tk.Frame(rp_body, bg=t["panel_bg"])
        badge_row.pack(anchor="w", pady=(0, 6))

        tk.Label(badge_row, text="🛡️", font=(FONT_MAIN, 16), bg=t["panel_bg"], fg=t["primary"]).pack(side="left", padx=(0, 8))
        tk.Label(badge_row, text="VISIONSHIELD PRO", font=(FONT_MAIN, 15, "bold"), fg=t["text_primary"], bg=t["panel_bg"]).pack(side="left")
        
        tier_lbl = tk.Label(badge_row, text="LEVEL 4", font=(FONT_CODE, 7, "bold"), bg=t["card_bg"], fg=t["secondary"], padx=6, pady=2)
        tier_lbl.pack(side="left", padx=10)

        tk.Label(
            rp_body,
            text="Sign in to initialize tactical biometric intelligence operations.",
            font=(FONT_MAIN, 9),
            fg=t["text_muted"],
            bg=t["panel_bg"]
        ).pack(anchor="w", pady=(0, 16))

        quick_fill_btn = tk.Button(
            rp_body,
            text="⚡ Quick Fill: Officer Subham Kumar",
            font=(FONT_MAIN, 8, "bold"),
            bg=t["card_bg"],
            fg=t["secondary"],
            activebackground=t["input_border"],
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=8,
            pady=3,
            command=self.auto_fill_credentials
        )
        quick_fill_btn.pack(anchor="w", pady=(0, 14))

        tk.Label(
            rp_body,
            text="OPERATOR IDENTIFIER",
            font=(FONT_MAIN, 8, "bold"),
            fg=t["text_muted"],
            bg=t["panel_bg"]
        ).pack(anchor="w", pady=(0, 4))

        u_box = tk.Frame(rp_body, bg=t["input_bg"], highlightbackground=t["input_border"], highlightthickness=1)
        u_box.pack(fill="x", pady=(0, 14))

        tk.Label(u_box, text="👤", font=(FONT_MAIN, 11), bg=t["input_bg"], fg=t["secondary"]).pack(side="left", padx=(12, 6))
        self.user_entry = tk.Entry(
            u_box,
            font=(FONT_MAIN, 11),
            bg=t["input_bg"],
            fg=t["text_primary"],
            insertbackground=t["secondary"],
            bd=0,
            relief="flat"
        )
        self.user_entry.insert(0, "Subham Kumar")
        self.user_entry.pack(side="left", fill="both", expand=True, ipady=7, padx=(0, 10))

        tk.Label(
            rp_body,
            text="SECURITY PASSCODE",
            font=(FONT_MAIN, 8, "bold"),
            fg=t["text_muted"],
            bg=t["panel_bg"]
        ).pack(anchor="w", pady=(0, 4))

        p_box = tk.Frame(rp_body, bg=t["input_bg"], highlightbackground=t["input_border"], highlightthickness=1)
        p_box.pack(fill="x", pady=(0, 10))

        tk.Label(p_box, text="🔒", font=(FONT_MAIN, 11), bg=t["input_bg"], fg=t["secondary"]).pack(side="left", padx=(12, 6))
        self.pass_entry = tk.Entry(
            p_box,
            font=(FONT_MAIN, 11),
            show="●",
            bg=t["input_bg"],
            fg=t["text_primary"],
            insertbackground=t["secondary"],
            bd=0,
            relief="flat"
        )
        self.pass_entry.insert(0, "1234")
        self.pass_entry.pack(side="left", fill="both", expand=True, ipady=7)
        self.pass_entry.bind("<Return>", lambda e: self.authenticate())

        self.eye_btn = tk.Button(
            p_box,
            text="👁",
            font=(FONT_MAIN, 10),
            bg=t["input_bg"],
            fg=t["text_muted"],
            activebackground=t["input_bg"],
            activeforeground=t["secondary"],
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=8,
            command=self.toggle_password_visibility
        )
        self.eye_btn.pack(side="right")

        self.login_error_lbl = tk.Label(
            rp_body,
            text="",
            font=(FONT_MAIN, 8, "bold"),
            fg=t["alert"],
            bg=t["panel_bg"]
        )
        self.login_error_lbl.pack(anchor="w", pady=(0, 6))

        sign_btn = create_luxury_button(
            rp_body,
            text="INITIALIZE SESSION  ➔",
            bg=t["primary"],
            hover_bg=t["primary_hover"],
            font=(FONT_MAIN, 10, "bold"),
            command=self.authenticate
        )
        sign_btn.pack(fill="x", ipady=7, pady=(4, 12))

        tk.Label(
            rp_body,
            text="⚠️ UNAUTHORIZED ATTEMPTS ARE LOGGED & TRACED BY IP",
            font=(FONT_CODE, 7, "bold"),
            fg=t["text_dim"],
            bg=t["panel_bg"]
        ).pack(anchor="w")

        self.start_login_animation()

    def toggle_password_visibility(self):
        self.password_visible = not self.password_visible
        if self.password_visible:
            self.pass_entry.config(show="")
            self.eye_btn.config(text="🙈", fg=self.theme["secondary"])
        else:
            self.pass_entry.config(show="●")
            self.eye_btn.config(text="👁", fg=self.theme["text_muted"])

    def auto_fill_credentials(self):
        self.user_entry.delete(0, "end")
        self.user_entry.insert(0, "Subham Kmar")
        self.pass_entry.delete(0, "end")
        self.pass_entry.insert(0, "1234")
        self.login_error_lbl.config(text="✓ Credentials loaded. Click 'Initialize Session'.", fg=self.theme["success"])

    def start_login_animation(self):
        if not hasattr(self, 'bio_canvas') or not self.bio_canvas.winfo_exists():
            return

        w = self.bio_canvas.winfo_width()
        h = self.bio_canvas.winfo_height()
        if w < 10 or h < 10:
            w, h = 380, 330

        cx, cy = w // 2, h // 2
        t = self.theme

        self.bio_canvas.delete("all")

        r_outer = 110
        self.bio_canvas.create_oval(cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer, outline="#162238", width=1)
        self.bio_canvas.create_oval(cx - r_outer + 12, cy - r_outer + 12, cx + r_outer - 12, cy + r_outer - 12, outline="#1B2B45", width=1, dash=(3, 3))

        b_pad = 130
        c_len = 16
        self.bio_canvas.create_line(cx - b_pad, cy - b_pad, cx - b_pad + c_len, cy - b_pad, fill=t["secondary"], width=2)
        self.bio_canvas.create_line(cx - b_pad, cy - b_pad, cx - b_pad, cy - b_pad + c_len, fill=t["secondary"], width=2)
        self.bio_canvas.create_line(cx + b_pad, cy - b_pad, cx + b_pad - c_len, cy - b_pad, fill=t["secondary"], width=2)
        self.bio_canvas.create_line(cx + b_pad, cy - b_pad, cx + b_pad, cy - b_pad + c_len, fill=t["secondary"], width=2)
        self.bio_canvas.create_line(cx - b_pad, cy + b_pad, cx - b_pad + c_len, cy + b_pad, fill=t["secondary"], width=2)
        self.bio_canvas.create_line(cx - b_pad, cy + b_pad, cx - b_pad, cy + b_pad - c_len, fill=t["secondary"], width=2)
        self.bio_canvas.create_line(cx + b_pad, cy + b_pad, cx + b_pad - c_len, cy + b_pad, fill=t["secondary"], width=2)
        self.bio_canvas.create_line(cx + b_pad, cy + b_pad, cx + b_pad, cy + b_pad - c_len, fill=t["secondary"], width=2)

        head_pts = [
            cx, cy - 80,
            cx + 45, cy - 50,
            cx + 52, cy,
            cx + 38, cy + 50,
            cx + 18, cy + 78,
            cx, cy + 85,
            cx - 18, cy + 78,
            cx - 38, cy + 50,
            cx - 52, cy,
            cx - 45, cy - 50
        ]
        self.bio_canvas.create_polygon(head_pts, fill="", outline="#243452", width=1)

        self.bio_canvas.create_oval(cx - 25, cy - 15, cx - 15, cy - 5, outline=t["secondary"], width=1)
        self.bio_canvas.create_oval(cx + 15, cy - 15, cx + 25, cy - 5, outline=t["secondary"], width=1)
        self.bio_canvas.create_line(cx - 28, cy - 10, cx - 12, cy - 10, fill=t["primary_glow"], width=1)
        self.bio_canvas.create_line(cx + 12, cy - 10, cx + 28, cy - 10, fill=t["primary_glow"], width=1)
        self.bio_canvas.create_line(cx, cy - 15, cx, cy + 15, fill="#2E4366", width=1)
        self.bio_canvas.create_line(cx - 8, cy + 15, cx + 8, cy + 15, fill="#2E4366", width=1)
        self.bio_canvas.create_line(cx - 18, cy + 42, cx + 18, cy + 42, fill=t["secondary"], width=1, dash=(2, 2))

        laser_y = cy - 85 + self.login_laser_y
        self.bio_canvas.create_line(cx - 75, laser_y, cx + 75, laser_y, fill=t["secondary"], width=2)
        self.bio_canvas.create_line(cx - 65, laser_y - (self.login_laser_dir * 3), cx + 65, laser_y - (self.login_laser_dir * 3), fill=t["primary_glow"], width=1)

        self.login_laser_y += self.login_laser_dir * 3
        if self.login_laser_y >= 165 or self.login_laser_y <= 5:
            self.login_laser_dir *= -1

        pct = int(min(99, max(12, (self.login_laser_y / 165.0) * 100)))
        self.bio_canvas.create_text(
            cx, cy + 115,
            text=f"CALIBRATING FACIAL GEOMETRY: {pct}%",
            font=(FONT_CODE, 8, "bold"),
            fill=t["secondary"]
        )

        self.login_scan_timer = self.root.after(35, self.start_login_animation)

    def stop_login_animation(self):
        if self.login_scan_timer:
            self.root.after_cancel(self.login_scan_timer)
            self.login_scan_timer = None

    def authenticate(self):
        user = self.user_entry.get().strip()
        pwd = self.pass_entry.get().strip()

        if user and pwd == "1234":
            self.stop_login_animation()
            self.current_officer = user
            self.login_frame.pack_forget()
            self.create_dashboard(user)
        else:
            self.login_error_lbl.config(text="⚠️ ACCESS DENIED: Invalid Security Keycode or Identifier.")
            threading.Thread(target=lambda: winsound.Beep(900, 150), daemon=True).start()

    def create_dashboard(self, officer_name):
        t = self.theme
        self.dash_frame = tk.Frame(self.root, bg=t["bg_root"])
        self.dash_frame.pack(fill="both", expand=True)

        navbar = tk.Frame(self.dash_frame, bg=t["panel_bg"], height=62, highlightbackground=t["card_border"], highlightthickness=1)
        navbar.pack(fill="x")
        navbar.pack_propagate(False)

        brand_frame = tk.Frame(navbar, bg=t["panel_bg"])
        brand_frame.pack(side="left", padx=20, fill="y")

        s_canvas = tk.Canvas(brand_frame, width=24, height=24, bg=t["panel_bg"], highlightthickness=0)
        s_canvas.pack(side="left", padx=(0, 8))
        s_pts = [12, 2, 22, 6, 22, 14, 12, 22, 2, 14, 2, 6]
        s_canvas.create_polygon(s_pts, fill=t["card_bg"], outline=t["primary"], width=2)
        s_canvas.create_line(12, 5, 12, 19, fill=t["primary_glow"], width=1)

        tk.Label(brand_frame, text="VISIONSHIELD PRO", font=(FONT_MAIN, 13, "bold"), fg=t["text_primary"], bg=t["panel_bg"]).pack(side="left")

        ver_badge = tk.Frame(brand_frame, bg=t["card_bg"], padx=6, pady=2, highlightbackground=t["card_border"], highlightthickness=1)
        ver_badge.pack(side="left", padx=10)
        tk.Label(ver_badge, text="v2.5 TACTICAL", font=(FONT_MAIN, 8, "bold"), fg=t["secondary"], bg=t["card_bg"]).pack()

        center_box = tk.Frame(navbar, bg=t["panel_bg"])
        center_box.pack(side="left", expand=True)

        self.clock_lbl = tk.Label(center_box, text="", font=(FONT_CODE, 10, "bold"), fg=t["secondary"], bg=t["panel_bg"])
        self.clock_lbl.pack(side="left", padx=16)
        self.update_clock()

        stat_pill = tk.Frame(center_box, bg=t["card_bg"], padx=10, pady=3, highlightbackground=t["card_border"], highlightthickness=1)
        stat_pill.pack(side="left")
        tk.Label(stat_pill, text="● SENSORS ACTIVE & ARMED", font=(FONT_MAIN, 8, "bold"), fg=t["success"], bg=t["card_bg"]).pack()

        right_bar = tk.Frame(navbar, bg=t["panel_bg"])
        right_bar.pack(side="right", padx=18)

        theme_pills_frame = tk.Frame(right_bar, bg=t["card_bg"], highlightbackground=t["card_border"], highlightthickness=1, padx=2, pady=2)
        theme_pills_frame.pack(side="left", padx=(0, 16))

        for key, info in [("indigo", "Indigo"), ("cyber_teal", "Teal"), ("obsidian_gold", "Gold")]:
            is_active = (key == CURRENT_THEME_KEY)
            p_bg = t["primary"] if is_active else t["card_bg"]
            p_fg = "#FFFFFF" if is_active else t["text_muted"]
            
            p_btn = tk.Button(
                theme_pills_frame,
                text=info,
                font=(FONT_MAIN, 8, "bold"),
                bg=p_bg,
                fg=p_fg,
                activebackground=t["primary_hover"],
                activeforeground="#FFFFFF",
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda k=key: self.apply_theme(k)
            )
            p_btn.pack(side="left", padx=2, ipady=2, ipadx=6)

        officer_box = tk.Frame(right_bar, bg=t["card_bg"], padx=10, pady=4, highlightbackground=t["card_border"], highlightthickness=1)
        officer_box.pack(side="left", padx=(0, 12))

        tk.Label(officer_box, text=f"OPERATOR: {officer_name.upper()}", font=(FONT_MAIN, 8, "bold"), fg=t["text_primary"], bg=t["card_bg"]).pack()

        disconnect_btn = create_luxury_button(
            right_bar,
            text="DISCONNECT",
            bg=t["alert"],
            hover_bg=t["alert_hover"],
            font=(FONT_MAIN, 8, "bold"),
            command=self.logout
        )
        disconnect_btn.pack(side="left", ipadx=8, ipady=3)

        main_content = tk.Frame(self.dash_frame, bg=t["bg_root"])
        main_content.pack(fill="both", expand=True, padx=16, pady=14)

        left_col = tk.Frame(main_content, bg=t["bg_root"], width=310)
        left_col.pack(side="left", fill="y", padx=(0, 14))
        left_col.pack_propagate(False)

        cmd_card = create_card(left_col, title="Surveillance Command", theme=t)
        cmd_card.pack(fill="x", pady=(0, 12))

        self.start_btn = create_luxury_button(
            cmd_card,
            text="▶   INITIALIZE CAMERA FEED",
            bg=t["primary"],
            hover_bg=t["primary_hover"],
            font=(FONT_MAIN, 9, "bold"),
            command=self.toggle_camera
        )
        self.start_btn.pack(fill="x", padx=14, pady=5, ipady=6)

        reg_btn = create_luxury_button(
            cmd_card,
            text="➕   ENROLL SUSPECT PROFILE",
            bg=t["card_border"],
            hover_bg=t["panel_bg"],
            fg=t["text_primary"],
            font=(FONT_MAIN, 9, "bold"),
            command=self.open_register_modal
        )
        reg_btn.pack(fill="x", padx=14, pady=5, ipady=6)

        snap_btn = create_luxury_button(
            cmd_card,
            text="📸   RECORD EVIDENCE SNAP",
            bg=t["card_border"],
            hover_bg=t["panel_bg"],
            fg=t["text_primary"],
            font=(FONT_MAIN, 9, "bold"),
            command=self.save_snapshot
        )
        snap_btn.pack(fill="x", padx=14, pady=(5, 14), ipady=6)

        sens_card = create_card(left_col, title="Matching Sensitivity Cutoff", theme=t)
        sens_card.pack(fill="x", pady=(0, 12))

        slider_head = tk.Frame(sens_card, bg=t["card_bg"])
        slider_head.pack(fill="x", padx=14, pady=(0, 4))

        tk.Label(slider_head, text="Cosine Similarity Threshold:", font=(FONT_MAIN, 8), fg=t["text_muted"], bg=t["card_bg"]).pack(side="left")
        self.thresh_badge = tk.Label(slider_head, text="52%", font=(FONT_CODE, 9, "bold"), fg=t["primary_glow"], bg=t["input_bg"], padx=6, pady=1)
        self.thresh_badge.pack(side="right")

        self.modern_slider = ModernCanvasSlider(
            sens_card,
            from_=30,
            to=85,
            initial=52,
            width=260,
            height=28,
            bg=t["card_bg"],
            active_color=t["primary"],
            command=self.on_thresh_change
        )
        self.modern_slider.pack(padx=14, pady=(2, 12))

        motion_card = create_card(left_col, title="Behavioral Agitation Sensor", theme=t)
        motion_card.pack(fill="x", pady=(0, 12))

        gauge_header = tk.Frame(motion_card, bg=t["card_bg"])
        gauge_header.pack(fill="x", padx=14, pady=(0, 6))

        self.motion_status_dot = tk.Label(gauge_header, text="●", font=(FONT_MAIN, 10), fg=t["success"], bg=t["card_bg"])
        self.motion_status_dot.pack(side="left", padx=(0, 6))

        self.motion_val_label = tk.Label(gauge_header, text="PACIFIED (0%)", font=(FONT_MAIN, 11, "bold"), fg=t["success"], bg=t["card_bg"])
        self.motion_val_label.pack(side="left")

        self.telemetry_canvas = tk.Canvas(motion_card, width=260, height=14, bg=t["input_bg"], highlightthickness=0)
        self.telemetry_canvas.pack(padx=14, pady=(0, 8))
        self.draw_telemetry_bar(0)

        self.motion_desc_lbl = tk.Label(
            motion_card,
            text="Head kinetic trajectory is within peaceful baseline.",
            font=(FONT_MAIN, 8),
            fg=t["text_dim"],
            bg=t["card_bg"]
        )
        self.motion_desc_lbl.pack(pady=(0, 12))

        # ==================== BIOMETRIC DATABASE CARD (ENHANCED) ====================
        db_card = create_card(left_col, title="Biometric Suspects Roster", theme=t)
        db_card.pack(fill="x")

        db_row = tk.Frame(db_card, bg=t["card_bg"])
        db_row.pack(fill="x", padx=14, pady=(0, 4))

        tk.Label(db_row, text="🗄️", font=(FONT_MAIN, 16), bg=t["card_bg"]).pack(side="left", padx=(0, 8))
        self.db_label = tk.Label(
            db_row,
            text=f"{len(self.ai.suspect_profiles)} Wanted Criminals",
            font=(FONT_MAIN, 11, "bold"),
            fg=t["secondary"],
            bg=t["card_bg"]
        )
        self.db_label.pack(side="left")

        # View Suspects List Modal Button
        view_suspects_btn = create_luxury_button(
            db_card,
            text="📜  View All Registered Suspects",
            bg=t["panel_bg"],
            hover_bg=t["card_border"],
            fg=t["secondary"],
            font=(FONT_MAIN, 8, "bold"),
            command=self.open_suspects_roster_modal
        )
        view_suspects_btn.pack(fill="x", padx=14, pady=(2, 6), ipady=3)

        open_folder_btn = tk.Button(
            db_card,
            text="📂  Open Dataset Directory",
            font=(FONT_MAIN, 8),
            fg=t["text_muted"],
            bg=t["card_bg"],
            activebackground=t["panel_bg"],
            activeforeground=t["text_primary"],
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda: os.startfile(DATASET_PATH) if os.path.exists(DATASET_PATH) else None
        )
        open_folder_btn.pack(anchor="w", padx=14, pady=(0, 10))

        center_col = tk.Frame(main_content, bg=t["card_bg"], highlightbackground=t["card_border"], highlightthickness=1)
        center_col.pack(side="left", fill="both", expand=True, padx=(0, 14))

        vid_header = tk.Frame(center_col, bg=t["panel_bg"], height=42)
        vid_header.pack(fill="x")
        vid_header.pack_propagate(False)

        self.rec_indicator = tk.Label(
            vid_header,
            text="● SENSOR STANDBY",
            font=(FONT_MAIN, 8, "bold"),
            fg=t["text_dim"],
            bg=t["panel_bg"]
        )
        self.rec_indicator.pack(side="left", padx=16)

        tk.Label(
            vid_header,
            text="PRIMARY SURVEILLANCE FEED [SECTOR-01]",
            font=(FONT_MAIN, 8, "bold"),
            fg=t["text_primary"],
            bg=t["panel_bg"]
        ).pack(side="left")

        # Telemetry with Live Suspect Counts
        self.feed_telemetry_lbl = tk.Label(
            vid_header,
            text="FPS: 0  |  FACES: 0  |  WANTED: 0",
            font=(FONT_CODE, 8, "bold"),
            fg=t["text_dim"],
            bg=t["panel_bg"]
        )
        self.feed_telemetry_lbl.pack(side="right", padx=16)

        self.display_container = tk.Frame(center_col, bg="#05080E")
        self.display_container.pack(fill="both", expand=True, padx=8, pady=8)

        self.radar_canvas = tk.Canvas(self.display_container, bg="#05080E", highlightthickness=0)
        self.radar_canvas.pack(fill="both", expand=True)

        self.video_view = tk.Label(self.display_container, bg="#05080E")

        self.start_radar_animation()

        right_col = tk.Frame(main_content, bg=t["bg_root"], width=340)
        right_col.pack(side="right", fill="y")
        right_col.pack_propagate(False)

        self.dossier_card = create_card(right_col, title="Threat Intelligence Dossier", theme=t)
        self.dossier_card.pack(fill="x", pady=(0, 12))

        self.target_status_badge = tk.Frame(self.dossier_card, bg=t["panel_bg"], pady=6)
        self.target_status_badge.pack(fill="x", padx=12, pady=(0, 8))

        self.target_status = tk.Label(
            self.target_status_badge,
            text="● ALL SECTORS CLEAR",
            font=(FONT_MAIN, 9, "bold"),
            fg=t["success"],
            bg=t["panel_bg"]
        )
        self.target_status.pack()

        mug_wrapper = tk.Frame(self.dossier_card, bg=t["card_bg"])
        mug_wrapper.pack(pady=4)

        self.mugshot_container = tk.Frame(
            mug_wrapper,
            bg=t["input_bg"],
            width=100,
            height=100,
            highlightbackground=t["card_border"],
            highlightthickness=1
        )
        self.mugshot_container.pack()
        self.mugshot_container.pack_propagate(False)

        self.mugshot_label = tk.Label(
            self.mugshot_container,
            text="SCANNING\nFEED...",
            font=(FONT_CODE, 8),
            fg=t["text_dim"],
            bg=t["input_bg"]
        )
        self.mugshot_label.pack(fill="both", expand=True)

        details_box = tk.Frame(self.dossier_card, bg=t["card_bg"])
        details_box.pack(fill="x", padx=14, pady=6)

        self.target_name = tk.Label(
            details_box,
            text="Subject: Standing by...",
            font=(FONT_MAIN, 11, "bold"),
            fg=t["text_primary"],
            bg=t["card_bg"]
        )
        self.target_name.pack(anchor="w")

        self.target_fir = tk.Label(
            details_box,
            text="Case / FIR: None Active",
            font=(FONT_CODE, 8),
            fg=t["secondary"],
            bg=t["card_bg"]
        )
        self.target_fir.pack(anchor="w", pady=(2, 0))

        self.target_crime = tk.Label(
            details_box,
            text="Status: Optical surveillance active. No warrants detected.",
            font=(FONT_MAIN, 8),
            fg=t["text_muted"],
            bg=t["card_bg"],
            wraplength=280,
            justify="left"
        )
        self.target_crime.pack(anchor="w", pady=(2, 0))

        self.conf_bar_frame = tk.Frame(details_box, bg=t["card_bg"])
        self.conf_bar_frame.pack(fill="x", pady=(8, 4))

        self.target_conf_lbl = tk.Label(
            self.conf_bar_frame,
            text="Confidence Match: 0%",
            font=(FONT_MAIN, 8, "bold"),
            fg=t["text_dim"],
            bg=t["card_bg"]
        )
        self.target_conf_lbl.pack(anchor="w")

        log_card = create_card(right_col, title="Real-Time Event Audit Log", theme=t)
        log_card.pack(fill="both", expand=True)

        log_scroll_frame = tk.Frame(log_card, bg=t["input_bg"], highlightbackground=t["card_border"], highlightthickness=1)
        log_scroll_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.log_box = tk.Text(
            log_scroll_frame,
            bg=t["input_bg"],
            fg=t["text_muted"],
            font=(FONT_CODE, 8),
            bd=0,
            relief="flat",
            wrap="word",
            insertbackground=t["secondary"]
        )
        self.log_box.pack(side="left", fill="both", expand=True, padx=8, pady=8)

        self.log_box.tag_config("time", foreground=t["secondary"])
        self.log_box.tag_config("alert", foreground=t["alert"], font=(FONT_CODE, 8, "bold"))
        self.log_box.tag_config("warn", foreground=t["warning"])
        self.log_box.tag_config("ok", foreground=t["success"])

        self.append_log(f"Session linked: Operator {officer_name}", tag="ok")
        self.append_log(f"Biometric DB loaded: {len(self.ai.suspect_profiles)} profiles active.", tag="time")

    def open_suspects_roster_modal(self):
        """Displays a clean modal list showing all suspicious persons loaded in the database."""
        t = self.theme
        modal = tk.Toplevel(self.root)
        modal.title("Registered Suspects Directory")
        modal.geometry("520x460")
        modal.configure(bg=t["bg_root"])
        modal.grab_set()

        head = tk.Frame(modal, bg=t["panel_bg"], pady=12, highlightbackground=t["card_border"], highlightthickness=1)
        head.pack(fill="x")
        tk.Label(head, text=f"SUSPECT DATABASE ROSTER ({len(self.ai.suspect_profiles)} PROFILES)", font=(FONT_MAIN, 11, "bold"), fg=t["secondary"], bg=t["panel_bg"]).pack()

        content = tk.Frame(modal, bg=t["bg_root"], padx=14, pady=12)
        content.pack(fill="both", expand=True)

        list_card = tk.Frame(content, bg=t["input_bg"], highlightbackground=t["card_border"], highlightthickness=1)
        list_card.pack(fill="both", expand=True)

        scroll = tk.Scrollbar(list_card)
        scroll.pack(side="right", fill="y")

        suspect_listbox = tk.Text(list_card, bg=t["input_bg"], fg=t["text_primary"], font=(FONT_CODE, 9), bd=0, yscrollcommand=scroll.set, padx=10, pady=10)
        suspect_listbox.pack(fill="both", expand=True)
        scroll.config(command=suspect_listbox.yview)

        suspect_listbox.tag_config("header", foreground=t["primary_glow"], font=(FONT_CODE, 9, "bold"))
        suspect_listbox.tag_config("name", foreground="#FFFFFF", font=(FONT_CODE, 10, "bold"))
        suspect_listbox.tag_config("detail", foreground=t["text_muted"])
        suspect_listbox.tag_config("badge", foreground=t["alert"], font=(FONT_CODE, 9, "bold"))

        if not self.ai.suspect_profiles:
            suspect_listbox.insert("end", "\nNo suspect biometric records currently loaded.\nUse 'Enroll Suspect Profile' to register.\n")
        else:
            suspect_listbox.insert("end", f" {'#':<3} | {'NAME':<18} | {'FIR / CASE ID':<14} | {'TEMPLATES'}\n", "header")
            suspect_listbox.insert("end", "-" * 56 + "\n")
            for idx, (name, data) in enumerate(self.ai.suspect_profiles.items(), start=1):
                tpl_count = len(data["templates"])
                suspect_listbox.insert("end", f" {idx:<3} | ", "detail")
                suspect_listbox.insert("end", f"{name:<18}", "name")
                suspect_listbox.insert("end", f" | {data['fir']:<14} | ", "detail")
                suspect_listbox.insert("end", f"{tpl_count} samples\n", "badge")
                suspect_listbox.insert("end", f"      Charges: {data['crime']}\n\n", "detail")

        suspect_listbox.config(state="disabled")

        close_btn = create_luxury_button(content, text="CLOSE DIRECTORY", bg=t["card_border"], hover_bg=t["panel_bg"], fg="#FFFFFF", font=(FONT_MAIN, 9, "bold"), command=modal.destroy)
        close_btn.pack(fill="x", pady=(10, 0), ipady=4)

    def start_radar_animation(self):
        if self.is_running:
            return

        w = self.radar_canvas.winfo_width()
        h = self.radar_canvas.winfo_height()

        if w > 10 and h > 10:
            cx, cy = w // 2, h // 2
            max_r = min(cx, cy) - 30
            t = self.theme

            self.radar_canvas.delete("all")

            self.radar_canvas.create_line(cx - max_r, cy, cx + max_r, cy, fill="#121D2C", width=1, dash=(4, 4))
            self.radar_canvas.create_line(cx, cy - max_r, cx, cy + max_r, fill="#121D2C", width=1, dash=(4, 4))

            for step in [0.25, 0.5, 0.75, 1.0]:
                r = int(max_r * step)
                self.radar_canvas.create_oval(cx - r, cy - r, cx + r, cy + r, outline=t["radar_circle"], width=1)

            rad = math.radians(self.radar_angle)
            sweep_x = cx + max_r * math.cos(rad)
            sweep_y = cy + max_r * math.sin(rad)
            self.radar_canvas.create_line(cx, cy, sweep_x, sweep_y, fill=t["radar_sweep"], width=2)

            self.radar_canvas.create_oval(cx - 4, cy - 4, cx + 4, cy + 4, fill=t["primary_glow"], outline="")

            self.radar_canvas.create_text(
                cx, cy + max_r + 14,
                text="OPTICAL SENSOR IN STANDBY  •  AWAITING ACTIVATION",
                font=(FONT_CODE, 9, "bold"),
                fill=t["text_muted"]
            )

            self.radar_angle = (self.radar_angle + 4) % 360

        self.radar_timer = self.root.after(40, self.start_radar_animation)

    def stop_radar_animation(self):
        if self.radar_timer:
            self.root.after_cancel(self.radar_timer)
            self.radar_timer = None

    def draw_telemetry_bar(self, score):
        self.telemetry_canvas.delete("all")
        t = self.theme
        total_segments = 20
        active_segments = int(round((score / 100.0) * total_segments))
        seg_w = 11
        seg_gap = 2

        for i in range(total_segments):
            x1 = 2 + i * (seg_w + seg_gap)
            x2 = x1 + seg_w
            
            if i < active_segments:
                if score > 50:
                    col = t["warning"]
                elif score > 75:
                    col = t["alert"]
                else:
                    col = t["success"]
            else:
                col = "#152033"

            self.telemetry_canvas.create_rectangle(x1, 2, x2, 12, fill=col, width=0)

    def update_clock(self):
        if hasattr(self, 'clock_lbl') and self.clock_lbl.winfo_exists():
            now_str = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
            self.clock_lbl.config(text=now_str)
            self.root.after(1000, self.update_clock)

    def append_log(self, text, tag="time"):
        if hasattr(self, 'log_box') and self.log_box.winfo_exists():
            ts = datetime.now().strftime('%H:%M:%S')
            self.log_box.insert("end", f"[{ts}] ", "time")
            self.log_box.insert("end", f"{text}\n", tag)
            self.log_box.see("end")

    def on_thresh_change(self, val):
        self.match_threshold = float(val) / 100.0
        if hasattr(self, 'thresh_badge'):
            self.thresh_badge.config(text=f"{int(val)}%")

    def toggle_camera(self):
        t = self.theme
        if not self.is_running:
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not self.cap.isOpened():
                self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Hardware Error", "Could not connect to camera hardware or driver.")
                return

            self.is_running = True
            self.stop_radar_animation()
            self.radar_canvas.pack_forget()
            self.video_view.pack(fill="both", expand=True)

            self.start_btn.config(text="⏹   HALT CAMERA FEED", bg=t["alert"], activebackground=t["alert_hover"])
            self.rec_indicator.config(text="● SENSOR LIVE REC", fg=t["alert"])
            self.append_log("Optical link established. Real-time biometrics active.", tag="ok")
            self.update_feed()
        else:
            self.is_running = False
            if self.cap:
                self.cap.release()
                self.cap = None

            self.video_view.pack_forget()
            self.radar_canvas.pack(fill="both", expand=True)
            self.start_radar_animation()

            self.start_btn.config(text="▶   INITIALIZE CAMERA FEED", bg=t["primary"], activebackground=t["primary_hover"])
            self.rec_indicator.config(text="● SENSOR STANDBY", fg=t["text_dim"])
            self.append_log("Optical link closed by operator.", tag="warn")

    def draw_hud_brackets(self, frame, x, y, w, h, color, label, sub_label=None):
        line_len = int(min(w, h) * 0.25)
        thickness = 2

        cv2.line(frame, (x, y), (x + line_len, y), color, thickness)
        cv2.line(frame, (x, y), (x, y + line_len), color, thickness)
        cv2.line(frame, (x + w, y), (x + w - line_len, y), color, thickness)
        cv2.line(frame, (x + w, y), (x + w, y + line_len), color, thickness)
        cv2.line(frame, (x, y + h), (x + line_len, y + h), color, thickness)
        cv2.line(frame, (x, y + h), (x, y + h - line_len), color, thickness)
        cv2.line(frame, (x + w, y + h), (x + w - line_len, y + h), color, thickness)
        cv2.line(frame, (x + w, y + h), (x + w, y + h - line_len), color, thickness)

        banner_h = 32 if sub_label else 22
        cv2.rectangle(frame, (x, y - banner_h), (x + w, y), color, -1)
        cv2.putText(frame, label, (x + 6, y - (14 if sub_label else 6)), cv2.FONT_HERSHEY_DUPLEX, 0.46, (255, 255, 255), 1)
        if sub_label:
            cv2.putText(frame, sub_label, (x + 6, y - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (240, 240, 240), 1)

    def update_feed(self):
        if not self.is_running or self.cap is None:
            return

        ret, frame = self.cap.read()
        if not ret:
            self.root.after(15, self.update_feed)
            return

        t = self.theme

        self.fps_counter += 1
        now_time = time.time()
        if now_time - self.fps_time >= 1.0:
            self.current_fps = self.fps_counter
            self.fps_counter = 0
            self.fps_time = now_time

        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.ai.face_detector.detectMultiScale(
            gray,
            scaleFactor=1.15,
            minNeighbors=5,
            minSize=(70, 70)
        )

        total_faces_in_frame = len(faces)
        wanted_suspects_in_frame = 0
        jittery_suspects_in_frame = 0
        last_matched_suspect = None
        last_matched_conf = 0.0

        for (x, y, w, h) in faces:
            center_x = x + w // 2
            center_y = y + h // 2
            is_jittery, motion_score = self.ai.analyze_motion_jitter((center_x, center_y))

            self.draw_telemetry_bar(motion_score)

            if is_jittery:
                jittery_suspects_in_frame += 1
                self.motion_status_dot.config(fg=t["warning"])
                self.motion_val_label.config(text=f"RESTLESS ({motion_score}%)", fg=t["warning"])
                self.trigger_motion_alert(motion_score)
            else:
                self.motion_status_dot.config(fg=t["success"])
                self.motion_val_label.config(text=f"PACIFIED ({motion_score}%)", fg=t["success"])

            face_crop = gray[y:y+h, x:x+w]
            if face_crop.shape[0] == 0 or face_crop.shape[1] == 0:
                continue

            match, conf = self.ai.find_match(face_crop, threshold=self.match_threshold)

            if match:
                wanted_suspects_in_frame += 1
                last_matched_suspect = match
                last_matched_conf = conf

                self.draw_hud_brackets(
                    frame, x, y, w, h, t["hud_wanted"],
                    label=f"WANTED: {match['name']} ({conf}%)",
                    sub_label=f"FIR: {match['fir']} | {match['crime']}"
                )
                self.trigger_criminal_alert(match, conf, frame)

            elif is_jittery:
                self.draw_hud_brackets(
                    frame, x, y, w, h, t["hud_jitter"],
                    label=f"SUSPICIOUS JITTER: {motion_score}%",
                    sub_label="Irregular Kinetic Dynamics"
                )

            else:
                self.draw_hud_brackets(
                    frame, x, y, w, h, t["hud_citizen"],
                    label=f"CITIZEN VERIFIED ({conf}%)",
                    sub_label="No Warrants Active"
                )

        # Update Live Counts on Top Right Header
        self.feed_telemetry_lbl.config(
            text=f"FPS: {self.current_fps}  |  FACES: {total_faces_in_frame}  |  WANTED IN FRAME: {wanted_suspects_in_frame}"
        )

        # Update Dossier Badge status based on how many suspects are in frame
        if wanted_suspects_in_frame > 0:
            self.target_status_badge.config(bg="#5B1425")
            self.target_status.config(
                text=f"🚨 CRITICAL: {wanted_suspects_in_frame} WANTED SUSPECT(S) IN FRAME",
                fg="#FECDD3",
                bg="#5B1425"
            )
        elif jittery_suspects_in_frame > 0:
            self.target_status_badge.config(bg="#3D2905")
            self.target_status.config(
                text=f"⚠️ WARNING: {jittery_suspects_in_frame} RESTLESS / SUSPICIOUS IN FRAME",
                fg="#FDE68A",
                bg="#3D2905"
            )
        else:
            self.target_status_badge.config(bg=t["panel_bg"])
            self.target_status.config(text="● ALL SECTORS CLEAR", fg=t["success"], bg=t["panel_bg"])
            self.target_name.config(text="Subject: Standing by...", fg=t["text_primary"])
            self.target_fir.config(text="Case / FIR: None Active")
            self.target_crime.config(text="Status: Optical surveillance active. No warrants detected.")
            self.target_conf_lbl.config(text="Confidence Match: 0%", fg=t["text_dim"])
            self.mugshot_label.config(image="", text="SCANNING\nFEED...")

        disp_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(disp_frame)
        pil_img.thumbnail((840, 520))
        photo = ImageTk.PhotoImage(image=pil_img)

        self.video_view.config(image=photo, text="")
        self.video_view.image = photo

        self.root.after(15, self.update_feed)

    def trigger_criminal_alert(self, match, conf, frame):
        t = self.theme
        now = time.time()
        self.target_name.config(text=f"Suspect: {match['name']}", fg=t["alert"])
        self.target_fir.config(text=f"FIR: {match['fir']}")
        self.target_crime.config(text=f"Charges: {match['crime']}")
        self.target_conf_lbl.config(text=f"Match Confidence: {conf}% (CRITICAL MATCH)", fg=t["alert"])

        if match.get("img_path") and os.path.exists(match["img_path"]):
            try:
                mug = Image.open(match["img_path"])
                mug = mug.resize((100, 100), Image.Resampling.LANCZOS)
                self.mug_photo = ImageTk.PhotoImage(mug)
                self.mugshot_label.config(image=self.mug_photo, text="")
            except Exception:
                self.mugshot_label.config(image="", text="MUGSHOT\nUNAVAILABLE")
        else:
            self.mugshot_label.config(image="", text="MUGSHOT\nUNAVAILABLE")

        if now - self.last_beep_time > 3.0:
            self.last_beep_time = now
            threading.Thread(target=lambda: winsound.Beep(2200, 350), daemon=True).start()
            self.append_log(f"🚨 TARGET MATCH: {match['name']} | Conf: {conf}% | FIR: {match['fir']}", tag="alert")
            
            snap_path = os.path.join(ALERTS_DIR, f"ALERT_{match['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
            cv2.imwrite(snap_path, frame)

    def trigger_motion_alert(self, score):
        now = time.time()
        if now - self.last_motion_alert_time > 4.0:
            self.last_motion_alert_time = now
            threading.Thread(target=lambda: winsound.Beep(1400, 180), daemon=True).start()
            self.append_log(f"⚠️ RESTLESS MOTION: Score {score}% - High evasive movement", tag="warn")

    def open_register_modal(self):
        t = self.theme
        modal = tk.Toplevel(self.root)
        modal.title("Suspect Biometric Enrollment")
        modal.geometry("460x590")
        modal.configure(bg=t["bg_root"])
        modal.resizable(False, False)
        modal.grab_set()

        header = tk.Frame(modal, bg=t["panel_bg"], pady=14, highlightbackground=t["card_border"], highlightthickness=1)
        header.pack(fill="x")
        tk.Label(header, text="BIOMETRIC PROFILE ENROLLMENT", font=(FONT_MAIN, 11, "bold"), fg=t["text_primary"], bg=t["panel_bg"]).pack()

        form = tk.Frame(modal, bg=t["bg_root"], padx=26, pady=16)
        form.pack(fill="both", expand=True)

        def make_field(parent, label_text, default_val=""):
            tk.Label(parent, text=label_text.upper(), font=(FONT_MAIN, 8, "bold"), fg=t["text_muted"], bg=t["bg_root"]).pack(anchor="w", pady=(6, 2))
            box = tk.Frame(parent, bg=t["input_bg"], highlightbackground=t["input_border"], highlightthickness=1)
            box.pack(fill="x", pady=(0, 6))

            entry = tk.Entry(box, font=(FONT_MAIN, 10), bg=t["input_bg"], fg=t["text_primary"], insertbackground=t["secondary"], bd=0, relief="flat")
            entry.insert(0, default_val)
            entry.pack(fill="x", ipady=6, padx=8)
            return entry

        name_e = make_field(form, "Suspect Full Name", "")
        fir_e = make_field(form, "FIR / Case File Reference", "FIR-2026-")
        crime_e = make_field(form, "Criminal Offense / Category", "Narcotics / Robbery / Wanted")

        tk.Label(form, text="MUGSHOT PHOTO SOURCE", font=(FONT_MAIN, 8, "bold"), fg=t["text_muted"], bg=t["bg_root"]).pack(anchor="w", pady=(8, 2))

        sel = {"path": None}

        preview_box = tk.Frame(form, bg=t["card_bg"], highlightbackground=t["card_border"], highlightthickness=1)
        preview_box.pack(fill="x", pady=(0, 10), ipady=6)

        p_lbl = tk.Label(preview_box, text="No Photo Selected", fg=t["text_dim"], bg=t["card_bg"], font=(FONT_MAIN, 9))
        p_lbl.pack(pady=4)

        def pick():
            f = filedialog.askopenfilename(filetypes=[("Mugshot Images", "*.jpg;*.jpeg;*.png")])
            if f:
                sel["path"] = f
                filename = os.path.basename(f)
                p_lbl.config(text=f"Selected: {filename}", fg=t["secondary"])

        pick_btn = create_luxury_button(
            preview_box,
            text="📁   Browse Mugshot File",
            bg=t["input_border"],
            hover_bg=t["card_border"],
            font=(FONT_MAIN, 8, "bold"),
            command=pick
        )
        pick_btn.pack(ipadx=10, ipady=2, pady=(2, 4))

        def save():
            name = name_e.get().strip()
            fir = fir_e.get().strip()
            crime = crime_e.get().strip()

            if not name or not fir or not crime or not sel["path"]:
                messagebox.showerror("Validation Error", "All fields and a valid mugshot photo are strictly required.")
                return

            dest = os.path.join(DATASET_PATH, f"{name}__{crime}__{fir}.jpg".replace(" ", "_"))
            img = cv2.imread(sel["path"])
            if img is None:
                messagebox.showerror("Read Error", "Could not process selected image file.")
                return

            cv2.imwrite(dest, img)
            
            num = self.ai.load_all_datasets(DATASET_PATH)
            self.db_label.config(text=f"{num} Wanted Criminals")
            self.append_log(f"New suspect enrolled: {name} (FIR: {fir})", tag="ok")
            messagebox.showinfo("Enrollment Complete", f"Suspect '{name}' successfully registered into biometric database.")
            modal.destroy()

        save_btn = create_luxury_button(
            form,
            text="💾   COMMIT BIOMETRIC RECORD",
            bg=t["success"],
            hover_bg=t["success_hover"],
            font=(FONT_MAIN, 9, "bold"),
            command=save
        )
        save_btn.pack(fill="x", ipady=6, pady=(10, 0))

    def save_snapshot(self):
        if self.cap and self.is_running:
            ret, f = self.cap.read()
            if ret:
                f = cv2.flip(f, 1)
                p = os.path.join(ALERTS_DIR, f"SNAP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
                cv2.imwrite(p, f)
                self.append_log(f"Snapshot recorded: {os.path.basename(p)}", tag="time")
                messagebox.showinfo("Snapshot Recorded", f"Evidence frame recorded successfully to:\n{p}")
        else:
            messagebox.showwarning("Feed Offline", "Start camera surveillance before capturing snapshots.")

    def logout(self):
        if self.is_running:
            self.toggle_camera()
        self.stop_radar_animation()
        self.dash_frame.pack_forget()
        self.create_login_screen()

if __name__ == "__main__":
    root = tk.Tk()
    app = VisionShieldApp(root)
    root.mainloop()


    
