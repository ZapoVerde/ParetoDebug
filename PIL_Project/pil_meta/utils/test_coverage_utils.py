# test_coverage_utils.py
"""
Test Coverage Utilities (utils)

Provides functions to estimate static test coverage by scanning test files
and matching function/method/class names to code symbols.
"""

import os
import re
from typing import List, Dict

def estimate_test_coverage(symbols: List[Dict], test_dir: str = "tests") -> List[Dict]:
    """
    Updates the 'test_coverage' field for each symbol based on whether
    its function/class/method name appears in any test file.

    Parameters:
        symbols (list[dict]): List of code symbol metadata dicts.
        test_dir (str): Directory containing test files.

    Returns:
        list[dict]: The same list, with 'test_coverage' set for each symbol.
    """
    # Gather all words from all test files
    mentioned = set()
    pattern = re.compile(r"\b([a-zA-Z_][a-zA-Z0-9_]*)\b")

    for root, _, files in os.walk(test_dir):
        for file in files:
            if file.startswith("test_") and file.endswith(".py"):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    for line in f:
                        for match in pattern.findall(line):
                            mentioned.add(match)

    # Mark coverage for each symbol
    for sym in symbols:
        # Consider class, function, or method names
        if sym.get("function") in mentioned:
            sym["test_coverage"] = True
        else:
            sym["test_coverage"] = False

    return symbols
