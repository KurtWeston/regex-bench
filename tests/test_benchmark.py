"""Tests for benchmark module."""
import pytest
import time
from regex_bench.benchmark import RegexBenchmark


class TestRegexBenchmark:
    def test_run_basic_pattern(self):
        """Test basic benchmark execution."""
        bench = RegexBenchmark(engine='re')
        result = bench.run(r'\d+', '123abc456', iterations=10)
        
        assert result['pattern'] == r'\d+'
        assert result['engine'] == 're'
        assert result['iterations'] == 10
        assert result['matches'] == 10
        assert result['mean'] > 0
        assert result['median'] > 0
        assert result['min'] > 0
        assert result['max'] >= result['min']
        assert result['total'] > 0
    
    def test_run_no_matches(self):
        """Test pattern with no matches."""
        bench = RegexBenchmark()
        result = bench.run(r'xyz', 'abc123', iterations=5)
        
        assert result['matches'] == 0
        assert result['mean'] > 0
    
    def test_invalid_pattern(self):
        """Test invalid regex pattern."""
        bench = RegexBenchmark()
        
        with pytest.raises(ValueError, match="Invalid pattern"):
            bench.run(r'[invalid', 'test', iterations=1)
    
    def test_regex_engine_not_installed(self):
        """Test error when regex module not available."""
        import sys
        import regex_bench.benchmark as bm
        
        original = bm.HAS_REGEX
        bm.HAS_REGEX = False
        
        try:
            with pytest.raises(ImportError, match="regex module not installed"):
                RegexBenchmark(engine='regex')
        finally:
            bm.HAS_REGEX = original
    
    def test_detect_backtracking_safe_pattern(self):
        """Test backtracking detection with safe pattern."""
        bench = RegexBenchmark()
        is_catastrophic, details = bench.detect_backtracking(
            r'\d+', 'a' * 100, threshold=0.1
        )
        
        assert is_catastrophic is False
        assert details['pattern'] == r'\d+'
        assert details['growth_rate'] >= 1
        assert len(details['timings']) > 0
    
    def test_detect_backtracking_dangerous_pattern(self):
        """Test backtracking detection with dangerous pattern."""
        bench = RegexBenchmark()
        is_catastrophic, details = bench.detect_backtracking(
            r'(a+)+b', 'a' * 20, threshold=0.001
        )
        
        assert 'pattern' in details
        assert 'growth_rate' in details
        assert 'timings' in details
        assert len(details['timings']) > 0