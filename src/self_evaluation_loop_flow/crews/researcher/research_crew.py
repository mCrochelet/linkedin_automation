from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class ResearchCrew:
    """Research Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def research_expert(self) -> Agent:

        return Agent(
            config=self.agents_config["research_expert"],
            # todo add tools to get the most relevant information
        )

    @task
    def research_hot_topics(self) -> Task:
        return Task(
            config=self.tasks_config["research_hot_topics"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Research Crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
