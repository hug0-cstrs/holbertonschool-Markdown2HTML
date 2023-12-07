#!/usr/bin/env python3
"""
Write a script markdown2html.py that takes an argument 2 strings:
First argument is the name of the Markdown file
Second argument is the output file name
"""
import sys
import os
import markdown

def convert_markdown_to_html(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as md_file:
            md_content = md_file.read()
            html_content = markdown.markdown(md_content)
        
        with open(output_file, 'w', encoding='utf-8') as html_file:
            html_file.write(html_content)
        
        return 0
    except FileNotFoundError:
        print(f"Missing {input_file}", file=sys.stderr)
        return 1

def main():
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    exit_code = convert_markdown_to_html(input_file, output_file)
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
