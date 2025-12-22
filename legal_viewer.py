import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

LEGAL_FILES = [
    "LICENSE",
    "README.md",
    "README.txt",
    "CREDITS",
    "AUTHORS",
    "SECURITY.md",
]

UNKNOWN_IMAGE = "unknownimagejpg"  # giữ nguyên tên bạn đang dùng

# ====== RETRO CONFIG ======
BG_COLOR = "#c0c0c0"        # xám Win95
TEXT_BG = "#f0f0f0"
TEXT_FG = "#000000"
RETRO_FONT = ("Courier New", 10)
TITLE_FONT = ("Courier New", 11)


def read_file_safe(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        return f"[Error reading file]\n{e}"


def main():
    root = tk.Tk()
    root.title("PLM Legal & Info Viewer")
    root.geometry("900x600")
    root.configure(bg=BG_COLOR)

    # ====== STYLE (CỐ TÌNH CỔ) ======
    style = ttk.Style()
    style.theme_use("default")

    style.configure(
        "TNotebook",
        background=BG_COLOR,
        borderwidth=2
    )

    style.configure(
        "TNotebook.Tab",
        background="#dcdcdc",
        font=TITLE_FONT,
        padding=[10, 4]
    )

    style.map(
        "TNotebook.Tab",
        background=[("selected", "#f0f0f0")]
    )

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=4, pady=4)

    # ====== LEGAL TABS ======
    found_any = False

    for fname in LEGAL_FILES:
        path = os.path.join(ROOT_DIR, fname)
        if os.path.isfile(path):
            found_any = True

            frame = ttk.Frame(notebook)
            notebook.add(frame, text=fname)

            text = tk.Text(
                frame,
                wrap="word",
                bg=TEXT_BG,
                fg=TEXT_FG,
                font=RETRO_FONT,
                relief="sunken",
                borderwidth=2,
                insertbackground="black"
            )

            text.insert("1.0", read_file_safe(path))
            text.config(state="disabled")
            text.pack(fill="both", expand=True, padx=6, pady=6)

    if not found_any:
        messagebox.showwarning(
            "Warning",
            "No LICENSE / README / related files were found."
        )

    # ====== SECRET / CONTACT TAB ======
    secret_frame = ttk.Frame(notebook)
    notebook.add(secret_frame, text="Contact")

    img_ref = None  # giữ reference tránh GC

    def on_tab_change(event):
        nonlocal img_ref

        if notebook.index("current") != notebook.index(secret_frame):
            return

        for widget in secret_frame.winfo_children():
            widget.destroy()

        img_path = os.path.join(ROOT_DIR, UNKNOWN_IMAGE)
        if not os.path.isfile(img_path):
            label = tk.Label(
                secret_frame,
                text="Image not found.",
                font=RETRO_FONT,
                bg=BG_COLOR
            )
            label.pack(expand=True)
            return

        try:
            img = Image.open(img_path)
            img.thumbnail((800, 500))
            img_ref = ImageTk.PhotoImage(img)

            label = tk.Label(
                secret_frame,
                image=img_ref,
                bg=BG_COLOR,
                relief="ridge",
                borderwidth=3
            )
            label.pack(expand=True, pady=20)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    notebook.bind("<<NotebookTabChanged>>", on_tab_change)

    root.mainloop()


if __name__ == "__main__":
    main()
