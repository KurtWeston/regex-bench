"""Core benchmarking engine."""
import re
import time
import statistics
from typing import Dict, List, Tuple, Any

try:
    import regex
    HAS_REGEX = True
except ImportError:
    HAS_REGEX = False


class RegexBenchmark:
    def __init__(self, engine: str = 're'):
        self.engine = engine
        if engine == 'regex' and not HAS_REGEX:
            raise ImportError("regex module not installed. Install with: pip install regex")
    
    def _compile_pattern(self, pattern: str):
        """Compile pattern with selected engine."""
        try:
            if self.engine == 'regex':
                return regex.compile(pattern)
            return re.compile(pattern)
        except Exception as e:
            raise ValueError(f"Invalid pattern: {e}")
    
    def run(self, pattern: str, test_input: str, iterations: int = 1000) -> Dict[str, Any]:
        """Run benchmark on a pattern."""
        compiled = self._compile_pattern(pattern)
        timings = []
        matches = 0
        
        for _ in range(iterations):
            start = time.perf_counter()
            result = compiled.search(test_input)
            end = time.perf_counter()
            timings.append(end - start)
            if result:
                matches += 1
        
        return {
            'pattern': pattern,
            'engine': self.engine,
            'iterations': iterations,
            'matches': matches,
            'mean': statistics.mean(timings),
            'median': statistics.median(timings),
            'stdev': statistics.stdev(timings) if len(timings) > 1 else 0,
            'min': min(timings),
            'max': max(timings),
            'total': sum(timings)
        }
    
    def detect_backtracking(self, pattern: str, test_input: str, threshold: float = 0.1) -> Tuple[bool, Dict]:
        """Detect catastrophic backtracking by testing with increasing input sizes."""
        compiled = self._compile_pattern(pattern)
        timings = []
        sizes = []
        
        for multiplier in [1, 2, 4, 8, 16]:
            test_str = test_input * multiplier
            sizes.append(len(test_str))
            
            start = time.perf_counter()
            try:
                compiled.search(test_str)
            except:
                pass
            end = time.perf_counter()
            
            elapsed = end - start
            timings.append(elapsed)
            
            if elapsed > threshold:
                growth_rate = elapsed / timings[0] if timings[0] > 0 else float('inf')
                return True, {
                    'pattern': pattern,
                    'threshold': threshold,
                    'max_time': elapsed,
                    'growth_rate': growth_rate,
                    'sizes': sizes,
                    'timings': timings
                }
        
        if len(timings) > 1:
            growth_rate = timings[-1] / timings[0] if timings[0] > 0 else 1
        else:
            growth_rate = 1
        
        return False, {
            'pattern': pattern,
            'threshold': threshold,
            'max_time': max(timings),
            'growth_rate': growth_rate,
            'sizes': sizes,
            'timings': timings
        }