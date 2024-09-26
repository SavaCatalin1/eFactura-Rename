import fitz  # PyMuPDF
import re
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Extract text from the first page of a PDF
def extract_text_from_first_page(pdf_path):
    document = fitz.open(pdf_path)
    page = document.load_page(0)  # Load the first page
    text = page.get_text()
    return text

### Existing Logic for Invoice with Date and Supplier ###
def find_date_and_supplier(text):
    date_pattern = re.compile(r'Nr\. doc\.\s*[\w\s\.\-/]*\s*din\s*(\d{2}/\d{2}/\d{4})')
    date_match = date_pattern.search(text)
    date = date_match.group(1) if date_match else 'unknown_date'
    date = date.replace('/', '-')

    supplier_pattern = re.compile(r'FURNIZOR\s*\n\s*(.+)')
    supplier_match = supplier_pattern.search(text)
    supplier = supplier_match.group(1).strip() if supplier_match else 'unknown_supplier'

    return date, supplier

### New Logic for Serie, Numar, Data, and Client Extraction (ATI Invoice) ###
def find_invoice_details(text):
    # Regex to find the "Serie", "Numar", "Data", and "Client"
    serie_pattern = re.compile(r'Serie\s+(\w+)\s+Numar\s+(\d+)')
    serie_match = serie_pattern.search(text)
    serie = serie_match.group(1) if serie_match else 'unknown_serie'
    numar = serie_match.group(2) if serie_match else 'unknown_numar'

    date_pattern = re.compile(r'Data\s+(\d{2}\.\d{2}\.\d{4})')
    date_match = date_pattern.search(text)
    date = date_match.group(1).replace('.', '-') if date_match else 'unknown_date'

    client_pattern = re.compile(r'Client\s*.*?\n(.+)\n')
    client_match = client_pattern.search(text)
    client = client_match.group(1).strip() if client_match else 'unknown_client'

    return serie, numar, date, client

### Common Function to Rename PDF Files ###
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

### Process Function for the ATI Invoice (with Serie, Numar, Data, and Client) ###
def process_ati_invoice(pdf_path):
    text = extract_text_from_first_page(pdf_path)
    serie, numar, date, client = find_invoice_details(text)
    new_name = f"{serie}_{numar} {date} {client}"
    new_path = rename_pdf_file(pdf_path, new_name)
    print(f"Renamed to: {new_path}")

### Process Function for Date and Supplier Invoice ###
def process_invoice(pdf_path):
    text = extract_text_from_first_page(pdf_path)
    date, supplier = find_date_and_supplier(text)
    new_name = f"{date}_{supplier}"
    new_path = rename_pdf_file(pdf_path, new_name)
    print(f"Renamed to: {new_path}")

### Folder and File Processing Logic ###
def process_all_pdfs_in_folder(folder_path, doc_type):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            if doc_type == "supplier_invoice":
                process_invoice(pdf_path)
            elif doc_type == "ati_invoice":
                process_ati_invoice(pdf_path)

def process_selected_pdfs(file_paths, doc_type):
    for pdf_path in file_paths:
        if doc_type == "supplier_invoice":
            process_invoice(pdf_path)
        elif doc_type == "ati_invoice":
            process_ati_invoice(pdf_path)

### GUI Selection Functions ###
def select_folder_and_process_pdfs(doc_type):
    folder_path = filedialog.askdirectory()
    if folder_path:
        process_all_pdfs_in_folder(folder_path, doc_type)

def select_files_and_process_pdfs(doc_type):
    file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    if file_paths:
        process_selected_pdfs(file_paths, doc_type)

### GUI Creation Function ###
def create_gui():
    root = tk.Tk()
    root.title("ATI / eFactura Rename")
    root.geometry("700x200")  # Enlarged window size

    label = tk.Label(root, text="Selecteaza o optiune de redenumire PDF:")
    label.pack(pady=20)

    # Create a frame to hold the buttons in a grid layout
    frame = tk.Frame(root)
    frame.pack(padx=20, pady=20)

    # Supplier Invoice Buttons on the left side
    button_select_folder_supplier = tk.Button(frame, text="Selecteaza Folder (Furnizori eFactura)", 
                                              command=lambda: select_folder_and_process_pdfs("supplier_invoice"),
                                              width=30)
    button_select_folder_supplier.grid(row=0, column=0, padx=50, pady=10)

    button_select_files_supplier = tk.Button(frame, text="Selecteaza Fisiere (Furnizori eFactura)", 
                                             command=lambda: select_files_and_process_pdfs("supplier_invoice"),
                                             width=30)
    button_select_files_supplier.grid(row=1, column=0, padx=50, pady=10)

    # ATI Invoice Buttons on the right side
    button_select_folder_ati = tk.Button(frame, text="Selecteaza Folder (Emise ATI)", 
                                         command=lambda: select_folder_and_process_pdfs("ati_invoice"),
                                         width=30)
    button_select_folder_ati.grid(row=0, column=2, padx=50, pady=10)

    button_select_files_ati = tk.Button(frame, text="Selecteaza Fisiere (Emise ATI)", 
                                        command=lambda: select_files_and_process_pdfs("ati_invoice"),
                                        width=30)
    button_select_files_ati.grid(row=1, column=2, padx=50, pady=10)
    root.mainloop()

# Run the GUI
create_gui()
