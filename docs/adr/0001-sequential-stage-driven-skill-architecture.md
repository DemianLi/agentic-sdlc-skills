# Sequential Stage-Driven Skill Architecture

We decided to structure the Agentic Skill System using a strict 7-stage sequential naming convention (e.g., `/s1-init`, `/s2-align`) and a 1-to-1 mapping between SDLC stages and Agent Roles, instead of traditional functional naming (e.g., `/act-as-architect`). 

This forces the AI Agent to follow a strict Directed Acyclic Graph (DAG) dependency flow, preventing it from skipping crucial upstream steps (like generating an OpenSpec before TDD), at the acceptable cost of slightly less conversational command names. This ensures the output quality remains consistently high by enforcing the correct chronological order of operations.
