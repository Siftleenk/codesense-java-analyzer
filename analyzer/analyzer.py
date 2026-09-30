
import re


def count_classes(code):
    """Count Java class declarations."""
    pattern = r"\bclass\s+\w+"
    return len(re.findall(pattern, code))


def count_methods(code):
    """
    Count basic Java method declarations.

    This looks for a method name followed by parentheses
    and an opening curly brace.
    """

    pattern = r"\b(?:public|private|protected|static|\s)+[\w<>\[\]]+\s+\w+\s*\([^;{}]*\)\s*\{"

    matches = re.findall(pattern, code)

    return len(matches)


def analyze_java_code(code):
    """Analyze basic Java source-code metrics."""

    lines = code.splitlines()

    total_lines = len(lines)

    non_empty_lines = [
        line for line in lines
        if line.strip()
    ]

    classes = count_classes(code)
    methods = count_methods(code)

    return {
        "total_lines": total_lines,
        "non_empty_lines": len(non_empty_lines),
        "classes": classes,
        "methods": methods
    }


if __name__ == "__main__":

    sample_code = """
public class Student {

    public void display() {
        System.out.println("Hello");
    }
}
"""

    result = analyze_java_code(sample_code)

    print("CODE SENSE ANALYSIS")
    print("-------------------")
    print("Total Lines:", result["total_lines"])
    print("Non-empty Lines:", result["non_empty_lines"])
    print("Classes:", result["classes"])
    print("Methods:", result["methods"])
