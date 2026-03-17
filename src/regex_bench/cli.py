"""CLI interface for regex-bench."""
import click
import json
import sys
from pathlib import Path
from .benchmark import RegexBenchmark
from .analyzer import RegexAnalyzer
from .reporter import Reporter


@click.group()
@click.version_option()
def cli():
    """Benchmark and compare regex patterns."""
    pass


@cli.command()
@click.argument('pattern')
@click.option('-i', '--input', 'test_input', required=True, help='Test input string')
@click.option('-n', '--iterations', default=1000, help='Number of iterations')
@click.option('--engine', type=click.Choice(['re', 'regex']), default='re')
@click.option('--json', 'json_output', is_flag=True, help='Output as JSON')
def bench(pattern, test_input, iterations, engine, json_output):
    """Benchmark a single regex pattern."""
    benchmark = RegexBenchmark(engine=engine)
    result = benchmark.run(pattern, test_input, iterations)
    
    if json_output:
        click.echo(json.dumps(result, indent=2))
    else:
        reporter = Reporter()
        reporter.print_single_result(result)


@cli.command()
@click.option('-p', '--patterns', required=True, help='File with patterns (one per line)')
@click.option('-i', '--input', 'test_input', required=True, help='Test input string')
@click.option('-n', '--iterations', default=1000, help='Number of iterations')
@click.option('--engine', type=click.Choice(['re', 'regex']), default='re')
@click.option('--json', 'json_output', is_flag=True, help='Output as JSON')
def compare(patterns, test_input, iterations, engine, json_output):
    """Compare multiple regex patterns."""
    pattern_list = Path(patterns).read_text().strip().split('\n')
    benchmark = RegexBenchmark(engine=engine)
    results = []
    
    for pattern in pattern_list:
        if pattern.strip():
            result = benchmark.run(pattern.strip(), test_input, iterations)
            results.append(result)
    
    if json_output:
        click.echo(json.dumps(results, indent=2))
    else:
        reporter = Reporter()
        reporter.print_comparison(results)


@cli.command()
@click.argument('pattern')
def analyze(pattern):
    """Analyze regex complexity and suggest optimizations."""
    analyzer = RegexAnalyzer()
    analysis = analyzer.analyze(pattern)
    reporter = Reporter()
    reporter.print_analysis(analysis)


@cli.command()
@click.argument('pattern')
@click.option('-i', '--input', 'test_input', required=True, help='Test input string')
@click.option('--threshold', default=0.1, help='Backtracking threshold in seconds')
def detect(pattern, test_input, threshold):
    """Detect catastrophic backtracking."""
    benchmark = RegexBenchmark()
    is_catastrophic, details = benchmark.detect_backtracking(pattern, test_input, threshold)
    reporter = Reporter()
    reporter.print_backtracking_result(is_catastrophic, details)


if __name__ == '__main__':
    cli()