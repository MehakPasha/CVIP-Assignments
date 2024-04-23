import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Player")

        # Video capture
        self.cap = None
        self.playing = False
        self.speed = 1.0

        # Canvas to display video
        self.canvas = tk.Canvas(root, width=800, height=600, bg="black")
        self.canvas.pack()

        # Buttons
        self.play_btn = tk.Button(root, text="▶ Play", command=self.play, font=("Helvetica", 12, "bold"), bd=0, bg="lightgray")
        self.play_btn.pack(side=tk.LEFT)
        self.play_btn.focus_set()  # Set focus on play button by default

        self.pause_btn = tk.Button(root, text="⏸ Pause", command=self.pause, font=("Helvetica", 12, "bold"), bd=0, bg="lightgray")
        self.pause_btn.pack(side=tk.LEFT)
        self.pause_btn.config(state=tk.DISABLED)

        self.speed_btn = tk.Button(root, text="⏩ Speed x1", command=self.change_speed, font=("Helvetica", 12, "bold"), bd=0, bg="lightgray")
        self.speed_btn.pack(side=tk.LEFT)

        self.open_btn = tk.Button(root, text="Open Video", command=self.open_video, font=("Helvetica", 12, "bold"), bd=0, bg="lightgray")
        self.open_btn.pack(side=tk.LEFT)

        self.camera_btn = tk.Button(root, text="Camera", command=self.open_camera, font=("Helvetica", 12, "bold"), bd=0, bg="lightgray")
        self.camera_btn.pack(side=tk.LEFT)

        # Progress bar
        self.progress_bar = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.seek_video, sliderlength=20, length=600)
        self.progress_bar.pack()

        # FPS Label
        self.fps_label = tk.Label(root, text="FPS: ", font=("Helvetica", 12))
        self.fps_label.pack()

    def open_video(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.cap = cv2.VideoCapture(file_path)
            self.play_video()

    def open_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.play_video()

    def play(self):
        self.playing = True
        self.pause_btn.config(state=tk.NORMAL)
        self.play_btn.config(state=tk.DISABLED)
        self.play_video()

    def pause(self):
        self.playing = False
        self.pause_btn.config(state=tk.DISABLED)
        self.play_btn.config(state=tk.NORMAL)

    def play_video(self):
        ret, frame = self.cap.read()
        if ret:
            filter_name = "blur"  # Change this to apply different filters
            filtered_frame = apply_filter(filter_name, frame)

            # Convert the filtered frame to RGB for display
            filtered_frame_rgb = cv2.cvtColor(filtered_frame, cv2.COLOR_BGR2RGB)

            # Convert the frame to an ImageTk format
            img = Image.fromarray(filtered_frame_rgb)
            img = ImageTk.PhotoImage(img)

            # Display the frame on the canvas
            self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
            self.canvas.img = img

            # Display FPS
            fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            self.fps_label.config(text="FPS: {}".format(fps))

            # Update progress bar
            total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            progress = (current_frame / total_frames) * 100
            self.progress_bar.set(progress)

            # Update at 30 FPS
            if self.playing:
                self.root.after(int(1000 / fps), self.play_video)

            # Adjust speed
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame + self.speed)

    def change_speed(self):
        if self.speed == 1.0:
            self.speed = 2.0
            self.speed_btn.config(text="⏩ Speed x2")
        elif self.speed == 2.0:
            self.speed = 0.5
            self.speed_btn.config(text="⏩ Speed x0.5")
        else:
            self.speed = 1.0
            self.speed_btn.config(text="⏩ Speed x1")

    def seek_video(self, value):
        if self.cap:
            total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            target_frame = int((float(value) / 100) * total_frames)
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)

# Filters and filter functions
filters_func = {
    "blur": cv2.blur,
    "boxFilter": cv2.boxFilter,
    "erode": cv2.erode,
    "dilate": cv2.dilate,
    "GaussianBlur": cv2.GaussianBlur,
    "filter2D": cv2.filter2D,
    "Sobel": cv2.Sobel,
    "Laplacian": cv2.Laplacian,
    "dft": cv2.dft,
    "getRotationMatrix2D": cv2.getRotationMatrix2D,
    "warpAffine": cv2.warpAffine,
}

# Filters and filter functions
def apply_filter(filter_name, frame):
    dtype = np.float64
    ksize = 3
    scale = 1
    delta = 0
    borderType = cv2.BORDER_DEFAULT

    filter_function = filters_func.get(filter_name, None)

    if filter_function is not None:
        if filter_name == "blur":
            return filter_function(frame, (ksize, ksize))
        elif filter_name == "boxFilter":
            return filter_function(frame, -1, (ksize, ksize), normalize=True, borderType=borderType)
        elif filter_name == "GaussianBlur":
            return filter_function(frame, (ksize, ksize), sigmaX=0)
        elif filter_name == "Sobel":
            return filter_function(frame, cv2.CV_64F, 1, 0, ksize=3)
        elif filter_name == "Laplacian":
            ddepth = cv2.CV_64F
            return filter_function(frame, ddepth, ksize=3)
        elif filter_name == "dilate":
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (ksize, ksize))
            anchor = (-1, -1)
            return filter_function(frame, kernel, anchor=anchor, iterations=1)
        elif filter_name == "erode":
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (ksize, ksize))
            anchor = (-1, -1)
            return filter_function(frame, kernel, anchor=anchor, iterations=1)
        elif filter_name == "filter2D":
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (ksize, ksize))
            anchor = (-1, -1)
            return filter_function(frame, cv2.CV_64F, kernel, anchor=anchor)
        elif filter_name == "dft":
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            return filter_function(frame.astype(dtype), flags=cv2.DFT_COMPLEX_OUTPUT)
        elif filter_name == "getRotationMatrix2D":
            center = (frame.shape[1] // 2, frame.shape[0] // 2)
            angle = 30
            scale = 1.0
            return filter_function(center, angle, scale)
        elif filter_name == "warpAffine":
            M = np.float32([[1, 0, 50], [0, 1, 50]])
            return filter_function(frame, M, (frame.shape[1], frame.shape[0]))
        else:
            return filter_function(frame, dtype, ksize, scale, delta, borderType)
    
    return None

root = tk.Tk()
app = VideoPlayer(root)
root.mainloop()
