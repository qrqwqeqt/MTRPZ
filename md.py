import re
import os

bold_regex = r"\*\*(?=\S)(.+?)(?<=\S)\*\*(?=\s|$)"
italic_regex = r"_(?=\S)(.+?)(?<=\S)_(?=\s|$)"
monospaced_regex = r"`(?=\S)(.+?)(?<=\S)`(?=\s|$)"
regexps = [bold_regex, italic_regex, monospaced_regex]

markers = ['**', '_', '`']

def set_paragraphs(text):
    paragraphs = list(filter(None, text.split('\n\n')))
    html_paragraphs = [f"<p>{par.strip()}</p>\n" for par in paragraphs]
    return ''.join(html_paragraphs)

def set_preformatted_parts(text):
    text = text.strip()
    return f"<pre>{text}</pre>\n"

def set_html_tags(text):
    text = re.sub(bold_regex, '<b>\\1</b>', text)
    text = re.sub(italic_regex, '<i>\\1</i>', text)
    return re.sub(monospaced_regex, '<tt>\\1</tt>', text)

def nested_markers_checker(text, regex, marker):
    parts = re.findall(regex, text)
    if parts:
        for part in parts:
            sliced_part = part[len(marker):-len(marker)]
            if (len(sliced_part) > 2 and 
                (sliced_part[:2] in markers or sliced_part[-2:] in markers)):
                raise ValueError('Nested markers are not allowed')
            if (len(sliced_part) > 1 and 
                (sliced_part[0] in markers or sliced_part[-1] in markers)):
                raise ValueError('Nested markers are not allowed')
            if (len(re.findall(r"\*\*", sliced_part)) > 1 or 
                len(re.findall(r"_", sliced_part)) > 1 or 
                len(re.findall(r"`", sliced_part)) > 1):
                raise ValueError('Nested markers are not allowed')

def markdown_to_html(filePath):
    if not filePath:
        raise ValueError('No file path provided')

    with open(filePath, 'r', encoding='utf-8') as file:
        md = file.read()

    parts = md.split('```')
    if len(parts) % 2 == 0:
        raise ValueError('No closing preformatted marker provided')

    for i in range(len(parts)):
        if i % 2 == 0:
            for regex, marker in zip(regexps, markers):
                nested_markers_checker(parts[i], regex, marker)
            parts[i] = set_html_tags(parts[i])
            parts[i] = set_paragraphs(parts[i])
        else:
            parts[i] = set_preformatted_parts(parts[i])

    return ''.join(parts)



html = markdown_to_html('md.md')
with open('output.html', 'w', encoding='utf-8') as f:
    f.write(html)
