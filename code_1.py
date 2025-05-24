import re
import sys
import os


def extract_class_name(line):
    pattern = r"class\s+(\w+)"
    match = re.search(pattern, line)
    if match:
        return match.group(1)
    return None


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


def read_java_file(file_path):
    """
    Проходит по файлу по строкам и отслеживает в каком классе находится строка
    """
    with open(file_path, "r", encoding="utf-8") as file:
        current_class = None
        brakets = ""
        for line in file:
            extracted_class_name = extract_class_name(line)
            if extracted_class_name != None:
                current_class = extracted_class_name
            if current_class != None:
                if "{" in line:
                    brakets += "{"
                if "}" in line:
                    brakets = brakets[:-1]
                if len(brakets) == 0:
                    current_class = None
            print(current_class)


def main():
    if len(sys.argv) != 2 or sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print("Usage: python script.py <path_to_java_file_or_directory>")
        sys.exit(1)

    path = sys.argv[1]
    java_files = read_java_files(path)

    if not java_files:
        print("No Java files found.")
        sys.exit(1)

    read_java_file(java_files[0])


if __name__ == "__main__":
    main()
