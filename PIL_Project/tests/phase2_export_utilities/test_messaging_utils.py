# tests/phase2_export_utilities/test_messaging_utils.py
"""
Unit tests for pil_meta.utils.messaging_utils.

Covers:
- Debug message toggle
- Info/warning/error formatting (stdout/stderr capture)
- Section headers and all reporting helpers

@tags: ["test", "messaging_utils", "unit"]
@status: "stable"
"""

import sys
import io
import pytest
import types
from pil_meta.utils import messaging_utils

def test_set_debug_and_debug_output(capsys):
    """
    Debug messages print only when debug is enabled.
    """
    messaging_utils.set_debug(False)
    messaging_utils.debug("should not print")
    out, err = capsys.readouterr()
    assert "[DEBUG]" not in out

    messaging_utils.set_debug(True)
    messaging_utils.debug("should print this")
    out, err = capsys.readouterr()
    assert "[DEBUG] should print this" in out

def test_info_warning_error_formatting(capsys):
    """
    info prints to stdout; warning/error print to stderr, with prefixes.
    """
    messaging_utils.info("my info", indent=1)
    out, err = capsys.readouterr()
    assert "[INFO] my info" in out

    messaging_utils.warning("my warn", indent=2)
    out, err = capsys.readouterr()
    assert "[WARNING] my warn" in err

    messaging_utils.error("my error", indent=0)
    out, err = capsys.readouterr()
    assert "[ERROR] my error" in err

def test_print_section_header_prints_title(capsys):
    """
    Section header function prints title with lines.
    """
    messaging_utils._print_section_header("TEST HEADER", icon="===")
    out, err = capsys.readouterr()
    assert "TEST HEADER" in out
    assert "===" in out

@pytest.mark.parametrize("func,args", [
    (messaging_utils.print_run_context, ("myscript.py", "myconfig.json", "20250705")),
    (messaging_utils.print_folder_tree_summary, (["tree1", "tree2"],)),
    (messaging_utils.print_asset_scan_summary, ([".py", ".md"], 5)),
    (messaging_utils.print_symbol_extraction, (10, 5, "rootdir")),
    (messaging_utils.print_entity_graph, (3, True)),
    (messaging_utils.print_exports, ({"timestamped": "f1.json"}, 3, "index.md")),
    (messaging_utils.print_governance_summary, (2, 1)),
    (messaging_utils.print_governance_summary, (0, 0)),
    (messaging_utils.print_journal_entries_loaded, (7,)),
    (messaging_utils.print_pipeline_complete, (5, "snap.zip")),
])
def test_reporting_helpers_dont_crash(func, args, capsys):
    """
    All reporting helper functions execute and print something.
    """
    func(*args)
    out, err = capsys.readouterr()
    assert out or err  # at least one should contain content

