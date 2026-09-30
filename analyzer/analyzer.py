
import re
import json


def count_classes(code):
    """Count Java class declarations."""

    pattern = r"\bclass\s+\w+"

    return len(re.findall(pattern, code))


def find_methods(code):
    """
    Find basic Java methods and calculate their line counts.

    Handles both:
    1. Multi-line methods
    2. Single-line methods
    """

    lines = code.splitlines()

    methods = []

    inside_method = False
    current_method = None
    method_start = 0
    brace_count = 0

    method_pattern = re.compile(
        r"\b(?:public|private|protected|static|final|"
        r"synchronized|abstract|native|default)?\s*"
        r"(?:<[^>]+>\s*)?"
        r"[\w<>\[\], ?]+\s+"
        r"\w+\s*"
        r"\([^;{}]*\)\s*\{"
    )

    for index, line in enumerate(lines, start=1):

        stripped = line.strip()

        if not stripped:
            continue

        # Look for a method declaration
        match = method_pattern.search(stripped)

        if not inside_method and match:

            inside_method = True
            current_method = match.group(0).strip()
            method_start = index

            # IMPORTANT:
            # Count ALL braces on the same line.
            brace_count = (
                line.count("{")
                - line.count("}")
            )

            # Handles one-line methods such as:
            #
            # public void display() {
            #     System.out.println("Hello");
            # }
            #
            # and:
            #
            # public void display() {
            #     System.out.println("Hello");
            # }

            if brace_count == 0:

                method_length = index - method_start + 1

                methods.append({
                    "name": current_method,
                    "start_line": method_start,
                    "end_line": index,
                    "lines": method_length
                })

                inside_method = False
                current_method = None
                brace_count = 0

            continue

        if inside_method:

            brace_count += line.count("{")
            brace_count -= line.count("}")

            if brace_count <= 0:

                method_length = index - method_start + 1

                methods.append({
                    "name": current_method,
                    "start_line": method_start,
                    "end_line": index,
                    "lines": method_length
                })

                inside_method = False
                current_method = None
                brace_count = 0

    return methods


def detect_long_methods(methods, threshold=20):
    """
    Detect methods whose length exceeds the threshold.
    """

    issues = []

    for method in methods:

        if method["lines"] >= threshold:

            issues.append({
                "type": "Long Method",
                "severity": "Medium",
                "lines": method["lines"],
                "message": (
                    f"Method starting at line "
                    f"{method['start_line']} contains "
                    f"{method['lines']} lines."
                ),
                "suggestion": (
                    "Consider breaking this method "
                    "into smaller, focused methods."
                )
            })

    return issues


def detect_deep_nesting(code, threshold=3):
    """
    Detect excessive nesting of code blocks.
    """

    lines = code.splitlines()

    current_depth = 0
    maximum_depth = 0

    for line in lines:

        stripped = line.strip()

        if not stripped or stripped.startswith("//"):
            continue

        opening_braces = line.count("{")
        closing_braces = line.count("}")

        current_depth += opening_braces

        maximum_depth = max(
            maximum_depth,
            current_depth
        )

        current_depth -= closing_braces

    issues = []

    if maximum_depth > threshold:

        issues.append({
            "type": "Deep Nesting",
            "severity": "Medium",
            "depth": maximum_depth,
            "message": (
                f"Maximum nesting depth is "
                f"{maximum_depth}."
            ),
            "suggestion": (
                "Consider reducing nested control structures "
                "or extracting logic into separate methods."
            )
        })

    return issues


def calculate_quality_score(issues):
    """
    Calculate a code-quality score from 0 to 100.
    """

    score = 100

    penalties = {
        "Long Method": 10,
        "Deep Nesting": 10
    }

    for issue in issues:

        issue_type = issue["type"]

        if issue_type in penalties:
            score -= penalties[issue_type]

    return max(score, 0)


def analyze_java_code(code):
    """
    Perform complete CodeSense analysis.
    """

    lines = code.splitlines()

    total_lines = len(lines)

    non_empty_lines = [
        line
        for line in lines
        if line.strip()
    ]

    classes = count_classes(code)

    methods = find_methods(code)

    long_methods = detect_long_methods(methods)

    deep_nesting = detect_deep_nesting(code)

    issues = long_methods + deep_nesting

    quality_score = calculate_quality_score(issues)

    return {
        "total_lines": total_lines,
        "non_empty_lines": len(non_empty_lines),
        "classes": classes,
        "methods": methods,
        "issues": issues,
        "quality_score": quality_score
    }


def generate_report(code):
    """
    Generate a structured CodeSense JSON-compatible report.
    """

    result = analyze_java_code(code)

    report = {
        "quality_score": result["quality_score"],

        "metrics": {
            "total_lines": result["total_lines"],
            "non_empty_lines": result["non_empty_lines"],
            "classes": result["classes"],
            "methods": len(result["methods"])
        },

        "issues": result["issues"]
    }

    return report


if __name__ == "__main__":

    sample_code = """
public class Student {

    public void processStudent() {

        if (condition1) {

            if (condition2) {

                for (int i = 0; i < 10; i++) {

                    if (condition3) {

                        System.out.println("Deep nesting");

                    }
                }
            }
        }
    }
}
"""

    result = analyze_java_code(sample_code)

    print("CODE SENSE ANALYSIS")
    print("-------------------")

    print(
        "Total Lines:",
        result["total_lines"]
    )

    print(
        "Non-empty Lines:",
        result["non_empty_lines"]
    )

    print(
        "Classes:",
        result["classes"]
    )

    print(
        "Methods:",
        len(result["methods"])
    )

    print(
        "Quality Score:",
        result["quality_score"],
        "/ 100"
    )

    print("\nISSUES")

    if not result["issues"]:

        print("No code smells detected.")

    else:

        for issue in result["issues"]:

            print("\nType:", issue["type"])

            print(
                "Severity:",
                issue["severity"]
            )

            if "lines" in issue:
                print(
                    "Lines:",
                    issue["lines"]
                )

            if "depth" in issue:
                print(
                    "Depth:",
                    issue["depth"]
                )

            print(
                "Message:",
                issue["message"]
            )

            print(
                "Suggestion:",
                issue["suggestion"]
            )

    print("\nJSON REPORT")

    print(
        json.dumps(
            generate_report(sample_code),
            indent=4
        )
    )

