import os
from typing import Optional

from utils import find_wiki_links

HEADER = '[//begin]: # "Autogenerated link references for markdown compatibility"'
FOOTER = '[//end]: # "Autogenerated link references"'


def generate_reference_links(file_contents: str, map_note_to_path: dict) -> str:
    ref_array = [
        HEADER,
    ]
    wiki_links = find_wiki_links(file_contents)
    for link in wiki_links:
        relative_note_path = map_note_to_path.get(link)
        if relative_note_path:
            ref_array.append(f'[{link}]: {relative_note_path} "{link}"')
    ref_array.append(FOOTER)
    return os.linesep.join(ref_array)


def get_file_contents_without_ref_block(file_contents: str) -> Optional[str]:
    header_line_no = None
    footer_line_no = None
    lines_in_file = file_contents.split(os.linesep)
    for i in range(len(lines_in_file)):
        line_contents = lines_in_file[i]
        if HEADER in line_contents:
            header_line_no = i
        if FOOTER in line_contents:
            footer_line_no = i

    contents_till_header = lines_in_file[:header_line_no]
    contents_after_footer = lines_in_file[(footer_line_no + 1):]
    final_file_contents = os.linesep.join(contents_till_header + contents_after_footer)
    return final_file_contents


def refresh_references_text_for_file(note_path: str, note_to_path_map: dict):
    # TODO: What is this monstrosity here? why open so many times! (https://gph.is/17I82kw)
    with open(note_path, "r") as readable_file:
        file_contents = readable_file.read()
        cleared_file_contents = get_file_contents_without_ref_block(file_contents)
        ref_text = generate_reference_links(file_contents, note_to_path_map)
        with open(note_path, "w") as writeable_file:
            writeable_file.write(cleared_file_contents.strip() + (os.linesep * 3) + ref_text)
