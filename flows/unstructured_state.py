from crewai.flow.flow import Flow, start, listen

class TaskManagementFlow(Flow):
    @start()
    def generate_task(self):
        print(f"Flow started. State ID: {self.state['id']}")
        self.state["task"] = "Fix a critical bug in the application."
        self.state["status"] = "Pending"
        print (f"Task generated: {self.state['task']} (Status: {self.state['status']})")

    @listen(generate_task)
    def start_task(self):
        self.state["status"] = "In Progress"
        print(f"Task '{self.state['task']}' started (Status: {self.state['status']}).")

    @listen(start_task)
    def complete_task(self):
        self.state["completed"] = True
        print(f"Task Status updated: {self.state['status']}")
        print(f"Final Task State: {self.state}")