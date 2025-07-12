import json
import logging
import os
import re
from typing import List
import google.generativeai as genai
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

# ✅ Configure Gemini API key
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# ✅ Initialize Gemini 1.5 Flash model
model = genai.GenerativeModel("gemini-1.5-flash")

# ✅ Define Pydantic Schema for structured validation
class PlagiarismAnalysis(BaseModel):
    plagiarism_score: float
    risk_level: str
    detected_issues: List[str]
    improvement_suggestions: List[str]
    original_sections: List[str]
    suspicious_sections: List[str]

def analyze_plagiarism(content: str, content_type: str = "text") -> PlagiarismAnalysis:
    try:
        # 📌 Use a strict prompt
        prompt = f"""
Analyze the following {content_type} for potential plagiarism and improvement suggestions:

{content}

Respond ONLY in JSON format like this:

{{
  "plagiarism_score": 25.4,
  "risk_level": "Low",
  "detected_issues": ["Example issue 1", "Example issue 2"],
  "improvement_suggestions": ["Example suggestion"],
  "original_sections": ["Original part here..."],
  "suspicious_sections": ["Suspicious part here..."]
}}
"""

        # ✅ Generate response using Gemini 1.5 Flash
        response = model.generate_content(prompt)

        if not response.text:
            raise ValueError("Empty response from Gemini API")

        # ✅ Extract JSON using regex in case Gemini wraps response in text
        json_match = re.search(r"\{.*\}", response.text, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON detected in Gemini response")

        result_data = json.loads(json_match.group())
        logging.info(f"Gemini returned: {result_data}")

        return PlagiarismAnalysis(**result_data)

    except json.JSONDecodeError as e:
        logging.error(f"JSON decoding failed: {e}")
        return PlagiarismAnalysis(
            plagiarism_score=0.0,
            risk_level="Unknown",
            detected_issues=["Unable to parse analysis results"],
            improvement_suggestions=["Please try again with different content"],
            original_sections=[],
            suspicious_sections=[]
        )
    except Exception as e:
        logging.error(f"Gemini API error: {e}")
        return PlagiarismAnalysis(
            plagiarism_score=0.0,
            risk_level="Error",
            detected_issues=[f"Analysis failed: {str(e)}"],
            improvement_suggestions=["Please check your API key and model name"],
            original_sections=[],
            suspicious_sections=[]
        )
