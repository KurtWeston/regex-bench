"""Tests for CLI interface."""
import pytest
import json
from click.testing import CliRunner
from regex_bench.cli import cli
from pathlib import Path
import tempfile


class TestCLI:
    def test_bench_command_basic(self):
        """Test basic bench command."""
        runner = CliRunner()
        result = runner.invoke(cli, ['bench', r'\d+', '-i', '123abc', '-n', '10'])
        
        assert result.exit_code == 0
        assert 'Benchmark Results' in result.output or result.output != ''
    
    def test_bench_command_json_output(self):
        """Test bench command with JSON output."""
        runner = CliRunner()
        result = runner.invoke(cli, [
            'bench', r'\d+', '-i', '123', '-n', '5', '--json'
        ])
        
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert 'pattern' in data
        assert 'mean' in data
        assert data['iterations'] == 5
    
    def test_compare_command(self):
        """Test compare command with pattern file."""
        runner = CliRunner()
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(r'\d+' + '\n')
            f.write(r'[0-9]+' + '\n')
            pattern_file = f.name
        
        try:
            result = runner.invoke(cli, [
                'compare', '-p', pattern_file, '-i', '123', '-n', '5'
            ])
            assert result.exit_code == 0
        finally:
            Path(pattern_file).unlink()
    
    def test_analyze_command(self):
        """Test analyze command."""
        runner = CliRunner()
        result = runner.invoke(cli, ['analyze', r'(a+)+b'])
        
        assert result.exit_code == 0
        assert result.output != ''
    
    def test_detect_command(self):
        """Test detect backtracking command."""
        runner = CliRunner()
        result = runner.invoke(cli, [
            'detect', r'\d+', '-i', 'abc123', '--threshold', '0.1'
        ])
        
        assert result.exit_code == 0