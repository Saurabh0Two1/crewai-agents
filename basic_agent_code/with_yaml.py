def multiagent_with_yaml():
    
    from crewai import Agent, Task, Crew, Process
    from crewai_tools import SerperDevTool
    
    import yaml

    # Load YAML Configuration
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)

    serper_dev_tool = SerperDevTool()


    research_agent = Agent(
        role=config["agents"]["research_agent"]["role"],
        goal=config["agents"]["research_agent"]["goal"],
        backstory=config["agents"]["research_agent"]["backstory"],
        tools=[serper_dev_tool],
        verbose=True
    )

    research_task = Task(
        description=config["tasks"]["research_task"]["description"],
        agent=research_agent,
        tools=[serper_dev_tool],
        expected_output=config["tasks"]["research_task"]["expected_output"]
    )

    summarization_agent = Agent(
        role=config["agents"]["summarization_agent"]["role"],
        goal=config["agents"]["summarization_agent"]["goal"],
        backstory=config["agents"]["summarization_agent"]["backstory"],
        verbose=True
    )

    fact_checker_agent = Agent(
        role=config["agents"]["fact_checker_agent"]["role"],
        goal=config["agents"]["fact_checker_agent"]["goal"],
        backstory=config["agents"]["fact_checker_agent"]["backstory"],
        tools=[serper_dev_tool],
        verbose=True
    )

    summarization_task = Task(
        description=config["tasks"]["summarization_task"]["description"],
        agent=summarization_agent,
        expected_output=config["tasks"]["summarization_task"]["expected_output"],
    )

    fact_checking_task = Task(
        description=config["tasks"]["fact_checking_task"]["description"],
        agent=fact_checker_agent,
        tools=[serper_dev_tool],
        expected_output=config["tasks"]["fact_checking_task"]["expected_output"],
    )

    research_crew = Crew(
        agents=[research_agent, summarization_agent, fact_checker_agent],
        tasks=[research_task, summarization_task, fact_checking_task],
        process=Process.sequential,
        verbose=True
    )

    result = research_crew.kickoff(inputs={"topic": "The impact of AI on job markets"})
    
    print("\nFinal Verified Summary:\n", result)
