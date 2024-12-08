# pdf-merger

A simple command line utility that allows for prepending, combining, and postfixing PDF files.

## Features

- Prepend pages from a PDF to all PDFs in a directory.
- Append pages from a PDF to all PDFs in a directory.
- Combine multiple PDFs with optional prefix and postfix pages.

## Requirements

- Python 3.x
- `pypdf` for PDF manipulation
- `pyinstaller` for building executables
- `pytest` and `pytest-mock` for testing

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/pdf-merger.git
   cd pdf-merger   ```

2. **Install Dependencies**

   Use `pip` to install the required packages:
   ```bash
   pip install -r requirements.txt   ```

## Usage

The `pdf-merger` script can be run from the command line. Below are the available options:

Linux / Mac OS

```bash
python src/merger.py <input_dir> [-p <prefix_file>] [-s <postfix_file>] [-o <output_dir>] [-t <threads>]
```

Windows

```cmd
python src\merger.py C:\path\to\input --prefix C:\path\to\prefix.pdf --postfix C:\path\to\postfix.pdf --output_dir C:\path\to\output
```

### Options

- `<input_dir>`: Path to the directory containing input PDF files.
- `-p, --prefix <prefix_file>`: Path to the PDF file containing prefix pages (optional).
- `-s, --postfix <postfix_file>`: Path to the PDF file containing postfix pages (optional).
- `-o, --output_dir <output_dir>`: Name of the output directory (default: 'output').
- `-t, --threads <threads>`: Number of threads to use (default: 4).

### Example

To prepend and append pages to all PDFs in a directory:

Linux / MacOS:

```bash
python src/merger.py /path/to/input --prefix /path/to/prefix.pdf --postfix /path/to/postfix.pdf --output_dir /path/to/output
```

Windows:

```cmd
python src\merger.py C:\path\to\input --prefix C:\path\to\prefix.pdf --postfix C:\path\to\postfix.pdf --output_dir C:\path\to\output
```

## Building Executables

To build standalone executables for different operating systems, use `pyinstaller`:

```bash
pyinstaller --onefile --name pdf_tool src/merger.py
```

This will create an executable in the `dist` directory.

## Testing

To run tests, use `pytest`:

```bash
pytest tests/
```


## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.