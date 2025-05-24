from pprint import pprint
import re
import sys
import os


def extract_class_name(line):
    match = re.search(r"\bclass\s+(\w+)", line)
    return match.group(1) if match else None


def extract_method_signature(line):
    pattern = (
        r"(public|protected|private)?\s*(sta"
        r"tic\s+)?([\w<>\[\]]+)\s+(\w+)\s*\(([^)]*)\)\s*\{?"
    )
    match = re.search(pattern, line)
    if match:
        signature = {
            "return_type": match.group(3),
            "method_name": match.group(4),
            "parameters": match.group(5).strip(),
        }
        return signature
    return None


def parse_javadoc_block(javadoc_lines):
    doc = {"description": "", "author": "", "params": [], "see": ""}
    description_lines = []
    for line in javadoc_lines:
        line = line.strip().lstrip("*").strip()
        if line.startswith("@param"):
            parts = line.split(None, 2)
            if len(parts) == 3:
                doc["params"].append((parts[1], parts[2]))
        elif line.startswith("@author"):
            doc["author"] = line.split(None, 1)[1]
        elif line.startswith("@see"):
            doc["see"] = line.split(None, 1)[1]
        elif line.startswith("@return"):
            doc["return"] = line.split(None, 1)[1]
        elif not line.startswith("@"):
            description_lines.append(line)
    doc["description"] = " ".join(description_lines)
    return doc


def parse_java_file(file_path):
    documentation = {}
    with open(file_path, "r", encoding="utf-8") as file:
        current_class = None
        bracket_stack = []
        javadoc_buffer = []
        in_javadoc = False

        for line in file:
            stripped = line.strip()

            # Начало JavaDoc
            if stripped.startswith("/**"):
                in_javadoc = True
                javadoc_buffer = []
                continue
            elif in_javadoc:
                if "*/" in stripped:
                    in_javadoc = False
                    continue
                javadoc_buffer.append(stripped)
                continue

            # Класс
            class_name = extract_class_name(stripped)
            if class_name:
                current_class = class_name
                documentation[current_class] = []

            # Метод
            method = extract_method_signature(stripped)
            if method and current_class:
                javadoc = (
                    parse_javadoc_block(javadoc_buffer)
                    if javadoc_buffer
                    else {}
                )
                method.update(javadoc)
                documentation[current_class].append(method)
                javadoc_buffer = []

            # отслеживание текущего класса по скобкам
            if current_class:
                bracket_stack += ["{"] * stripped.count("{")
                bracket_stack = bracket_stack[
                    : len(bracket_stack) - stripped.count("}")
                ]
                if not bracket_stack:
                    current_class = None

    return documentation


def generate_html_documentation(all_docs_by_file):
    html = [
        "<html><head><meta charset='utf-8'><tit"
        "le>JavaDoc</title></head><body>"
    ]
    html.append("<h1>JavaDoc</h1>")

    for filename, classes in all_docs_by_file.items():
        html.append(f"<hr><h2>File: {filename}</h2>")

        for class_name, methods in classes.items():
            html.append(f"<div style='margin-left: 20px;'>")
            html.append(f"<h3>Class: {class_name}</h3>")

            for method in methods:
                html.append(f"<div style='margin-left: 40px;'>")
                html.append(
                    f"<h4>{method['method_name']}"
                    f"({method.get('parameters', '')})</h4>"
                )
                html.append(f"<div style='margin-left: 60px;'>")

                if method.get("description"):
                    html.append(
                        f"<p><b>Descrip"
                        f"tion:</b> {method['description']}</p>"
                    )
                if method.get("author"):
                    html.append(f"<p><b>Auth"
                                f"or:</b> {method['author']}</p>")
                if method.get("params"):
                    html.append("<p><b>Parameters:</b><ul>")
                    for name, desc in method["params"]:
                        html.append(f"<li><b>{name}</b>: {desc}</li>")
                    html.append("</ul></p>")
                if method.get("see"):
                    html.append(f"<p><b>See also:</b> {method['see']}</p>")
                if method.get("return"):
                    html.append(f"<p><b>Return"
                                f"s:</b> {method['return']}</p>")
                # html.append("aaaaaaaaaaaaaaaaaaaaa")
                html.append("</div>")
                html.append("</div>")

            html.append("</div>")

    html.append("</body></html>")
    return "\n".join(html)


def read_java_files(path):
    java_files = []
    if os.path.isfile(path) and path.endswith(".java"):
        java_files.append(path)
    elif os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".java"):
                    java_files.append(os.path.join(root, file))
    return java_files


def main():
    if len(sys.argv) != 2 or sys.argv[1] in ["-h", "--help"]:
        print(
            "Использование: python code_1.py <путь_к_ja"
            "va_файлу_или_директории>"
        )
        sys.exit(1)

    path = sys.argv[1]
    java_files = read_java_files(path)

    if not java_files:
        print(".java файлы не найдены в указаной директории")
        sys.exit(1)

    all_docs_by_file = {}

    for java_file in java_files:
        doc = parse_java_file(java_file)
        all_docs_by_file[java_file] = doc

    html = generate_html_documentation(all_docs_by_file)
    pprint(all_docs_by_file)
    with open("all_java_docs.html", "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    main()
