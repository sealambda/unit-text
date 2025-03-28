from pathlib import Path
from typing import Annotated

import typer
from rich import print
from rich.console import Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

from unit_text.core import Evaluation, IdeaModel, run_tests

app = typer.Typer(
    short_help="Unit tests for prose",
    help="""
    [bold green]unit-text[/] helps you write unit tests for prose.
    It uses :sparkles: agents :sparkles: to ensure
    that you meet the target audience's expectations,
    and that your writing achieves the desired outcomes.
    """,
    no_args_is_help=True,
    rich_markup_mode="rich",
)

OptConfig = Annotated[Path, typer.Option(help="The config file for the idea.")]
default_config = Path("unit-text.json")


@app.command()
def ideate(config: OptConfig = default_config):
    """Generate ideas for your writing."""
    print("I'll ask you a few questions to prepare for your writing.")

    existing_idea = (
        IdeaModel.model_validate_json(config.read_text())
        if config.exists()
        else IdeaModel(
            topic=None,
            audience=None,
            audience_knowledge=None,
            audience_care=None,
            desired_action=None,
            goal=None,
            perspective=None,
        )
    )

    topic = Prompt.ask(
        "What is the [bold green]topic[/]?",
        default=existing_idea.topic,
    )
    audience = Prompt.ask(
        "Who is your intended [bold red]audience[/]?",
        default=existing_idea.audience,
    )
    audience_knowledge = Prompt.ask(
        "What does your audience already know about the [bold green]topic[/]?",
        default=existing_idea.audience_knowledge,
    )
    audience_care = Prompt.ask(
        "Why do they care about what you're writing?",
        default=existing_idea.audience,
    )
    desired_action = Prompt.ask(
        "What do you want them to do differently after reading your writing?",
        default=existing_idea.desired_action,
    )

    goal = Prompt.ask(
        "What's the goal of this blog post?",
        default=existing_idea.goal,
    )
    perspective = Prompt.ask(
        "Why is your perspective on this [bold green]topic[/] interesting?",
        default=existing_idea.perspective,
    )

    idea = IdeaModel(
        topic=topic,
        audience=audience,
        audience_knowledge=audience_knowledge,
        audience_care=audience_care,
        desired_action=desired_action,
        goal=goal,
        perspective=perspective,
    )

    config.write_text(idea.model_dump_json(indent=2))

    print(f"[bold yellow]Idea[/] written to {config}")


@app.command()
def test(file: Path, config: OptConfig = default_config):
    """Run tests on the input file against the config."""
    print("Running tests...")

    idea = IdeaModel.model_validate_json(config.read_text())
    out = run_tests(file.read_text(), idea)

    def evaluation_panel(evaluation: Evaluation, title: str) -> Panel:
        return Panel(
            Group(
                Panel(
                    Markdown(evaluation.evaluation),
                    title="Evaluation",
                    style="blue",
                ),
                Panel(
                    Markdown(evaluation.suggestions),
                    title="Suggestions",
                    style="green",
                ),
            ),
            title=f"""{title} ({
                "[bold green]Passed[/]"
                if evaluation.test_passed
                else "[bold red]Failed[/]"
            })""",
        )

    panel_group = Group(
        evaluation_panel(
            out.clarity,
            title="Clarity",
        ),
        evaluation_panel(
            out.alignment_with_objectives,
            title="Alignment with Objectives",
        ),
        evaluation_panel(
            out.completeness,
            title="Completeness",
        ),
        Panel(
            Markdown(out.overall_suggestions),
            title="Overall Suggestions",
        ),
    )
    print(panel_group)
