
import asyncio
from pprint import pprint

async def main():
    print("Hello from crewai-agents!")
    # from basic_agent_code.introduction import basic_crew
    # from basic_agent_code.with_tools import multi_agent_with_serper_tool, with_file_read_tool
    # from basic_agent_code.with_yaml import multiagent_with_yaml
    # from basic_agent_code.structured_output import structured_output
    # from modular_crews.research_crew import ResearchCrew
    # from modular_crews.custom_tools import custom_tool
    from flows.agentic_flow import MovieRecommendationFlow
    from dotenv import load_dotenv
    load_dotenv()


    flow = MovieRecommendationFlow()
    final_result =await flow.kickoff_async()
    pprint(flow.state)

    print(f"\nMovie Recommendation: {final_result}")
    
if __name__ == "__main__":
    asyncio.run(main())
