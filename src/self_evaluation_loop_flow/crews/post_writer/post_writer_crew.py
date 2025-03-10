from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from crewai_tools import (
    SerperDevTool,
    WebsiteSearchTool
)

search_tool = SerperDevTool()
web_rag_tool = WebsiteSearchTool()

@CrewBase
class PostWriterCrew:
    """Post Writer Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def post_writer(self) -> Agent:

        return Agent(
            config=self.agents_config["post_writer"],
            tools=[search_tool, web_rag_tool],
        )

    @task
    def write_post(self) -> Task:
        return Task(
            config=self.tasks_config["write_post"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Post Writer Crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=False,
        )
