
import re


def count_classes(code):
    """Count Java class declarations."""

    pattern = r"\bclass\s+\w+"

    return len(re.findall(pattern, code))


def find_methods(code):
    """
    Find basic Java methods and calculate their line counts.
    """

    lines = code.splitlines()

    methods = []

    inside_method = False
    current_method = None
    method_start = 0
    brace_count = 0

    for index, line in enumerate(lines, start=1):

        stripped = line.strip()

        # Detect a basic Java method declaration
        method_pattern = (
            r"(public|private|protected|static|\s)+"
            r"[\w<>\[\]]+\s+\w+\s*\([^;{}]*\)\s*\{"
        )

        if not inside_method and re.search(method_pattern, stripped):

            inside_method = True
            current_method = stripped
            method_start = index
            brace_count = stripped.count("{") - stripped.count("}")

            continue

        if inside_method:

            brace_count += line.count("{")
            brace_count -= line.count("}")

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


def analyze_java_code(code):

    lines = code.splitlines()

    total_lines = len(lines)

    non_empty_lines = [
        line for line in lines
        if line.strip()
    ]

    classes = count_classes(code)

    methods = find_methods(code)

    long_methods = detect_long_methods(methods)

    return {
        "total_lines": total_lines,
        "non_empty_lines": len(non_empty_lines),
        "classes": classes,
        "methods": methods,
        "issues": long_methods
    }


if __name__ == "__main__":

    sample_code = """
public class Student {

    public void processStudent() {

        int a = 1;
        int b = 2;
        int c = 3;
        int d = 4;
        int e = 5;
        int f = 6;
        int g = 7;
        int h = 8;
        int i = 9;
        int j = 10;
        int k = 11;
        int l = 12;
        int m = 13;
        int n = 14;
        int o = 15;
        int p = 16;
        int q = 17;
        int r = 18;
        int s = 19;
        int t = 20;

    }

}
"""

    result = analyze_java_code(sample_code)

    print("CODE SENSE ANALYSIS")
    print("-------------------")

    print("Total Lines:", result["total_lines"])
    print("Non-empty Lines:", result["non_empty_lines"])
    print("Classes:", result["classes"])
    print("Methods:", len(result["methods"]))

    print("\nISSUES")

    if not result["issues"]:

        print("No code smells detected.")

    else:

        for issue in result["issues"]:

            print("Type:", issue["type"])
            print("Severity:", issue["severity"])
            print("Lines:", issue["lines"])
            print("Message:", issue["message"])
            print("Suggestion:", issue["suggestion"])

