#!/usr/bin/python3
"""Markdown to HTML Converter"""

import re
import hashlib
import sys
import os

def convert_markdown_to_html(input_md_file, output_html_file):
    # Check if the correct number of arguments is provided
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)

    # Check if the Markdown file exists
    if not os.path.exists(input_md_file):
        sys.stderr.write("Missing " + input_md_file + "\n")
        exit(1)

    with open(input_md_file) as md_file:
        with open(output_html_file, 'w') as html_file:
            in_unordered_list = False
            in_ordered_list = False
            in_paragraph = False

            for line in md_file:
                # Replace '**' with '<b>' and '</b>'
                line = line.replace('**', '<b>', 1)
                line = line.replace('**', '</b>', 1)

                # Replace '__' with '<em>' and '</em>'
                line = line.replace('__', '<em>', 1)
                line = line.replace('__', '</em>', 1)

                # Find all occurrences of '[[...]]' and replace them with the MD5 hash of the content inside the brackets
                md5_matches = re.findall(r'\[\[.+?\]\]', line)
                md5_contents = re.findall(r'\[\[(.+?)\]\]', line)
                if md5_matches:
                    line = line.replace(md5_matches[0], hashlib.md5(md5_contents[0].encode()).hexdigest())

                # Find all occurrences of '(())' and remove the letter 'C' or 'c' from the content inside the brackets
                delete_c_matches = re.findall(r'\(\(.+?\)\)', line)
                remove_c_contents = re.findall(r'\(\((.+?)\)\)', line)
                if delete_c_matches:
                    remove_c_contents = ''.join(c for c in remove_c_contents[0] if c not in 'Cc')
                    line = line.replace(delete_c_matches[0], remove_c_contents)

                line_length = len(line)
                line_without_headings = line.lstrip('#')
                heading_count = line_length - len(line_without_headings)
                line_without_unordered = line.lstrip('-')
                unordered_count = line_length - len(line_without_unordered)
                line_without_ordered = line.lstrip('*')
                ordered_count = line_length - len(line_without_ordered)

                # Convert heading lines to HTML heading tags
                if 1 <= heading_count <= 6:
                    line = '<h{}>'.format(heading_count) + line_without_headings.strip() + '</h{}>\n'.format(heading_count)

                # Convert unordered list lines to HTML list items
                if unordered_count:
                    if not in_unordered_list:
                        html_file.write('<ul>\n')
                        in_unordered_list = True
                    line = '<li>' + line_without_unordered.strip() + '</li>\n'
                if in_unordered_list and not unordered_count:
                    html_file.write('</ul>\n')
                    in_unordered_list = False

                # Convert ordered list lines to HTML list items
                if ordered_count:
                    if not in_ordered_list:
                        html_file.write('<ol>\n')
                        in_ordered_list = True
                    line = '<li>' + line_without_ordered.strip() + '</li>\n'
                if in_ordered_list and not ordered_count:
                    html_file.write('</ol>\n')
                    in_ordered_list = False

                # Convert regular lines to HTML paragraphs or line breaks
                if not (heading_count or in_unordered_list or in_ordered_list):
                    if not in_paragraph and line_length > 1:
                        html_file.write('<p>\n')
                        in_paragraph = True
                    elif line_length > 1:
                        html_file.write('<br/>\n')
                    elif in_paragraph:
                        html_file.write('</p>\n')
                        in_paragraph = False

                # Write the line to the output file
                if line_length > 1:
                    html_file.write(line)

            # Close any open HTML tags at the end of the file
            if in_ordered_list:
                html_file.write('</ol>\n')
            if in_paragraph:
                html_file.write('</p>\n')

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)

    convert_markdown_to_html(sys.argv[1], sys.argv[2])
    exit(0)
