from typing import Optional
from datetime import datetime
from crewai.flow.flow import Flow, listen, router, start, and_, or_
from pydantic import BaseModel

from self_evaluation_loop_flow.crews.tov_crew.tov_crew import ToVCrew
from self_evaluation_loop_flow.crews.researcher.research_crew import ResearchCrew
from self_evaluation_loop_flow.crews.post_writer.post_writer_crew import PostWriterCrew
from self_evaluation_loop_flow.crews.post_review_crew.post_review_crew import PostReviewCrew


post_topic = "Impact of ai on the build-buy-partner decisions - does AI make it easier and cheaper to build than buy?"

class ShakespeareXPostFlowState(BaseModel):
    post: str = ""
    tov_instructions: str = ""
    research_results: str = ""
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
                "topic": post_topic, 
                "current_year": str(datetime.now().year), 
                "current_month": str(datetime.now().month),
                "current_day": str(datetime.now().day)
                }
            )
        )

        self.state.research_results = result.raw
        print("Researching post topics:", result.raw)

    @listen(or_(and_(extract_tov, research_post_topics), "retry"))
    def write_post(self):
        print("Writing a post based on the research results and tone of voice instructions")
        result = (
            PostWriterCrew()
            .crew()
            .kickoff(inputs={
                "topic": post_topic, 
                "research_results": self.state.research_results,
                "tov_instructions": self.state.tov_instructions,
                "feedback": self.state.feedback,
                "previous_post": self.state.post
                }
            )
        )

        self.state.post = result.raw
        print("Post written:", result.raw)
    
    @router(write_post)
    def evaluate_post(self):
        if self.state.retry_count > 3:
            return "max_retry_exceeded"

        result = PostReviewCrew().crew().kickoff(inputs={
            "post": self.state.post, 
            "topic": post_topic, 
            "tov_instructions": self.state.tov_instructions
            }
        )
        
        self.state.valid = result["valid"]
        self.state.feedback = result["feedback"]

        print("valid", self.state.valid)
        print("feedback", self.state.feedback)
        self.state.retry_count += 1

        if self.state.valid:
            return "complete"
        else:
            return "retry"

    @listen("complete")
    def save_result(self):
        print("Post is valid")
        print("Post:", self.state.post)

        # Save the valid X post to a file
        with open("post.txt", "w") as file:
            file.write(self.state.post)

    @listen("max_retry_exceeded")
    def max_retry_exceeded_exit(self):
        print("Max retry count exceeded")
        print("Post:", self.state.post)
        print("Feedback:", self.state.feedback)


def kickoff():
    shakespeare_flow = ShakespeareXPostFlow()
    shakespeare_flow.kickoff()


def plot():
    shakespeare_flow = ShakespeareXPostFlow()
    shakespeare_flow.plot()


if __name__ == "__main__":
    kickoff()
