from agents import function_tool

@function_tool
def get_career_roadmap(field: str) -> str:
    maps = {
        "software engineering": "Learn Python, DSA, Web Dev, Github, build Projects.",
        "data science": "Master Python, Pandas, ML, and real-world datasets",
        "graphic designing": "Learn Adpbe Photoshop, Illustrator, Figma , UI/UX,",
        "agentic ai": "Study Python, Deep Learning, Transformers, Langchain, Dockers, LLMs, Openrouter, and AI tools"
    }
    return maps.get(field.lower(), "Nor Roadmap found for that field!")