import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field
import spacy
from spacy.matcher import Matcher
from spacy.tokens import Doc
from spacy.training import Example
import random
import logging
from concurrent.futures import ProcessPoolExecutor
import pandas as pd
import re
from collections import Counter

from .constants import EDUCATION, JOB_TITLE, EXPERIENCE
from .utils import extract_text, extract_email, extract_mobile_number

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ResumeData:
    name: Optional[str] = None
    email: Optional[str] = None
    mobile_number: Optional[str] = None
    skills: List[str] = field(default_factory=list)
    education: List[str] = field(default_factory=list)
    experience: List[Dict[str, str]] = field(default_factory=list)
    competencies: Dict[str, List[str]] = field(default_factory=dict)
    measurable_results: Dict[str, List[str]] = field(default_factory=dict)

class ResumeParser:
    def __init__(self, resume_path: str):
        self.resume_path = Path(resume_path)
        self.nlp = spacy.load("fr_core_news_lg")
        self.matcher = Matcher(self.nlp.vocab)
        self.resume_data = ResumeData()
        self._train_custom_ner()

    def _train_custom_ner(self):
        ner = self.nlp.get_pipe("ner")

        TRAIN_DATA = [
            ("J'ai travaillé chez Maroc Telecom pendant 3 ans", {"entities": [(17, 30, "ORG")]}),
            ("J'ai obtenu une Licence en Informatique à l'Université Mohammed V", {"entities": [(17, 24, "DEGREE"), (41, 62, "ORG")]}),
            ("Mon numéro est +212 6 12 34 56 78", {"entities": [(14, 31, "PHONE_NUMBER")]}),
            ("J'ai effectué un stage chez OCP Group", {"entities": [(28, 37, "ORG")]}),
            ("Diplômé de l'ENSA de Marrakech", {"entities": [(13, 17, "ORG"), (21, 30, "GPE")]}),
            ("J'ai travaillé sur des projets pour Royal Air Maroc", {"entities": [(37, 53, "ORG")]}),
        ]

        for _, annotations in TRAIN_DATA:
            for ent in annotations.get("entities"):
                ner.add_label(ent[2])

        other_pipes = [pipe for pipe in self.nlp.pipe_names if pipe != "ner"]
        with self.nlp.disable_pipes(*other_pipes):
            optimizer = self.nlp.create_optimizer()
            for _ in range(30):
                random.shuffle(TRAIN_DATA)
                losses = {}
                for text, annotations in TRAIN_DATA:
                    doc = self.nlp.make_doc(text)
                    example = Example.from_dict(doc, annotations)
                    self.nlp.update([example], drop=0.5, losses=losses)
                print(losses)

    def parse(self) -> ResumeData:
        try:
            text_raw = extract_text(self.resume_path)
            doc = self.nlp(text_raw)

            self._extract_basic_details(doc)
            self._extract_advanced_details(doc)

            return self.resume_data
        except Exception as e:
            logger.error(f"Error parsing resume {self.resume_path}: {str(e)}")
            raise

    def _extract_basic_details(self, doc: Doc):
        self.resume_data.name = self._extract_name(doc)
        self.resume_data.email = extract_email(doc.text)
        self.resume_data.mobile_number = extract_mobile_number(doc.text)
        self.resume_data.skills = self._extract_skills(doc)
        self.resume_data.education = self._extract_education(doc)

    def _extract_advanced_details(self, doc: Doc):
        self.resume_data.experience = self._extract_experience(doc)
        self.resume_data.competencies = self._extract_competencies(doc)
        self.resume_data.measurable_results = self._extract_measurable_results(doc)

    def _extract_name(self, doc: Doc) -> Optional[str]:
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
        return None

    def _extract_skills(self, doc: Doc) -> List[str]:
        skill_patterns = [
            [{"LOWER": {"IN": ["python", "java", "c++", "javascript", "php"]}}],
            [{"LOWER": "machine"}, {"LOWER": "learning"}],
            [{"LOWER": "data"}, {"LOWER": "analysis"}],
            [{"LOWER": "gestion"}, {"LOWER": "de"}, {"LOWER": "projet"}],
            [{"LOWER": "marketing"}, {"LOWER": "digital"}],
        ]
        matcher = Matcher(self.nlp.vocab)
        matcher.add("SKILLS", skill_patterns)
        matches = matcher(doc)
        skills = [doc[start:end].text for _, start, end in matches]
        return list(set(skills))

    def _extract_education(self, doc: Doc) -> List[str]:
        education = []
        for ent in doc.ents:
            if ent.label_ in ["DEGREE", "ORG"]:
                education.append(ent.text)
        for sent in doc.sents:
            if any(keyword in sent.text.lower() for keyword in EDUCATION):
                education.append(sent.text)
        return list(set(education))

    def _extract_experience(self, doc: Doc) -> List[Dict[str, str]]:
        experience = []
        for sent in doc.sents:
            if any(keyword in sent.text.lower() for keyword in EXPERIENCE):
                exp = {
                    "description": sent.text,
                    "organization": next((ent.text for ent in sent.ents if ent.label_ == "ORG"), None),
                    "duration": self._extract_duration(sent.text)
                }
                experience.append(exp)
        return experience

    def _extract_duration(self, text: str) -> Optional[str]:
        duration_pattern = r"\d+\s*(an|année|ans|mois|semaine|semaines|jour|jours)"
        match = re.search(duration_pattern, text, re.IGNORECASE)
        return match.group(0) if match else None

    def _extract_competencies(self, doc: Doc) -> Dict[str, List[str]]:
        competencies = {
            "leadership": [],
            "communication": [],
            "teamwork": [],
            "languages": [],
        }

        competency_patterns = {
            "leadership": ["diriger", "gérer", "superviser", "leader"],
            "communication": ["communiquer", "présenter", "négocier"],
            "teamwork": ["collaborer", "travailler en équipe", "coopérer"],
            "languages": ["arabe", "français", "anglais", "espagnol", "amazigh"],
        }

        for sent in doc.sents:
            for category, patterns in competency_patterns.items():
                if any(pattern in sent.text.lower() for pattern in patterns):
                    competencies[category].append(sent.text)

        return competencies

    def _extract_measurable_results(self, doc: Doc) -> Dict[str, List[str]]:
        results = []
        for sent in doc.sents:
            if any(token.like_num for token in sent) and any(token.text in ["%", "pourcent", "dirhams", "dh", "MAD"] for token in sent):
                results.append(sent.text)
        return {"achievements": results}

    def parse_resume(resume_path: str) -> ResumeData:
        parser = ResumeParser(resume_path)
        return parser.parse()

