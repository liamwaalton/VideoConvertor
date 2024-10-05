import tkinter as tk
from tkinter import filedialog, messagebox
import ffmpeg
import threading
import os

class MKVtoMP4Converter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MKV to MP4 Converter")
        self.geometry("400x200")
        self.input_file = None
        self.output_file = None

        self.create_widgets()

    def create_widgets(self):
        # Input File Selection
        self.select_button = tk.Button(self, text="Select MKV File", command=self.select_file)
        self.select_button.pack(pady=10)

        self.file_label = tk.Label(self, text="No file selected")
        self.file_label.pack(pady=5)

        # Convert Button
        self.convert_button = tk.Button(self, text="Convert to MP4", command=self.start_conversion, state=tk.DISABLED)
        self.convert_button.pack(pady=10)

        # Status Label
        self.status_label = tk.Label(self, text="")
        self.status_label.pack(pady=5)

    def select_file(self):
        filetypes = (("MKV files", "*.mkv"), ("All files", "*.*"))
        filepath = filedialog.askopenfilename(title="Open MKV file", initialdir=os.getcwd(), filetypes=filetypes)

        if filepath:
            self.input_file = filepath
            self.output_file = os.path.splitext(self.input_file)[0] + '.mp4'
            self.file_label.config(text=f"Selected: {os.path.basename(self.input_file)}")
            self.convert_button.config(state=tk.NORMAL)

    def start_conversion(self):
        self.convert_button.config(state=tk.DISABLED)
        self.status_label.config(text="Conversion started...")
        threading.Thread(target=self.convert_mkv_to_mp4).start()

    def convert_mkv_to_mp4(self):
        try:
            (
                ffmpeg
                .input(self.input_file)
                .output(self.output_file, c='copy')
                .run(overwrite_output=True)
            )
            self.status_label.config(text="Conversion successful!")
            messagebox.showinfo("Success", f"File converted successfully:\n{self.output_file}")
        except ffmpeg.Error as e:
            error_message = e.stderr.decode()
            self.status_label.config(text="Conversion failed.")
            messagebox.showerror("Error", f"An error occurred:\n{error_message}")
        finally:
            self.convert_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    app = MKVtoMP4Converter()
    app.mainloop()