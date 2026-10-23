
import asyncio
from pprint import pprint

from crewai import flow

from flows.unstructured_state import TaskManagementFlow

async def main():
    print("Hello from crewai-agents!")
    # from basic_agent_code.introduction import basic_crew
    # from basic_agent_code.with_tools import multi_agent_with_serper_tool, with_file_read_tool
    # from basic_agent_code.with_yaml import multiagent_with_yaml
    # from basic_agent_code.structured_output import structured_output
    # from modular_crews.research_crew import ResearchCrew
    # from modular_crews.custom_tools import custom_tool
    from dotenv import load_dotenv
    load_dotenv()



    # Execute the flow
    flow = TaskManagementFlow()
    await flow.kickoff_async()

    
if __name__ == "__main__":
    asyncio.run(main())
