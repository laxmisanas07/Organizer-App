import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil

class FileOrganizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Organizer App - File Sorter")
        self.root.geometry("600x400")
        self.root.config(bg="#1e293b") # Dark Theme

        # --- UI Elements ---
        # Title
        title_label = tk.Label(root, text="AUTOMATED FILE ORGANIZER", 
                               font=("Arial", 20, "bold"), bg="#1e293b", fg="#22d3ee")
        title_label.pack(pady=30)

        # Selected Folder Label
        self.folder_path = tk.StringVar()
        self.path_label = tk.Label(root, text="No Folder Selected", 
                                   font=("Arial", 12), bg="#1e293b", fg="white")
        self.path_label.pack(pady=10)

        # Select Button
        btn_select = tk.Button(root, text="📂 Select Folder", command=self.select_folder,
                               font=("Arial", 14), bg="#facc15", fg="black", width=20)
        btn_select.pack(pady=10)

        # Organize Button
        btn_run = tk.Button(root, text="🚀 Clean & Organize", command=self.organize_files,
                            font=("Arial", 16, "bold"), bg="#22c55e", fg="white", width=20)
        btn_run.pack(pady=30)

        # Status
        self.status_label = tk.Label(root, text="Ready...", font=("Arial", 10), bg="#1e293b", fg="#94a3b8")
        self.status_label.pack(side=tk.BOTTOM, pady=20)

    # --- Functions ---
    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)
            self.path_label.config(text=f"Selected: {folder_selected}")
            self.status_label.config(text="Folder Loaded. Click 'Clean' to start.")

    def organize_files(self):
        path = self.folder_path.get()
        if not path:
            messagebox.showerror("Error", "Please select a folder first!")
            return

        # Extensions Mapping
        extensions = {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
            "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
            "Videos": [".mp4", ".mkv", ".mov", ".avi"],
            "Music": [".mp3", ".wav"],
            "Archives": [".zip", ".rar", ".tar"]
        }

        count = 0
        try:
            files = os.listdir(path)
            for file in files:
                filename, ext = os.path.splitext(file)
                ext = ext.lower()

                # Skip folders
                if not ext: 
                    continue

                for category, ext_list in extensions.items():
                    if ext in ext_list:
                        # Create Category Folder if not exists
                        category_path = os.path.join(path, category)
                        if not os.path.exists(category_path):
                            os.makedirs(category_path)
                        
                        # Move File
                        src = os.path.join(path, file)
                        dst = os.path.join(category_path, file)
                        shutil.move(src, dst)
                        count += 1
                        break
            
            self.status_label.config(text=f"Success! Moved {count} files.")
            messagebox.showinfo("Success", f"Done! Organized {count} files successfully.")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizer(root)
    root.mainloop()