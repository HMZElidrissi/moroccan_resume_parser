from resume_parser.resume_parser import ResumeParser
from pathlib import Path
import json

def main():
    resume_directory = Path('resumes')
    output_file = Path('parsed_resumes.json')

    results = []
    for resume_path in resume_directory.glob('*'):
        if resume_path.is_file():
            try:
                parser = ResumeParser(str(resume_path))
                parsed_data = parser.parse()
                results.append({
                    'file_name': resume_path.name,
                    'parsed_data': parsed_data.__dict__
                })
                print(f"Successfully parsed {resume_path.name}")
            except Exception as e:
                print(f"Error parsing {resume_path.name}: {str(e)}")

    # Save results to a JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    print(f"Parsing complete. Results saved to {output_file}")

if __name__ == '__main__':
    main()