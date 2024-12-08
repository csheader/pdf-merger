import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from unittest.mock import MagicMock, patch
from src.merger import process_pdf, process_pdfs

@pytest.fixture
def mock_pdf_merger(mocker):
    mock_merger = mocker.patch('src.merger.PdfMerger', autospec=True)
    mock_instance = mock_merger.return_value
    mock_instance.append = MagicMock()
    mock_instance.write = MagicMock()
    mock_instance.close = MagicMock()
    return mock_instance

def test_process_pdf(mock_pdf_merger, tmp_path):
    pdf_file = "test.pdf"
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()
    (input_dir / pdf_file).touch()
    prefix_pages = MagicMock()
    postfix_pages = MagicMock()
    process_pdf(pdf_file, str(input_dir), prefix_pages, postfix_pages, str(output_dir))
    mock_pdf_merger.append.assert_any_call(prefix_pages)
    mock_pdf_merger.append.assert_any_call(str(input_dir / pdf_file))
    mock_pdf_merger.append.assert_any_call(postfix_pages)
    mock_pdf_merger.write.assert_called_once_with(str(output_dir / pdf_file))
    mock_pdf_merger.close.assert_called_once()

def test_process_pdfs(mocker, tmp_path):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()
    pdf_file = "test.pdf"
    (input_dir / pdf_file).touch()
    prefix_file = "prefix.pdf"
    postfix_file = "postfix.pdf"
    mocker.patch('src.merger.PdfReader', side_effect=lambda x: x)
    mock_process_pdf = mocker.patch('src.merger.process_pdf')
    process_pdfs(str(input_dir), prefix_file, postfix_file, str(output_dir), num_threads=2)
    mock_process_pdf.assert_called_once_with(
        pdf_file, str(input_dir), prefix_file, postfix_file, str(output_dir)
    )
