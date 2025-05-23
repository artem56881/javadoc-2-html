import re
import sys

def extract_javadoc_comments(java_code):
    pattern = r'/\*\*(.*?)\*/'
    matches = re.findall(pattern, java_code, re.DOTALL)
    return matches

def parse_javadoc_comment(comment):
    comment = re.sub(r'\s*\*\s*', '', comment)
    comment = re.sub(r'^\s*', '', comment, flags=re.MULTILINE)
    return comment

def generate_html_documentation(javadoc_comments):
    html = """
    <html>
    <head>
        <title>Javadoc Documentation</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .class { margin-bottom: 20px; }
            .method { margin-bottom: 15px; }
            .tag { font-weight: bold; }
        </style>
    </head>
    <body>
    """

    for comment in javadoc_comments:
        if "class" in comment.lower():
            html += f"<div class='class'><h2>Class</h2><p>{comment}</p></div>\n"
        else:
            # Обработка тегов @param, @return, @throws
            comment = re.sub(r'@param\s+(\w+)\s+(.*)', r'<div class="tag">@param \1:</div> \2<br>', comment)
            comment = re.sub(r'@return\s+(.*)', r'<div class="tag">@return:</div> \1<br>', comment)
            comment = re.sub(r'@throws\s+(\w+)\s+(.*)', r'<div class="tag">@throws \1:</div> \2<br>', comment)
            comment = re.sub(r'@author\s+(.*)', r'<div class="tag">@author:</div> \1<br>', comment)
            comment = re.sub(r'@version\s+(.*)', r'<div class="tag">@version:</div> \1<br>', comment)

            html += f"<div class='method'><h3>Method</h3><p>{comment}</p></div>\n"

    html += "</body></html>"
    return html

def read_java_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def main():
    if len(sys.argv) != 2 or sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print("Usage: python script.py <path_to_java_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    java_code = read_java_file(file_path)

    javadoc_comments = extract_javadoc_comments(java_code)

    parsed_comments = [parse_javadoc_comment(comment) for comment in javadoc_comments]

    html_documentation = generate_html_documentation(parsed_comments)

    with open('javadoc_documentation.html', 'w', encoding='utf-8') as file:
        file.write(html_documentation)

if __name__ == "__main__":
    main()

 # type: ignore