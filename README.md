# regex-bench

Benchmark and compare regex pattern performance to detect catastrophic backtracking and optimize production patterns

## Features

- Benchmark single or multiple regex patterns against provided test inputs
- Measure execution time with statistical analysis (mean, median, std dev)
- Detect catastrophic backtracking by monitoring execution time growth
- Compare multiple equivalent patterns side-by-side with performance metrics
- Analyze regex complexity and identify problematic constructs (nested quantifiers, alternation)
- Suggest optimizations like atomic groups, possessive quantifiers, or pattern simplification
- Support both Python's re module and the more powerful regex module
- Generate colorized terminal output with tables showing timing comparisons
- Export results as JSON for integration with CI/CD pipelines
- Provide sample inputs generation for testing patterns without real data
- Warn about common anti-patterns like excessive backtracking or unbounded repetition
- Support reading patterns and inputs from files for batch testing

## How to Use

Use this project when you need to:

- Quickly solve problems related to regex-bench
- Integrate python functionality into your workflow
- Learn how python handles common patterns with click

## Installation

```bash
# Clone the repository
git clone https://github.com/KurtWeston/regex-bench.git
cd regex-bench

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Built With

- python using click

## Dependencies

- `click`
- `rich`
- `regex`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
