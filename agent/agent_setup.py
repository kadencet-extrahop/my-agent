import os
from anthropic import Anthropic


def create_agent_session(task: str) -> dict:
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    agent = client.beta.agents.create(
        name="Task Executor",
        model="claude-opus-4-7",
        system="You are a helpful task executor. Execute user requests safely and report results clearly.",
        tools=[{"type": "agent_toolset_20260401"}],
    )
    print(f"Agent created: {agent.id}")

    environment = client.beta.environments.create(
        name="execution-env",
        config={"type": "cloud", "networking": {"type": "unrestricted"}},
    )
    print(f"Environment created: {environment.id}")

    session = client.beta.sessions.create(
        agent=agent.id,
        environment_id=environment.id,
        title="Task session",
    )
    print(f"Session created: {session.id}\n")

    response_text = []

    with client.beta.sessions.events.stream(session.id) as stream:
        client.beta.sessions.events.send(
            session.id,
            events=[
                {
                    "type": "user.message",
                    "content": [{"type": "text", "text": task}],
                }
            ],
        )

        for event in stream:
            if event.type == "agent.message":
                for block in event.content:
                    if hasattr(block, "text"):
                        print(block.text, end="", flush=True)
                        response_text.append(block.text)
            elif event.type == "agent.tool_use":
                print(f"\n[Tool: {event.name}]", flush=True)
            elif event.type == "session.status_idle":
                print("\n\nDone.")
                break

    return {"session_id": session.id, "response": "".join(response_text)}
