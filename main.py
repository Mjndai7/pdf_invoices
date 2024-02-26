import os
import csv
import io
import traceback
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as pdf_file:
        for page in PDFPage.get_pages(pdf_file, caching=True, check_extractable=True):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()

    return text


def extract_key_value_pairs(text):
    header_keywords = ["Header", "Data"]
    table_keywords = ["Column 1", "Column 2", "Column 3", "Column 4"]

    header_data = []
    table_data = []

    lines = text.split('\n')
    for line in lines:
        if all(keyword in line for keyword in header_keywords):
            header_data.append(line.split(":")[1].strip())
        elif all(keyword in line for keyword in table_keywords):
            table_data.append(line.split(":")[1].strip())

    return header_data, table_data


def save_to_csv(header_data, table_data, csv_file):
    with open(csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write header data to CSV
        csv_writer.writerow(['Header Key', 'Header Value'])
        for i in range(0, len(header_data), 2):
            csv_writer.writerow([header_data[i], header_data[i+1]])

        # Write tabular data to CSV
        csv_writer.writerow([])  # Add an empty row for separation
        csv_writer.writerow(['Column 1', 'Column 2', 'Column 3', 'Column 4'])
        for i in range(0, len(table_data), 4):
            csv_writer.writerow(table_data[i:i+4])


def main(pdf_file_path, csv_file_path):
    try:
        text = extract_text_from_pdf(pdf_file_path)
        print("Extracted text length:", len(text))  # Print length of extracted text
        print("Extracted text:", text)  # Print extracted text for debugging
        header_data, table_data = extract_key_value_pairs(text)
        print("Header data:", header_data)  # Print extracted header data
        print("Table data:", table_data)  # Print extracted table data
        save_to_csv(header_data, table_data, csv_file_path)
        print("CSV file saved successfully.")
    except Exception as e:
        print("An error occurred:")
        print(traceback.format_exc())


if __name__ == "__main__":
    pdf_file_path = "invoice.pdf"  # Provide path to your PDF file
    csv_file_path = "invoice_data.csv"  # Provide desired path for CSV file
    main(pdf_file_path, csv_file_path)
