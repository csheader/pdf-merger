import os
import argparse
from PyPDF2 import PdfMerger, PdfReader

def process_pdf(pdf_file, input_dir, prefix_pages, postfix_pages, output_dir):
    """
    Process a single PDF file by adding prefix and/or postfix pages.

    Args:
        pdf_file (str): The name of the PDF file to process.
        input_dir (str): The directory containing the input PDF file.
        prefix_pages (PdfReader or None): The PDF reader object for prefix pages, or None if not used.
        postfix_pages (PdfReader or None): The PDF reader object for postfix pages, or None if not used.
        output_dir (str): The directory where the processed PDF file will be saved.

    This function reads the specified PDF file, appends any prefix and/or postfix pages,
    and writes the result to the output directory. It handles exceptions and prints
    a message indicating the success or failure of the operation.
    """
    try:
        input_pdf_path = os.path.join(input_dir, pdf_file)
        output_pdf_path = os.path.join(output_dir, pdf_file)
        merger = PdfMerger()
        if prefix_pages:
            merger.append(prefix_pages)
        merger.append(input_pdf_path)
        if postfix_pages:
            merger.append(postfix_pages)
        merger.write(output_pdf_path)
        merger.close()
        print(f"Processed: '{pdf_file}' -> '{output_pdf_path}'")
    except Exception as e:
        print(f"An error occurred while processing '{pdf_file}': {e}")

def process_pdfs(input_dir, prefix_file, postfix_file, output_dir, num_threads):
    """
    Process all PDF files in the specified input directory by adding 
    prefix and/or postfix pages from the given PDF files.

    Args:
        input_dir (str): Path to the directory containing input PDF files.
        prefix_file (str): Path to the PDF file containing prefix pages (optional).
        postfix_file (str): Path to the PDF file containing postfix pages (optional).
        output_dir (str): Path to the directory where output PDF files will be saved.
        num_threads (int): Number of threads to use for processing PDF files.

    This function creates the output directory if it does not exist, 
    collects all PDF files from the input directory, and processes 
    each file concurrently using the specified number of threads.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    prefix_pages = prefix_file if prefix_file else None
    postfix_pages = postfix_file if postfix_file else None
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for pdf_file in pdf_files:
            executor.submit(process_pdf, pdf_file, input_dir, prefix_pages, postfix_pages, output_dir)

def main():
    parser = argparse.ArgumentParser(
        description="Add prefix and/or postfix pages to all PDF files in a directory."
    )
    parser.add_argument(
        "input_dir", 
        type=str, 
        help="Path to the directory containing input PDF files"
    )
    parser.add_argument(
        "-p", 
        "--prefix", 
        type=str, 
        help="Path to the PDF file containing prefix pages (optional)"
    )
    parser.add_argument(
        "-s", 
        "--postfix", 
        type=str, 
        help="Path to the PDF file containing postfix pages (optional)"
    )
    parser.add_argument(
        "-o", 
        "--output_dir", 
        type=str, 
        default="output", 
        help="Name of the output directory (default: 'output')"
    )
    parser.add_argument(
        "-t", 
        "--threads", 
        type=int, 
        default=4, 
        help="Number of threads to use (default: 4)"
    )
    args = parser.parse_args()
    input_dir = os.path.abspath(args.input_dir)
    prefix_file = os.path.abspath(args.prefix) if args.prefix else None
    postfix_file = os.path.abspath(args.postfix) if args.postfix else None
    output_dir = os.path.abspath(args.output_dir)
    # We only load the prefix and postfix pages once, since we know that
    # we will only really need to append or prepend the file with a single
    # file.
    prefix_pages = PdfReader(prefix_file) if prefix_file else None
    postfix_pages = PdfReader(postfix_file) if postfix_file else None
    process_pdfs(input_dir, prefix_pages, postfix_pages, output_dir, args.threads)

if __name__ == "__main__":
    main()
