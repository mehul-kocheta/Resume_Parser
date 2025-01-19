# Resume Information Extraction Script

This project is a Python script designed to process PDF resumes from a folder, extract specific information using the Ollama API, and save the extracted data into a CSV file. The script uses the `llama3.2` model to extract details like name, email, university, skills, and various experience scores from the resumes. For better performance, consider using larger models if available.

## Features

- Read and process multiple PDF resumes from a folder.
- Extract structured information using the Ollama API.
- Save the extracted data into a CSV file for easy analysis.

---

## Prerequisites

### Install Ollama

Before running the script, you need to install Ollama on you[r PC. Follow t](https://ollama.com/)he instructions on the [Ollama website](https://ollama.com/) to download and set it up.

### Python Dependencies

Install the required Python libraries:

```bash
pip install pymupdf pandas ollama
```

### Folder Setup

Ensure you have a folder containing the PDF resumes you want to process.

### Ollama Setup

Make sure the `ollama` library is properly installed and configured. You'll need access to the `llama3.2` model for processing the resumes.

Note : Bigger models will give better performace.

### Clone the Repository

Clone this repository to your local machine:

```bash
git clone <repository_url>
cd <repository_folder>
```

### Run the Script

The script accepts the following command-line arguments:

- `--folder_path` (required): Path to the folder containing PDF resumes.
- `--batch_size` (optional): Number of resumes to process in parallel batches (default is 3).

Example command to run the script:

```bash
python script.py --folder_path "path/to/resume/folder" --batch_size 5
```

### Output

The script generates a CSV file named `test1.csv` containing the extracted information.

---

## Error Handling

The script handles errors during PDF processing gracefully. If a resume cannot be processed, the error is logged, and the script continues processing the remaining resumes.

---

## Notes

- The `ollama` API should be configured properly on your system.
- Ensure that all PDF files in the folder are readable.
- The script assumes that the resumes are in English and follow a general structure.
- 10 Sample resumes are given in /resume folder and their outputs are saved in test_output.xlsx

---

## Contributions

Feel free to fork the repository and submit pull requests for any improvements or bug fixes.

---
