import os
import sys
from agent_setup import create_agent_session


def main():
    task = (
        os.environ.get("AGENT_TASK")
        or (" ".join(sys.argv[1:]) if len(sys.argv) > 1 else None)
        or "List the current directory."
    )

    print(f"Task: {task}\n")

    try:
        result = create_agent_session(task)
        print(f"Session ID: {result['session_id']}")
    except KeyError:
        print("Error: ANTHROPIC_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
