from typing import Optional

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel
from self_evaluation_loop_flow.tools.CharacterCounterTool import CharacterCounterTool


class PostVerification(BaseModel):
    valid: bool
    feedback: Optional[str]


@CrewBase
class PostReviewCrew:
    """Post Review Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def post_verifier(self) -> Agent:
        return Agent(
            config=self.agents_config["post_verifier"],
        )

    @task
    def verify_post(self) -> Task:
        return Task(
            config=self.tasks_config["verify_post"],
            output_pydantic=PostVerification,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Post Review Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
