import json
import os

import logging
import re
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI




# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


openai_client = OpenAI(api_key=OPENAI_API_KEY)

def analyze_website_content(content: str, url: str) -> dict:

    # Analyze website content using ChatGPT according to a predefined rubric
    
    
    # Define the analysis rubric
    rubric_prompt = """
    You are a web Product Page (PDP) grader, grading PDP's based on GEO.
    Grade the given webpage content based on this comprehensive 
    rubric and give a score from 0 to 25 for each of the criteria.
    No need to score in increments of 5. Try to ignore info that
    is not relevant to the PDP and try to interpret possibly
    corrupted info as best as you can:

    Title Quality
    5	Title is incomplete, vague, or missing brand/keywords
    10	Title includes either brand or model, but not both
    15	Title includes brand + model, but lacks feature/benefit
    20	Title includes brand + model + one relevant feature or keyword
    25	Title includes brand + model + feature/benefit + keyword (readable & optimized)

    Description Depth
    5	Description is absent or only one sentence
    10	Description is minimal; lists specs but lacks structure
    15	Description lists key specs; weak or no benefits explained
    20	Includes specs + some benefits; generally well-structured
    25	Clear, structured description with specs, benefits, and persuasive language

    Bullet Point Effectiveness
    5	No bullet points or irrelevant/repetitive content
    10	1–2 bullet points; not well-formatted or persuasive
    15	3+ bullet points with basic info (but lacks selling points)
    20	3+ bullet points with some unique features/benefits
    25	5+ clear, concise bullets with strong selling points & varied content

    Image & Alt-Text Quality
    5	One image only; low resolution or unclear
    10	2+ images, but no alternate views or poor quality
    15	Multiple clear images; lacks lifestyle/demo context
    20	Includes multiple angles and at least one lifestyle/demo image
    25	High-res images from multiple views + lifestyle/demo + accurate alt-text

    User-Generated Content (UGC) Presence
    5	No reviews, Q&A, or ratings
    10	<3 reviews; mostly vague or low-detail
    15	3+ reviews; some detail, basic Q&A present
    20	5+ reviews, some with photos/verified badge, active Q&A
    25	10+ detailed reviews (some visual), active Q&A, high rating visibility

    Add the scores for a total score as well.
    Provide your analysis in JSON format with the following structure:
    {
        "overall_score": number (0-100),
        "grade": "letter grade (A+ to F)",
        "categories": {
            "title_quality": {"score": number, "feedback": "detailed feedback"},
            "description_depth": {"score": number, "feedback": "detailed feedback"},
            "bullet_point_effectiveness": {"score": number, "feedback": "detailed feedback"},
            "image_alt_text_quality": {"score": number, "feedback": "detailed feedback"},
            "user_generated_content": {"score": number, "feedback": "detailed feedback"},
        },
        "strengths": ["list of 3-5 key strengths"],
        "areas_for_improvement": ["list of 3-5 areas needing improvement"],
        "summary": "2-3 sentence overall summary",
        "recommendations": ["list of 3-5 specific actionable recommendations"]
    }
    """


    
    '''
        "content_quality": {"score": number, "feedback": "detailed feedback"},
        "structure_organization": {"score": number, "feedback": "detailed feedback"},
        "user_experience": {"score": number, "feedback": "detailed feedback"},
        "purpose_audience": {"score": number, "feedback": "detailed feedback"},
        "technical_aspects": {"score": number, "feedback": "detailed feedback"},
        "credibility_trust": {"score": number, "feedback": "detailed feedback"}
    '''
    
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": rubric_prompt
                },
                {
                    "role": "user",
                    "content": f"Please analyze this website content from {url}"  # Limit content to avoid token limits
                }
            ],
            response_format={"type": "json_object"},
            max_tokens=2000
        )
        #"Please analyze this website content from {url}:\n\n{content[:8000]}
        result = json.loads(response.choices[0].message.content)
        # Save the JSON to a local file
        filename = re.sub(r'[\\/*?:"<>|&=%]', "_", url) + ".json"
        filename = filename[:50]
        filepath = os.path.join("analysis_results", filename)  # Save in a directory named "analysis_results"

        # Ensure the directory exists
        if not os.path.exists("analysis_results"):
            os.makedirs("analysis_results")

        with open(filepath, "w") as f:
            json.dump(result, f, indent=4)
        logging.info(f"Successfully analyzed content for {url}")
        return result
        
    except json.JSONDecodeError as e:
        logging.error(f"JSON parsing error: {e}")
        raise Exception("Failed to parse analysis results")
    except Exception as e:
        logging.error(f"OpenAI API error: {e}")
        raise Exception(f"Failed to analyze content with ChatGPT: {str(e)}")
    
'''
models = openai.models.list()

for model in models.data:
    print(model.id)
'''