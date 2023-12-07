#!/usr/bin/python3
""" Write a script markdown2html.py that takes an argument 2 strings:
First argument is the name of the Markdown file
Second argument is the output file name """

import re
import hashlib
import sys
import os

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)
    
    # Check if the Markdown file exists
    if not os.path.exists(sys.argv[1]):
        sys.stderr.write("Missing " + sys.argv[1] + "\n")
        exit(1)

    with open(sys.argv[1]) as r:
        with open(sys.argv[2], 'w') as w:
            change_status = False
            ordered_status = False
            paragraph = False
            for line in r:
                # Replace '**' with '<b>' and '</b>'
                line = line.replace('**', '<b>', 1)
                line = line.replace('**', '</b>', 1)
                
                # Replace '__' with '<em>' and '</em>'
                line = line.replace('__', '<em>', 1)
                line = line.replace('__', '</em>', 1)

                # Find all occurrences of '[[...]]' and replace them with the MD5 hash of the content inside the brackets
                md5 = re.findall(r'\[\[.+?\]\]', line)
                md5_inside = re.findall(r'\[\[(.+?)\]\]', line)
                if md5:
                    line = line.replace(md5[0], hashlib.md5(md5_inside[0].encode()).hexdigest())

                # Find all occurrences of '(())' and remove the letter 'C' or 'c' from the content inside the brackets
                delete_c = re.findall(r'\(\(.+?\)\)', line)
                remove_c_inside = re.findall(r'\(\((.+?)\)\)', line)
                if delete_c:
                    remove_c_inside = ''.join(c for c in remove_c_inside[0] if c not in 'Cc')
                    line = line.replace(delete_c[0], remove_c_inside)
                
                length = len(line)
                headings = line.lstrip('#')
                heading_count = length - len(headings)
                unordered = line.lstrip('-')
                unordered_count = length - len(unordered)
                ordered = line.lstrip('*')
                ordered_count = length - len(ordered)

                # Convert heading lines to HTML heading tags
                if 1 <= heading_count <= 6:
                    line = '<h{}>'.format(heading_count) + headings.strip() + '</h{}>\n'.format(heading_count)

                # Convert unordered list lines to HTML list items
                if unordered_count:
                    if not change_status:
                        w.write('<ul>\n')
                        change_status = True
                    line = '<li>' + unordered.strip() + '</li>\n'
                if change_status and not unordered_count:
                    w.write('</ul>\n')
                    change_status = False

                # Convert ordered list lines to HTML list items
                if ordered_count:
                    if not ordered_status:
                        w.write('<ol>\n')
                        ordered_status = True
                    line = '<li>' + ordered.strip() + '</li>\n'
                if ordered_status and not ordered_count:
                    w.write('</ol>\n')
                    ordered_status = False

                # Convert regular lines to HTML paragraphs or line breaks
                if not (heading_count or change_status or ordered_status):
                    if not paragraph and length > 1:
                        w.write('<p>\n')
                        paragraph = True
                    elif length > 1:
                        w.write('<br/>\n')
                    elif paragraph:
                        w.write('</p>\n')
                        paragraph = False

                # Write the line to the output file
                if length > 1:
                    w.write(line)

            # Close any open HTML tags at the end of the file
            if ordered_status:
                w.write('</ol>\n')
            if paragraph:
                w.write('</p>\n')

    exit(0)