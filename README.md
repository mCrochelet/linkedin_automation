# LinkedIn Post Crew

Welcome to the LinkedIn Post Crew project, powered by [crewAI](https://crewai.com). This project creates professional LinkedIn posts on specified topics through an intelligent workflow of AI agents working together. It leverages crewAI's multi-agent system to research, write, review, and refine content in a self-improving loop.

## Overview

This application creates high-quality LinkedIn posts through a collaborative AI workflow with the following steps:

1. **Extract Tone of Voice**: Establishes the writing style and tone guidelines for the post.

2. **Research the Topic**: Gathers current, relevant information on the specified topic, including citations to credible sources.

3. **Write the Post**: Creates a LinkedIn post based on research findings and tone guidelines.

4. **Review and Validate**: Evaluates the post against quality criteria and provides feedback if necessary.

5. **Iterative Refinement**: If the post doesn't meet the criteria, it iterates with feedback until a valid post is created or maximum retry count is reached.

6. **Save the Post**: Once validated, the final post is saved to a file.

The current implementation focuses on creating professional posts about topics with proper citations to relevant sources.

## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system.

To install the required dependencies:

```bash
pip install crewai
```

### Configuration

1. **Add your API keys into the `.env` file:**
   - `OPENAI_API_KEY` for AI agent functionality
   - `SERPER_API_KEY` for web search capabilities

2. **Customize the components:**
   - Modify `config/agents.yaml` to define your agents' capabilities and roles
   - Modify `config/tasks.yaml` to define specific tasks for each agent
   - Adjust crew files in `src/self_evaluation_loop_flow/crews/` to customize agent behaviors

3. **Change the post topic:**
   - Edit the `post_topic` variable in `src/self_evaluation_loop_flow/main.py`

## Running the Project

To generate a LinkedIn post, run this from the root folder of your project:
    
```bash
crewai flow kickoff 
```

This command initiates the flow, assembling the agents and assigning them tasks as defined in your configuration.

The output will be saved to `post.txt` in the root directory.

## Project Components

The project consists of several key components:

1. **Tone of Voice Crew**: Defines the writing style and guidelines for the post

2. **Research Crew**: Gathers current, relevant information on the specified topic, including credible sources

3. **Post Writer Crew**: Creates a LinkedIn post based on research and tone guidelines

4. **Post Review Crew**: Validates the post against quality criteria and provides feedback

These components work together in a coordinated flow, defined in `src/self_evaluation_loop_flow/main.py`, to produce a polished final result.

## Example Output

The system generates professional LinkedIn posts with:
- Well-researched content
- Citations to credible sources
- Professional tone appropriate for the LinkedIn platform
- Engaging questions to prompt discussion
