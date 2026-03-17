"""Tests for analyzer module."""
import pytest
from regex_bench.analyzer import RegexAnalyzer


class TestRegexAnalyzer:
    def test_analyze_simple_pattern(self):
        """Test analysis of simple pattern."""
        analyzer = RegexAnalyzer()
        result = analyzer.analyze(r'\d+')
        
        assert result['pattern'] == r'\d+'
        assert result['complexity'] >= 0
        assert isinstance(result['warnings'], list)
        assert isinstance(result['suggestions'], list)
    
    def test_complexity_calculation(self):
        """Test complexity score calculation."""
        analyzer = RegexAnalyzer()
        
        simple = analyzer.analyze(r'abc')
        complex_pattern = analyzer.analyze(r'(a+|b*)+c?')
        
        assert complex_pattern['complexity'] > simple['complexity']
    
    def test_nested_quantifiers_warning(self):
        """Test detection of nested quantifiers."""
        analyzer = RegexAnalyzer()
        result = analyzer.analyze(r'(a+)+')
        
        assert len(result['warnings']) > 0
        assert any('nested quantifiers' in w.lower() for w in result['warnings'])
        assert len(result['suggestions']) > 0
    
    def test_alternation_warning(self):
        """Test detection of excessive alternation."""
        analyzer = RegexAnalyzer()
        result = analyzer.analyze(r'a|b|c|d|e|f')
        
        assert any('alternation' in w.lower() for w in result['warnings'])
    
    def test_unbounded_repetition_warning(self):
        """Test detection of unbounded repetition."""
        analyzer = RegexAnalyzer()
        result = analyzer.analyze(r'.*test')
        
        assert any('unbounded' in w.lower() for w in result['warnings'])
        assert any('.*' in w or '.+' in w for w in result['warnings'])