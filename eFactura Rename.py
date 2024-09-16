import fitz  # PyMuPDF
import re
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def extract_text_from_first_page(pdf_path):
    document = fitz.open(pdf_path)
    page = document.load_page(0)  # Load the first page
    text = page.get_text()
    return text

def find_date_and_supplier(text):
    # Enhanced regex to match various formats of the document number and date
    date_pattern = re.compile(r'Nr\. doc\.\s*[\w\s\.\-/]*\s*din\s*(\d{2}/\d{2}/\d{4})')
    date_match = date_pattern.search(text)
    date = date_match.group(1) if date_match else 'unknown_date'
    # Replace '/' with '-' for valid file names
    date = date.replace('/', '-')

    # Regex to find the supplier following the word FURNIZOR on the next line
    supplier_pattern = re.compile(r'FURNIZOR\s*\n\s*(.+)')
    supplier_match = supplier_pattern.search(text)
    supplier = supplier_match.group(1).strip() if supplier_match else 'unknown_supplier'

    return date, supplier

def rename_pdf_file(pdf_path, new_name):
    directory = os.path.dirname(pdf_path)
    new_path = os.path.join(directory, new_name + '.pdf')
    
    # Check if the file already exists and add a number if it does
    base_name = new_name
    counter = 1
    while os.path.exists(new_path):
        new_name = f"{base_name}_{counter}"
        new_path = os.path.join(directory, new_name + '.pdf')
        counter += 1

    os.rename(pdf_path, new_path)
    return new_path

def process_invoice(pdf_path):
    text = extract_text_from_first_page(pdf_path)
    date, supplier = find_date_and_supplier(text)
    new_name = f"{date}_{supplier}"
    new_path = rename_pdf_file(pdf_path, new_name)
    print(f"Renamed to: {new_path}")

def process_all_pdfs_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            process_invoice(pdf_path)

def process_selected_pdfs(file_paths):
    for pdf_path in file_paths:
        process_invoice(pdf_path)

def select_folder_and_process_pdfs():
    folder_path = filedialog.askdirectory()
    if folder_path:
        process_all_pdfs_in_folder(folder_path)

def select_files_and_process_pdfs():
    file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    if file_paths:
        process_selected_pdfs(file_paths)

def create_gui():
    root = tk.Tk()
    root.title("eFactura Renamer")

    label = tk.Label(root, text="Alegeti o optiune pentru a redenumi PDF-urile:")
    label.pack(pady=10)

    button_select_folder = tk.Button(root, text="Selectati Folder", command=select_folder_and_process_pdfs)
    button_select_folder.pack(pady=5)

    button_select_files = tk.Button(root, text="Selectati Fisiere", command=select_files_and_process_pdfs)
    button_select_files.pack(pady=5)

    root.mainloop()

# Run the GUI
create_gui()
