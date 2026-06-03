import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from todo_cli.storage import TodoStorage

console = Console()
storage = TodoStorage()


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Todo CLI - A powerful command-line todo manager"""
    if ctx.invoked_subcommand is None:
        ctx.invoke(list_todos)


@cli.command("add")
@click.argument("title")
@click.option("-p", "--priority", type=click.IntRange(1, 3), default=1, help="Priority: 1=low, 2=medium, 3=high")
def add_todo(title: str, priority: int) -> None:
    """Add a new todo"""
    todo = storage.add(title, priority)
    color = {1: "green", 2: "yellow", 3: "red"}[priority]
    console.print(f"[bold {color}]Added #{todo.id}[/bold {color}]: {todo.title} (priority: {todo.priority_label})")


@cli.command("list")
@click.option("-a", "--all", "show_all", is_flag=True, help="Show completed todos")
@click.option("-p", "--priority", type=click.IntRange(1, 3), help="Filter by priority")
def list_todos(show_all: bool = False, priority: int = None) -> None:
    """List todos"""
    todos = storage.list_all(show_completed=show_all, priority=priority)
    if not todos:
        console.print("[dim]No todos found.[/dim]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan", width=5)
    table.add_column("", style="dim", width=3)
    table.add_column("Title")
    table.add_column("Priority", width=10)
    table.add_column("Created", style="dim", width=12)

    for t in todos:
        status = "[green]+[/green]" if t.completed else "[red]o[/red]"
        table.add_row(
            str(t.id),
            status,
            f"[dim]{t.title}[/dim]" if t.completed else t.title,
            t.priority_label,
            t.created_at[:10],
        )
    console.print(table)
    console.print(f"\n[dim]{storage.pending_count} pending / {storage.count} total[/dim]")


@cli.command("done")
@click.argument("todo_id", type=int)
def complete_todo(todo_id: int) -> None:
    """Mark a todo as done"""
    todo = storage.complete(todo_id)
    if todo:
        console.print(f"[bold green]Completed #{todo.id}[/bold green]: {todo.title}")
    else:
        console.print(f"[bold red]Todo #{todo_id} not found or already completed.[/bold red]")


@cli.command("rm")
@click.argument("todo_id", type=int)
def remove_todo(todo_id: int) -> None:
    """Delete a todo"""
    if storage.delete(todo_id):
        console.print(f"[bold yellow]Deleted #{todo_id}[/bold yellow]")
    else:
        console.print(f"[bold red]Todo #{todo_id} not found.[/bold red]")


@cli.command("search")
@click.argument("query")
def search_todos(query: str) -> None:
    """Search todos by title"""
    todos = storage.search(query)
    if not todos:
        console.print(f"[dim]No todos matching '{query}'[/dim]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan", width=5)
    table.add_column("Title")
    table.add_column("Priority", width=10)
    for t in todos:
        table.add_row(str(t.id), t.title, t.priority_label)
    console.print(table)


@cli.command("stats")
def show_stats() -> None:
    """Show todo statistics"""
    total = storage.count
    pending = storage.pending_count
    completed = total - pending

    panel = Panel(
        f"Total: {total}  |  Pending: {pending}  |  Completed: {completed}",
        title="Todo Stats",
        border_style="blue",
    )
    console.print(panel)


if __name__ == "__main__":
    cli()
