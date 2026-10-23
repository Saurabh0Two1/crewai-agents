from pydantic import BaseModel, Field
from crewai import Crew, Process, Agent, Task


class EntityRelationEntity(BaseModel):
    entity: str = Field(description="The first entity in the triplet")
    relation: str = Field(description="The relation between the first and second entity")
    entity: str = Field(description="The second entity in the triplet")


def structured_output():
    agent = Agent(
        role="Senior Linguist",
        goal="Analyse the query and extract entity-relation-entity triplets",
        backstory="You are a senior linguist that is known for your analytical skills.",
        verbose=True
    )

    task = Task(
        description="""Analyse the query and return structured JSON
                        output in the form of
                        - entity
                        - relation
                        - entity

                        The query is: {query}
                        """,
        expected_output="""A structured JSON object with the
                            entity-relation-entity triplets""",
        output_pydantic=EntityRelationEntity,
        verbose=True,
        agent=agent
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )

    response = crew.kickoff(inputs={"query": "Paris is the capital of France."})


    return response