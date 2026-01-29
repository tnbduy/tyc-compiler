"""
Lexer test cases for TyC compiler
TODO: Implement 100 test cases for lexer
"""

import pytest
from tests.utils import Tokenizer


def test_lexer_placeholder():
    """Placeholder test - replace with actual test cases"""
    source = "// This is a placeholder test\r\nid"
    tokenizer = Tokenizer(source)
    # TODO: Add actual test assertions
    assert True

# Convert Tokenizer.get_tokens_as_string() into a list of token names.
def _token_names(source: str) -> list[str]:
    s = Tokenizer(source).get_tokens_as_string()
    parts = s.split(",") if s else []
    names = parts[0::2] 
    return names

# Remove trailing EOF token from list of token names.
def _token_names_no_eof(source: str) -> list[str]:
    names = _token_names(source)
    if names and names[-1] == "EOF":
        return names[:-1]
    return names

## Test Cases for Comments ##

# LX-001: Valid block comment
def test_LX_001_valid_block_comment():
    source = "/* Valid block comment */ id"
    assert _token_names_no_eof(source) == ["ID"]


# LX-002: Block comment spans multiple lines
def test_LX_002_block_comment_spans_multiple_lines():
    source = "/* line1\nline2 */ id"
    assert _token_names_no_eof(source) == ["ID"]


# LX-003: Block comment with special characters
def test_LX_003_block_comment_with_special_characters():
    source = ("/* !@#$%^&*()_+-=[]{}|;:'\"<>/?`~ \\b \\t \\f \\\\ /* // still comment \n*/id")
    assert _token_names_no_eof(source) == ["ID"]

# LX-004: Unterminated block comment (reaches EOF)
def test_LX_004_unterminated_block_comment_reaches_eof():
    source = "/* Unclosed block comment"
    assert "UNCLOSE_BLOCK_COMMENT" in _token_names_no_eof(source)


# LX-005: Valid line comment (ends at newline)
def test_LX_005_valid_line_comment_ends_at_newline():
    source = "// Valid line comment\nid"
    assert _token_names_no_eof(source) == ["ID"]


# LX-006: /* */ has no meaning inside line comment
def test_LX_006_block_markers_have_no_meaning_inside_line_comment():
    source = "// this /* is not a block */\nid"
    assert _token_names_no_eof(source) == ["ID"]

# LX-007: Comments are not nested
def test_LX_007_comments_not_nested_block_comment_stops_at_first_end():
    source = "/* outer */ inner */ id"
    assert _token_names_no_eof(source) == ["ID", "MUL", "DIV", "ID"]


# LX-008: Line comment at EOF
def test_LX_008_line_comment_at_eof():
    source = "// Line comment encounter EOF <EOF>"
    assert _token_names_no_eof(source) == []
    

# LX-009: Nested line comments
def test_LX_009_nested_line_comments():
    source = "// Outer comment // Inner comment\r\nid"
    assert _token_names_no_eof(source) == ["ID"]    
    

# LX-010: Line comment with special characters
def test_LX_010_line_comment_with_special_characters():
    source = "// !@#$%^&*()_+-=[]{}|;:'\"<>/?`~ \\b \\t \\f \\\\ /* not a block */ // still comment \nid"
    assert _token_names_no_eof(source) == ["ID"]