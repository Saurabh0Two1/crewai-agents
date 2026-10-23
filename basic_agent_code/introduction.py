
    
def basic_crew():
    print("Hello from crewai-agents!")
    import os
    from dotenv import load_dotenv
    from crewai import Agent, LLM, Task, Crew

    load_dotenv()
    llm = LLM(
        model="ollama/llama3.2:1b",
        base_url="http://localhost:11434"
    )

    ## AGENTS
    senior_technical_writer = Agent(
        role="Senior Technical Writer",
        goal="""Craft clear, engaging, and well-structured
                technical content based on research findings""",    
        backstory="""You are an experienced technical writer
                    with expertise in simplifying complex
                    concepts, structuring content for readability,
                    and ensuring accuracy in documentation.""",
        llm=llm,      
        verbose=True
    )

    ## TASKS
    writing_task = Task(
        description="""Write a well-structured, engaging,
                    and technically accurate article
                    on {topic}.""",
        agent=senior_technical_writer, 
        expected_output="""A polished, detailed, and easy-to-read
                        article on the given topic.""",
    )


    ## CREW
    crew = Crew(
        agents=[senior_technical_writer],
        tasks=[writing_task],
        verbose=True
    )

    response = crew.kickoff(inputs={"topic":"AI Agents"})

    f = open("output.md", "w")
    f.write(response.raw)
    f.close()