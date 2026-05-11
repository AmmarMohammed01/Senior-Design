"""
Merged Tkinter UI for PCB Quality Checker

Purpose:
- Keeps the existing terminal-menu project logic as the backend.
- Replaces input()/print() menu navigation with buttons, dropdowns, dialogs, and image preview.
- Expected location: place this file at the project root, beside the src/ folder.

Run:
    python pcb_quality_checker_merged_gui.py
"""

from __future__ import annotations

import shutil
import threading
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Existing project modules
from src.processing.ml_detection import run_camera
from src.processing.image_comparison import compare_boards
from src.processing.map_errors import generate_defect_frequency_map
from src.hardware.take_image import take_golden_board_image, take_test_board_image
from src.config import pcb_global_variables as gv
from src.config import select_camera
from src.utils.handle_json import roi_read
from src.scripts.launch_image_labeler import launch_image_labeler


class PCBQualityCheckerGUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("PCB Quality Checker")
        self.geometry("1050x650")
        self.minsize(950, 575)

        self.current_board = tk.StringVar(value="")
        self.current_face = tk.StringVar(value="top")
        self.camera_choice = tk.StringVar(value=getattr(select_camera, "camera_choice", "usb"))
        self.status = tk.StringVar(value="Ready.")
        self.preview_image = None

        self._build_layout()
        self.refresh_boards()

    # ---------- UI layout ----------
    def _build_layout(self) -> None:
        header = ttk.Frame(self, padding=12)
        header.pack(fill="x")

        ttk.Label(header, text="PCB Quality Checker", font=("Arial", 20, "bold")).pack(side="left")
        ttk.Label(header, textvariable=self.status).pack(side="right")

        main = ttk.Frame(self, padding=12)
        main.pack(fill="both", expand=True)

        left = ttk.LabelFrame(main, text="Board Manager", padding=12)
        left.pack(side="left", fill="y", padx=(0, 10))

        ttk.Label(left, text="Existing board types").pack(anchor="w")
        self.board_listbox = tk.Listbox(left, height=15, width=30)
        self.board_listbox.pack(fill="y", expand=False, pady=6)
        self.board_listbox.bind("<<ListboxSelect>>", self.on_board_select)

        ttk.Button(left, text="Refresh Board List", command=self.refresh_boards).pack(fill="x", pady=2)
        ttk.Button(left, text="Add New Board Type", command=self.add_board_type).pack(fill="x", pady=2)
        ttk.Button(left, text="Remove Selected Board", command=self.remove_board_type).pack(fill="x", pady=2)

        selected_box = ttk.LabelFrame(left, text="Selected Setup", padding=8)
        selected_box.pack(fill="x", pady=(12, 0))
        ttk.Label(selected_box, text="Board:").grid(row=0, column=0, sticky="w")
        ttk.Label(selected_box, textvariable=self.current_board).grid(row=0, column=1, sticky="w")
        ttk.Label(selected_box, text="Face:").grid(row=1, column=0, sticky="w")
        ttk.Combobox(selected_box, textvariable=self.current_face, values=["top", "bottom"], state="readonly", width=12).grid(row=1, column=1, sticky="w")
        ttk.Label(selected_box, text="Camera:").grid(row=2, column=0, sticky="w")
        ttk.Combobox(selected_box, textvariable=self.camera_choice, values=["usb", "picam"], state="readonly", width=12).grid(row=2, column=1, sticky="w")

        center = ttk.LabelFrame(main, text="Operations", padding=12)
        center.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ttk.Label(center, text="Capture", font=("Arial", 13, "bold")).pack(anchor="w")
        ttk.Button(center, text="Capture Golden Board Image", command=self.capture_golden_board_image).pack(fill="x", pady=3)
        ttk.Button(center, text="Capture Test Board Image", command=self.capture_test_board_image).pack(fill="x", pady=3)

        ttk.Separator(center).pack(fill="x", pady=10)
        ttk.Label(center, text="Analyze", font=("Arial", 13, "bold")).pack(anchor="w")
        ttk.Button(center, text="Launch Image Labeler", command=self.label_board_type).pack(fill="x", pady=3)
        ttk.Button(center, text="Compare Golden vs Test Image", command=self.compare_images).pack(fill="x", pady=3)
        ttk.Button(center, text="Generate Defect Frequency Map", command=self.generate_frequency_map).pack(fill="x", pady=3)
        ttk.Button(center, text="Run ML Detection", command=self.run_ml_detection).pack(fill="x", pady=3)

        ttk.Separator(center).pack(fill="x", pady=10)
        ttk.Label(center, text="Image Preview", font=("Arial", 13, "bold")).pack(anchor="w")
        ttk.Button(center, text="Preview Golden Image", command=lambda: self.preview_named_image("golden.jpg")).pack(fill="x", pady=3)
        ttk.Button(center, text="Preview Latest Test Image", command=self.preview_latest_test_image).pack(fill="x", pady=3)
        ttk.Button(center, text="Choose Image to Preview", command=self.choose_image_to_preview).pack(fill="x", pady=3)

        right = ttk.LabelFrame(main, text="Preview", padding=12)
        right.pack(side="left", fill="both", expand=True)
        self.preview_label = ttk.Label(right, text="No image loaded", anchor="center")
        self.preview_label.pack(fill="both", expand=True)

    # ---------- Helpers ----------
    def set_status(self, message: str) -> None:
        self.status.set(message)
        self.update_idletasks()

    def selected_board_dir(self) -> Path | None:
        board = self.current_board.get().strip()
        if not board:
            messagebox.showwarning("No Board Selected", "Select a board type first.")
            return None
        board_dir = gv.BOARDS_DIR / board
        if not board_dir.exists():
            messagebox.showerror("Board Not Found", f"Board folder was not found:\n{board_dir}")
            return None
        gv.board_type = board
        gv.selected_board_dir = board_dir
        return board_dir

    def selected_face_dir(self) -> Path | None:
        board_dir = self.selected_board_dir()
        if board_dir is None:
            return None
        face = self.current_face.get().lower().strip()
        face_dir = board_dir / face
        if not face_dir.exists():
            messagebox.showerror("Face Folder Not Found", f"Expected folder was not found:\n{face_dir}")
            return None
        return face_dir

    def run_in_thread(self, task, success_message: str = "Done.") -> None:
        def wrapper():
            try:
                self.set_status("Running...")
                task()
                self.set_status(success_message)
            except Exception as err:
                self.set_status("Error.")
                messagebox.showerror("Operation Failed", str(err))

        threading.Thread(target=wrapper, daemon=True).start()

    # ---------- Board manager ----------
    def refresh_boards(self) -> None:
        self.board_listbox.delete(0, tk.END)
        gv.BOARDS_DIR.mkdir(parents=True, exist_ok=True)
        boards = sorted([p.name for p in gv.BOARDS_DIR.iterdir() if p.is_dir()])
        for board in boards:
            self.board_listbox.insert(tk.END, board)
        self.set_status(f"Loaded {len(boards)} board type(s).")

    def on_board_select(self, _event=None) -> None:
        selection = self.board_listbox.curselection()
        if selection:
            board = self.board_listbox.get(selection[0])
            self.current_board.set(board)
            gv.board_type = board
            gv.selected_board_dir = gv.BOARDS_DIR / board
            self.set_status(f"Selected board: {board}")

    def add_board_type(self) -> None:
        board_name = simpledialog.askstring("Add Board Type", "Enter new board name:")
        if not board_name:
            return
        board_name = board_name.strip()
        new_board_dir = gv.BOARDS_DIR / board_name
        try:
            (new_board_dir / "top").mkdir(parents=True, exist_ok=False)
            (new_board_dir / "bottom").mkdir(parents=True, exist_ok=False)
            self.refresh_boards()
            self.current_board.set(board_name)
            messagebox.showinfo("Success", f"Board '{board_name}' folder was created.")
        except FileExistsError:
            messagebox.showerror("Duplicate Board", f"The board name '{board_name}' is already in use.")

    def remove_board_type(self) -> None:
        board_dir = self.selected_board_dir()
        if board_dir is None:
            return
        board = self.current_board.get()
        if messagebox.askyesno("Confirm Delete", f"Remove board '{board}' and all related images/data?"):
            shutil.rmtree(board_dir)
            self.current_board.set("")
            self.refresh_boards()
            messagebox.showinfo("Removed", f"Board '{board}' was deleted.")

    # ---------- Operations ----------
    def capture_golden_board_image(self) -> None:
        board_dir = self.selected_board_dir()
        if board_dir is None:
            return
        select_camera.camera_choice = self.camera_choice.get()

        def task():
            # Matches terminal-menu behavior: capture both top and bottom golden images.
            take_golden_board_image(board_dir, "top")
            take_golden_board_image(board_dir, "bottom")

        self.run_in_thread(task, "Golden board image captured.")

    def capture_test_board_image(self) -> None:
        board_dir = self.selected_board_dir()
        if board_dir is None:
            return
        top_roi = board_dir / "top" / "roi.json"
        bottom_roi = board_dir / "bottom" / "roi.json"
        if not top_roi.exists() or not bottom_roi.exists():
            messagebox.showerror("Missing Golden ROI", "Capture golden board images and ROI for top/bottom before test images.")
            return
        select_camera.camera_choice = self.camera_choice.get()

        def task():
            # Matches terminal-menu behavior: capture both top and bottom test images.
            take_test_board_image(board_dir, "top")
            take_test_board_image(board_dir, "bottom")

        self.run_in_thread(task, "Test board image captured.")

    def label_board_type(self) -> None:
        face_dir = self.selected_face_dir()
        if face_dir is None:
            return
        golden = face_dir / "golden.jpg"
        if not golden.exists():
            messagebox.showerror("Missing Golden Image", f"Golden image was not found:\n{golden}")
            return
        self.run_in_thread(lambda: launch_image_labeler(golden), "Image labeler closed.")

    def compare_images(self) -> None:
        face_dir = self.selected_face_dir()
        if face_dir is None:
            return
        golden = face_dir / "golden.jpg"
        if not golden.exists():
            messagebox.showerror("Missing Golden Image", f"Golden image was not found:\n{golden}")
            return
        test_name = simpledialog.askstring("Test Image", "Enter test image filename, example: test1.jpg")
        if not test_name:
            return
        test_path = face_dir / test_name.strip()
        if not test_path.exists():
            messagebox.showerror("Missing Test Image", f"Test image was not found:\n{test_path}")
            return
        self.run_in_thread(lambda: compare_boards(golden, test_path), "Comparison complete.")

    def generate_frequency_map(self) -> None:
        face_dir = self.selected_face_dir()
        if face_dir is None:
            return
        golden = face_dir / "golden.jpg"
        next_test = face_dir / "next-test-img-num.json"
        yolo_coords = face_dir / "golden.txt"
        yolo_classes = face_dir / "classes.txt"

        missing = [p.name for p in [golden, next_test, yolo_coords, yolo_classes] if not p.exists()]
        if missing:
            messagebox.showerror("Missing Required Files", "Missing:\n" + "\n".join(missing))
            return

        self.run_in_thread(
            lambda: generate_defect_frequency_map(
                yolo_coordinates_filepath=yolo_coords,
                selected_board_dir=face_dir,
                golden_board_filepath=golden,
                yolo_classes_filepath=yolo_classes,
            ),
            "Frequency map generated.",
        )

    def run_ml_detection(self) -> None:
        face_dir = self.selected_face_dir()
        if face_dir is None:
            return
        model_path = face_dir / "best.pt"
        roi_path = face_dir / "roi.json"
        if not model_path.exists():
            messagebox.showerror("Missing Model", f"Model file was not found:\n{model_path}")
            return
        if not roi_path.exists():
            messagebox.showerror("Missing ROI", f"ROI file was not found:\n{roi_path}")
            return

        def task():
            roi = roi_read(roi_path)
            run_camera(model_path, roi)

        self.run_in_thread(task, "ML detection finished.")

    # ---------- Preview ----------
    def preview_named_image(self, filename: str) -> None:
        face_dir = self.selected_face_dir()
        if face_dir is None:
            return
        self.load_preview(face_dir / filename)

    def preview_latest_test_image(self) -> None:
        face_dir = self.selected_face_dir()
        if face_dir is None:
            return
        test_images = sorted(
            [p for p in face_dir.glob("*.jpg") if p.name.lower().startswith("test")],
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        if not test_images:
            messagebox.showwarning("No Test Images", "No test*.jpg images were found for this board face.")
            return
        self.load_preview(test_images[0])

    def choose_image_to_preview(self) -> None:
        face_dir = self.selected_face_dir()
        if face_dir is None:
            return
        images = sorted([p.name for p in face_dir.glob("*.jpg")])
        if not images:
            messagebox.showwarning("No Images", "No .jpg images were found in this board face folder.")
            return
        image_name = simpledialog.askstring("Choose Image", "Available images:\n" + "\n".join(images) + "\n\nType filename:")
        if image_name:
            self.load_preview(face_dir / image_name.strip())

    def load_preview(self, image_path: Path) -> None:
        if not image_path.exists():
            messagebox.showerror("Image Not Found", f"Image was not found:\n{image_path}")
            return
        if not PIL_AVAILABLE:
            self.preview_label.configure(text=f"Pillow is not installed.\nInstall with: pip install pillow\n\nImage path:\n{image_path}")
            return

        image = Image.open(image_path)
        image.thumbnail((480, 420))
        self.preview_image = ImageTk.PhotoImage(image)
        self.preview_label.configure(image=self.preview_image, text="")
        self.set_status(f"Previewing: {image_path.name}")


if __name__ == "__main__":
    app = PCBQualityCheckerGUI()
    app.mainloop()
