# Agentic Skill System

This context defines the ubiquitous language for the 7-stage Agentic Software Development Lifecycle (SDLC) framework. It establishes how AI Agents are directed through different phases of software development using specialized, atomic instructions.

## Language

**Stage**:
One of the 7 sequential phases of the Agentic SDLC (from Initialization to Delivery).
*Avoid*: Phase, Step, Level

**Role**:
The specific persona an AI Agent assumes to execute a given Stage. There is a strict 1-to-1 mapping between a Role and a Stage (e.g., Stage 1 is always executed by the Foundation Engineer).
*Avoid*: Agent, Persona, Actor

**Skill**:
A discrete, atomic Markdown file containing instructions for a specific Role to accomplish a specific task within a Stage.
*Avoid*: Prompt, Command, Script

**Slash Command**:
The user-facing trigger for a Skill, following the strict naming convention `/s{StageNumber}-{Action}` (e.g., `/s4-tdd`).
*Avoid*: Trigger, Command Line, Input

**OpenSpec**:
The highly rigorous specification document format produced in Stage 3, serving as the absolute single source of truth (Source of Truth) for Stage 4's Test-Driven Development (TDD).
*Avoid*: PRD, Design Doc, Requirements

**Atomic Task**:
A functionally independent, minimal unit of work derived from the technical design in Stage 3, suitable for concurrent implementation in Stage 4.
*Avoid*: Ticket, Issue, Story

## Relationships

- A **Stage** requires exactly one **Role** to execute it.
- A **Role** possesses multiple atomic **Skills**.
- A **Skill** is invoked via exactly one **Slash Command**.
- The **OpenSpec** dictates the acceptable outcomes for an **Atomic Task**.

## Example dialogue

> **Dev:** "I need the Agent to write tests for this new feature."
> **Architect:** "You can't jump straight to the `/s4-tdd` **Slash Command**. The **Role** for Stage 4 needs the **OpenSpec** first. Run `/s3-breakdown` to generate the **Atomic Tasks** and specs."

## Flagged ambiguities

- "Agent" vs "Role" — resolved: An "Agent" is the underlying AI model (e.g., Claude, Gemini). A "Role" is the specific hat the Agent wears (e.g., Foundation Engineer) when executing a Skill.
