from typing import Optional
from datetime import datetime
from crewai.flow.flow import Flow, listen, router, start, and_
from pydantic import BaseModel

from self_evaluation_loop_flow.crews.tov_crew.tov_crew import ToVCrew
from self_evaluation_loop_flow.crews.researcher.research_crew import ResearchCrew
from self_evaluation_loop_flow.crews.x_post_review_crew.x_post_review_crew import XPostReviewCrew


class ShakespeareXPostFlowState(BaseModel):
    x_post: str = ""
    tov_instructions: str = ""
    feedback: Optional[str] = None
    valid: bool = False
    retry_count: int = 0


class ShakespeareXPostFlow(Flow[ShakespeareXPostFlowState]):

    @start()
    def extract_tov(self):
        print("Extracting tone of voice")
        
        result = (
            ToVCrew()
            .crew()
            .kickoff()
        )

        # print("ToV extracted, instructions:", result.raw)
        self.state.tov_instructions = result.raw

    @start()
    def research_post_topics(self):
        print("Researching post topics")
        result = (
            ResearchCrew()
            .crew()
            .kickoff(inputs={
                "topic": "ai productivity tools in product management", 
                "current_year": str(datetime.now().year), 
                "current_month": str(datetime.now().month),
                "current_day": str(datetime.now().day)
                }
            )
        )

        print("Researching post topics:", result.raw)

        return "ai productivity tools in product management"

    @listen(and_(extract_tov, research_post_topics))
    def evaluate_x_post(self):
        if self.state.retry_count > 3:
            return "max_retry_exceeded"

        result = XPostReviewCrew().crew().kickoff(inputs={"x_post": self.state.x_post})
        self.state.valid = result["valid"]
        self.state.feedback = result["feedback"]

        print("valid", self.state.valid)
        print("feedback", self.state.feedback)
        self.state.retry_count += 1

        # if self.state.valid:
        return "complete"

    @listen("complete")
    def save_result(self):
        print("X post is valid")
        print("X post:", self.state.x_post)

        # Save the valid X post to a file
        with open("x_post.txt", "w") as file:
            file.write(self.state.x_post)

    @listen("max_retry_exceeded")
    def max_retry_exceeded_exit(self):
        print("Max retry count exceeded")
        print("X post:", self.state.x_post)
        print("Feedback:", self.state.feedback)


def kickoff():
    shakespeare_flow = ShakespeareXPostFlow()
    shakespeare_flow.kickoff()


def plot():
    shakespeare_flow = ShakespeareXPostFlow()
    shakespeare_flow.plot()


if __name__ == "__main__":
    kickoff()
