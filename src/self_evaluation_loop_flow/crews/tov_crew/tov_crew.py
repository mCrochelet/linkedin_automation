from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource

text_source = TextFileKnowledgeSource(
    file_path=["20250310 - linkedin posts extract.txt"],
    metadata={
        "source": "linkedin",
        "content_type": "posts",
        "date": "2025-03-10",
        "purpose": "content_analysis",
        "platform": "linkedin",
        "document_type": "extract"
    }
)

@CrewBase
class ToVCrew:
    """ToV Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def expert_copywriter_tov(self) -> Agent:

        return Agent(
            config=self.agents_config["expert_copywriter_tov"],
            knowledge=[text_source],
        )

    @task
    def extract_tov(self) -> Task:
        return Task(
            config=self.tasks_config["extract_tov"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ToV Crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            knowledge_sources=[text_source],
            verbose=False,
        )
