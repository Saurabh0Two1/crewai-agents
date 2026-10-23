from pydantic import BaseModel

# Defining a structured state model
class TaskState(BaseModel):
    task: str = "None"
    status: str = "None"


from crewai.flow.flow import Flow, listen, start

class StructuredTaskFlow(Flow[TaskState]):

    @start()
    def generate_task(self):
        print(f"Flow started. State ID: {self.state.id}")
        self.state.task = "Develop a new API endpoint"
        self.state.status = "Pending"
        self.state.priority = "High"
        print(f"Task generated: {self.state.task} (Status: {self.state.status})")

    @listen(generate_task)
    def start_task(self):
        self.state.status = "In Progress"
        print(f"Task status updated: {self.state.status}")

    @listen(start_task)
    def complete_task(self):
        self.state.status = "Completed"
        print(f"Task status updated: {self.state.status}")
        print(f"Final Task State: {self.state}")