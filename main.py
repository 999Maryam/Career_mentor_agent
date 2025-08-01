import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from roadmap_tool import get_career_roadmap

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)
career_agent = Agent(
    name="Career Mentor Agent",
    instructions="You ask about interest and suggest a career field.",
    model=model
)

skill_agent = Agent(
    name="SkillAgent",
    instructions="You share the roadmap using the get_career_roadmap tool.",
    model=model,
    tools=[get_career_roadmap]
)

job_agent = Agent(
    name="JobAgent",
    instructions="You suggest job titles in the chosen career.",
    model=model
)

def main():
    print("\U0001F393 Career Mentor Agent\n")

    while True:
        interest = input("📝 What are your interests? ➡ ")

        result1 = Runner.run_sync(career_agent, interest, run_config=config)
        field = result1.final_output.strip()
        print("\n📌 Suggested Career:", field)

        result2 = Runner.run_sync(skill_agent, field, run_config=config)
        print("\n📚 Required Skills:", result2.final_output)

        result3 = Runner.run_sync(job_agent, field, run_config=config)
        print("\n💼 Possible Jobs:", result3.final_output)

        again = input("\n🔁 Do you want to explore another field? (yes/no): ").strip().lower()
        if again not in ('yes', 'y'):
            print("\n🙌 Thanks for using Career Mentor Agent!")
            break

if __name__ == "__main__":
    main()