"""CLI entrypoint for the Research Assistant capstone.

Usage:
    python cli.py "How many people live in Tokyo, and what is that divided by 100?"
"""

import sys
import json
import time
import argparse
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.json import JSON

load_dotenv(dotenv_path="../../.env")
from assistant import run    # noqa: E402

console = Console()


def main():
    parser = argparse.ArgumentParser(description="Research Assistant")
    parser.add_argument("question", nargs="+", help="The research question")
    parser.add_argument("--max-steps", type=int, default=10)
    args = parser.parse_args()
    question = " ".join(args.question)

    console.print(Panel(f"[bold]Question:[/bold] {question}", title="research-assistant"))
    t0 = time.perf_counter()
    result = run(question, max_steps=args.max_steps)
    dt = time.perf_counter() - t0

    if result["ok"]:
        console.print(Panel(JSON(json.dumps(result["report"], indent=2)), title="Report", border_style="green"))
    else:
        console.print(Panel(f"[red]Did not complete: {result['reason']}[/red]\n"
                            f"{json.dumps(result.get('report'), indent=2)}",
                            title="Result", border_style="yellow"))

    u = result["usage"]
    console.print(
        f"[dim]steps={result['steps']}  time={dt:.1f}s  "
        f"in={u.input_tokens}  out={u.output_tokens}  "
        f"cache_read={u.cache_read}  cache_write={u.cache_write}[/dim]"
    )


if __name__ == "__main__":
    main()
