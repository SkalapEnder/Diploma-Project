import tkinter as tk
from tkinter import ttk, filedialog

class ImageResizerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Resizer")
        self.root.geometry("1200x700")

        self.create_layout()

    def create_layout(self):
        # === MAIN GRID CONFIGURATION ===
        self.root.columnconfigure(0, weight=2)
        self.root.columnconfigure(1, weight=6)
        self.root.columnconfigure(2, weight=1)

        self.root.rowconfigure(0, weight=1)

        # === LEFT PANEL: INPUT PARAMETERS ===
        left_panel = ttk.Frame(self.root, padding=10, relief="groove")
        left_panel.grid(row=0, column=0, sticky="nsew")

        ttk.Label(left_panel, text="Input Parameters", font=("Arial", 10, "bold")).pack(pady=5)

        # Interpolation method
        ttk.Label(left_panel, text="Interpolation Method").pack(anchor="w", pady=(10, 2))
        self.method = tk.StringVar(value="Nearest")
        ttk.OptionMenu(
            left_panel,
            self.method,
            "Nearest",
            "Nearest",
            "Bilinear",
            "Bicubic",
            "Lanczos"
        ).pack(fill="x")

        # Scale multiplier
        ttk.Label(left_panel, text="Scale Multiplier").pack(anchor="w", pady=(15, 2))
        self.scale_entry = ttk.Entry(left_panel)
        self.scale_entry.insert(0, "1.5")
        self.scale_entry.pack(fill="x")

        ttk.Label(left_panel, text="OR", foreground="gray").pack(pady=10)

        # Width / Height
        wh_frame = ttk.Frame(left_panel)
        wh_frame.pack(fill="x")

        ttk.Label(wh_frame, text="Width").grid(row=0, column=0, padx=5, sticky="w")
        self.width_entry = ttk.Entry(wh_frame, width=10)
        self.width_entry.insert(0, "1000")
        self.width_entry.grid(row=1, column=0, padx=5)

        ttk.Label(wh_frame, text="Height").grid(row=0, column=1, padx=5, sticky="w")
        self.height_entry = ttk.Entry(wh_frame, width=10)
        self.height_entry.insert(0, "1000")
        self.height_entry.grid(row=1, column=1, padx=5)

        # === CENTER PANEL ===
        center_panel = ttk.Frame(self.root, padding=10)
        center_panel.grid(row=0, column=1, sticky="nsew")

        center_panel.rowconfigure(0, weight=1)
        center_panel.rowconfigure(1, weight=1)
        center_panel.columnconfigure(0, weight=1)

        # Input Image
        input_image_frame = ttk.LabelFrame(center_panel, text="Input Image")
        input_image_frame.grid(row=0, column=0, sticky="nsew", pady=5)

        self.input_canvas = tk.Canvas(input_image_frame, bg="white")
        self.input_canvas.pack(expand=True, fill="both", padx=5, pady=5)

        ttk.Button(
            input_image_frame,
            text="Load Image",
            command=self.load_image
        ).place(relx=0.5, rely=0.5, anchor="center")

        # Output Image
        output_image_frame = ttk.LabelFrame(center_panel, text="Output Image")
        output_image_frame.grid(row=1, column=0, sticky="nsew", pady=5)

        self.output_canvas = tk.Canvas(output_image_frame, bg="white")
        self.output_canvas.pack(expand=True, fill="both", padx=5, pady=5)

        # === RIGHT PANEL: INFORMATION ===
        right_panel = ttk.Frame(self.root, padding=10, relief="groove")
        right_panel.grid(row=0, column=2, sticky="nsew")

        ttk.Label(right_panel, text="Input Image Info", font=("Arial", 9, "bold")).pack(pady=(15, 5))
        self.input_info = tk.Label(right_panel, text="—", anchor="w", justify="left")
        self.input_info.pack(fill="x")

        ttk.Label(right_panel, text="Output Image Info", font=("Arial", 9, "bold")).pack(pady=(15, 5))
        self.output_info = tk.Label(right_panel, text="—", anchor="w", justify="left")
        self.output_info.pack(fill="x")

        ttk.Label(
            right_panel,
            text="Statistics / Performance metrics",
            font=("Arial", 9, "bold")
        ).pack(pady=(20, 5))

        self.stats_text = tk.Text(right_panel, height=6, state="disabled")
        self.stats_text.pack(fill="both", expand=True)

    def load_image(self):
        filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageResizerUI(root)
    root.mainloop()
