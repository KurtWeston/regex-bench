"""Format and display benchmark results."""
from typing import Dict, List, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box


class Reporter:
    def __init__(self):
        self.console = Console()
    
    def print_single_result(self, result: Dict[str, Any]):
        """Print single benchmark result."""
        table = Table(title=f"Benchmark Results: {result['pattern']}", box=box.ROUNDED)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Engine", result['engine'])
        table.add_row("Iterations", str(result['iterations']))
        table.add_row("Matches", str(result['matches']))
        table.add_row("Mean Time", f"{result['mean']*1000:.4f} ms")
        table.add_row("Median Time", f"{result['median']*1000:.4f} ms")
        table.add_row("Std Dev", f"{result['stdev']*1000:.4f} ms")
        table.add_row("Min Time", f"{result['min']*1000:.4f} ms")
        table.add_row("Max Time", f"{result['max']*1000:.4f} ms")
        table.add_row("Total Time", f"{result['total']*1000:.2f} ms")
        
        self.console.print(table)
    
    def print_comparison(self, results: List[Dict[str, Any]]):
        """Print comparison of multiple patterns."""
        table = Table(title="Pattern Comparison", box=box.ROUNDED)
        table.add_column("Pattern", style="cyan")
        table.add_column("Mean (ms)", style="green")
        table.add_column("Median (ms)", style="green")
        table.add_column("Std Dev (ms)", style="yellow")
        table.add_column("Matches", style="blue")
        
        sorted_results = sorted(results, key=lambda x: x['mean'])
        
        for i, result in enumerate(sorted_results):
            pattern = result['pattern'][:50] + '...' if len(result['pattern']) > 50 else result['pattern']
            rank = "⭐ " if i == 0 else "   "
            table.add_row(
                rank + pattern,
                f"{result['mean']*1000:.4f}",
                f"{result['median']*1000:.4f}",
                f"{result['stdev']*1000:.4f}",
                str(result['matches'])
            )
        
        self.console.print(table)
        
        if len(sorted_results) > 1:
            fastest = sorted_results[0]
            slowest = sorted_results[-1]
            speedup = slowest['mean'] / fastest['mean']
            self.console.print(f"\n[green]Fastest pattern is {speedup:.2f}x faster than slowest[/green]")
    
    def print_analysis(self, analysis: Dict[str, Any]):
        """Print regex analysis results."""
        self.console.print(Panel(f"[cyan]Pattern:[/cyan] {analysis['pattern']}", title="Analysis"))
        self.console.print(f"\n[yellow]Complexity Score:[/yellow] {analysis['complexity']}")
        
        if analysis['warnings']:
            self.console.print("\n[red]⚠ Warnings:[/red]")
            for warning in analysis['warnings']:
                self.console.print(f"  • {warning}")
        
        if analysis['suggestions']:
            self.console.print("\n[green]💡 Suggestions:[/green]")
            for suggestion in analysis['suggestions']:
                self.console.print(f"  • {suggestion}")
        
        if not analysis['warnings']:
            self.console.print("\n[green]✓ No major issues detected[/green]")
    
    def print_backtracking_result(self, is_catastrophic: bool, details: Dict[str, Any]):
        """Print backtracking detection results."""
        if is_catastrophic:
            self.console.print(Panel(
                f"[red]⚠ CATASTROPHIC BACKTRACKING DETECTED[/red]\n\n"
                f"Pattern: {details['pattern']}\n"
                f"Max Time: {details['max_time']*1000:.2f} ms\n"
                f"Growth Rate: {details['growth_rate']:.2f}x",
                title="Backtracking Detection",
                border_style="red"
            ))
        else:
            self.console.print(Panel(
                f"[green]✓ No catastrophic backtracking detected[/green]\n\n"
                f"Pattern: {details['pattern']}\n"
                f"Max Time: {details['max_time']*1000:.2f} ms\n"
                f"Growth Rate: {details['growth_rate']:.2f}x",
                title="Backtracking Detection",
                border_style="green"
            ))