

def with_file_read_tool():

    from crewai import Agent, Task, Crew, LLM
    from crewai_tools import FileReadTool

    llm = LLM(
        model="ollama/llama3.2:1b",
        base_url="http://localhost:11434"
    )

    file_read_tool = FileReadTool()

    summarizer_agent = Agent(
        role="Senior Document Summarizer",
        goal="Extract and summarize key insights from provided files in 20 words or less.",
        backstory="""You are an expert in document analysis, skilled at extracting 
                    key details, summarizing content, and identifying critical 
                    insights from structured and unstructured text.""",
        tools=[file_read_tool],
        llm=llm,
        verbose=True
    )

    summarizer_task = Task(
        description=(
            "Use the FileReadTool to read the contents of {file_path}"
            "and provide a summary in 20 words or less. "
            "Ensure the summary captures the key insights "
            "and main points from the document."
        ),
        agent=summarizer_agent,
        tools=[file_read_tool],
        expected_output="A concise 20-word summary of the key points from the file.",
    )

    summarizer_crew = Crew(
        agents=[summarizer_agent],
        tasks=[summarizer_task],
        verbose=True
    )

    # Run the crew with the file input
    response = summarizer_crew.kickoff(inputs={"file_path": "output.md"})

    f = open("summary_with_file.md", "w")
    f.write(response.raw)
    f.close()

def multi_agent_with_serper_tool():
    from crewai import Agent, Task, Crew, Process
    from crewai_tools import SerperDevTool
    # MULTI-AGENT WITH TOOLS
    serper_dev_tool = SerperDevTool()

    research_agent = Agent(
        role="Internet Researcher",
        goal="Find the most relevant and recent information about a given topic.",
        backstory="""You are a skilled researcher, adept at navigating the internet 
                    and gathering high-quality, reliable information.""",
        tools=[serper_dev_tool],
        verbose=True
    )

    research_task = Task(
        description="""Use the SerperDevTool to search for the 
                    most relevant and recent data about {topic}."""
                    "Extract the key insights from multiple sources.",
        agent=research_agent,
        tools=[serper_dev_tool],
        expected_output="A detailed research report with key insights and source references."
    )

    summarizer_agent = Agent(
    role="Content Summarizer",
    goal="Condense the key insights from research into a short and informative summary.",
    backstory="""You are an expert in distilling complex information into concise, 
                    easy-to-read summaries.""",
    verbose=True
    )

    summarization_task = Task(
        description="Summarize the research report into a concise and informative paragraph. "
                    "Ensure clarity, coherence, and completeness.",
        agent=summarizer_agent,
        expected_output="A well-structured summary with the most important insights."
    )

    fact_checker_agent = Agent(
        role="Fact-Checking Specialist",
        goal="Verify the accuracy of information and remove any misleading or false claims.",
        backstory="""You are an investigative journalist with a knack for validating facts, 
                    ensuring that only accurate information is published.""",
        tools=[serper_dev_tool],
        verbose=True
    )

    fact_checking_task = Task(
        description="Verify the summarized information for accuracy using the SerperDevTool. "
                    "Cross-check facts with reliable sources and correct any errors.",
        agent=fact_checker_agent,
        tools=[serper_dev_tool],
        expected_output="A fact-checked, verified summary of the research topic."
    )

    research_crew = Crew(
        agents=[research_agent, summarizer_agent, fact_checker_agent],
        tasks=[research_task, summarization_task, fact_checking_task],
        process=Process.sequential,
        verbose=True
    )

    result = research_crew.kickoff(inputs={"topic": "The impact of AI on job markets"})
    print(result)
    f = open("with_serper.md", "w")
    f.write(result.raw)
    f.close()