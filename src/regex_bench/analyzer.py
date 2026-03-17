"""Regex complexity analyzer."""
import re
from typing import Dict, List, Any


class RegexAnalyzer:
    def __init__(self):
        self.warnings = []
        self.suggestions = []
    
    def analyze(self, pattern: str) -> Dict[str, Any]:
        """Analyze regex complexity and provide suggestions."""
        self.warnings = []
        self.suggestions = []
        
        complexity = self._calculate_complexity(pattern)
        self._check_nested_quantifiers(pattern)
        self._check_alternation(pattern)
        self._check_unbounded_repetition(pattern)
        self._check_backtracking_constructs(pattern)
        
        return {
            'pattern': pattern,
            'complexity': complexity,
            'warnings': self.warnings,
            'suggestions': self.suggestions
        }
    
    def _calculate_complexity(self, pattern: str) -> int:
        """Calculate pattern complexity score."""
        score = 0
        score += pattern.count('*') * 2
        score += pattern.count('+') * 2
        score += pattern.count('?')
        score += pattern.count('|') * 3
        score += pattern.count('(') * 2
        score += pattern.count('[') * 1
        return score
    
    def _check_nested_quantifiers(self, pattern: str):
        """Check for nested quantifiers."""
        if re.search(r'[*+?][*+?]', pattern) or re.search(r'\([^)]*[*+?][^)]*\)[*+?]', pattern):
            self.warnings.append('Nested quantifiers detected - high risk of catastrophic backtracking')
            self.suggestions.append('Use atomic groups (?>) or possessive quantifiers (*+, ++)')
    
    def _check_alternation(self, pattern: str):
        """Check for complex alternation."""
        alternations = pattern.count('|')
        if alternations > 3:
            self.warnings.append(f'Multiple alternations ({alternations}) may slow matching')
            self.suggestions.append('Consider using character classes or simplifying alternatives')
    
    def _check_unbounded_repetition(self, pattern: str):
        """Check for unbounded repetition."""
        if re.search(r'\.\*', pattern) or re.search(r'\.\+', pattern):
            self.warnings.append('Unbounded repetition with .* or .+ can cause performance issues')
            self.suggestions.append('Use more specific patterns or limit repetition with {n,m}')
    
    def _check_backtracking_constructs(self, pattern: str):
        """Check for constructs that cause excessive backtracking."""
        if re.search(r'\([^)]*\*[^)]*\)\*', pattern):
            self.warnings.append('Repeated group with quantifier inside - exponential backtracking risk')
            self.suggestions.append('Refactor to avoid nested repetition or use atomic groups')
        
        if re.search(r'\w\*\w', pattern) or re.search(r'\w\+\w', pattern):
            self.warnings.append('Overlapping character classes can cause backtracking')
            self.suggestions.append('Use possessive quantifiers or be more specific')