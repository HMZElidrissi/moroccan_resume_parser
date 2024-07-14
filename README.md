# Moroccan Resume Parser

Moroccan Resume Parser is a customized tool for parsing resumes specifically tailored to the Moroccan job market. It is built upon the [pyresparser](https://github.com/OmkarPathak/pyresparser) library with specific adjustments to handle Moroccan education, job titles, and other relevant details.

## Features

- Extracts basic details such as name, email, and mobile number.
- Identifies skills, education, and professional experience from resumes.
- Customized to recognize Moroccan-specific education titles and job roles.
- Uses `spacy` for natural language processing and matching.

## Installation and Usage

1. Clone the repository:
    ```bash
    git clone https://github.com/HMZElidrissi/moroccan_resume_parser.git
    ```

2. Navigate to the project directory:
    ```bash
    cd moroccan_resume_parser
    ```
   
3. Set up the environment:
   First, ensure you have Python 3.7+ installed on your system. Then, create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
   
4. Download necessary NLTK data:
    ```bash
    python -m nltk.downloader stopwords
    python -m nltk.downloader punkt
    python -m nltk.downloader averaged_perceptron_tagger
    python -m nltk.downloader maxent_ne_chunker
    python -m nltk.downloader words
    ```

5. Download the French spaCy model:
    ```bash
    python -m spacy download fr_core_news_lg
    ```
   
6. Prepare your resume files:
   Place the resume files (PDF, DOCX, or TXT) you want to parse in a directory named 'resumes' in your project root.

7. Run the parser:
    ```bash
    python main.py
    ```
   The parsed data will be saved in a json file named `parsed_resumes.json` in the project root.


## Built On

This project is built on top of the [Pyresparser](https://github.com/OmkarPathak/pyresparser) library, which provides the core functionality for resume parsing. The adjustments made cater specifically to the nuances of the Moroccan job market.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.