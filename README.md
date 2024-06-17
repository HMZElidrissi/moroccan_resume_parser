# Moroccan Resume Parser

Moroccan Resume Parser is a customized tool for parsing resumes specifically tailored to the Moroccan job market. It is built upon the [pyresparser](https://github.com/OmkarPathak/pyresparser) library with specific adjustments to handle Moroccan education, job titles, and other relevant details.

## Features

- Extracts basic details such as name, email, and mobile number.
- Identifies skills, education, and professional experience from resumes.
- Customized to recognize Moroccan-specific education titles and job roles.
- Uses `spacy` for natural language processing and matching.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/HMZElidrissi/moroccan_resume_parser.git
    ```

2. Navigate to the project directory:
    ```bash
    cd moroccan_resume_parser
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Place resumes to be parsed in a directory named `resumes` within the project directory.

2. Run the parser:
    ```bash
    python resume_parser.py
    ```

3. The parsed data will be printed to the console.

## Customization

### Adding New Education Titles

To add new education titles specific to Morocco, modify the `EDUCATION` list in the `constants.py` file:
```python
EDUCATION = [
    'Bac', 'Baccalauréat', 'Licence', 'Master', 'Doctorat', 'Master', 'LST',
    'niveau bac', 'Diplôme d\'ingénieur', 'Bachelor', 'PhD', 'Doctorat',
    'Ingénieur', 'Cycle', 'Ingénierie', 'DEUG', 'DUT', 'BTS', 'BAC', 'Licencié',
    'BAC+2', 'Ingénieur d\'état', 'BAC+3', 'BAC+4', 'BAC+5', 'DEUST', 'M1', 'M2'
]
```

### Adding New Job Titles

To add new job titles specific to Morocco, modify the `JOB_TITLE` list in the `constants.py` file:
```python
JOB_TITLE = ["Développeur", "stage", "PFE", "PFA", "Consultant", "Ingénieur", "stagiaire", "internship", "intern"]
```

## Built On

This project is built on top of the [Pyresparser](https://github.com/OmkarPathak/pyresparser) library, which provides the core functionality for resume parsing. The adjustments made cater specifically to the nuances of the Moroccan job market.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.