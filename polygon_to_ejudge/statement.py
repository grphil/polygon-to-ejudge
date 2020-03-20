import os
import xml.etree.ElementTree as ET

from .config import *


def latex_to_html(location: str, file_name: str) -> str:
    text = open(os.path.join(location, file_name), 'r').read()
    text = text.replace('\\t{', '\\texttt{').replace('<<', '«').replace('>>', '»')

    text_ouput_file = open(os.path.join(location, file_name), 'w')
    text_ouput_file.write(text)
    text_ouput_file.close()

    os.system(RUN_PANDOC.format(
        os.path.join(location, file_name),
        os.path.join(location, "out.html"),
    ))
    return open(os.path.join(location, "out.html")).read()


def import_statement(location: str, language: str):
    statement_files = os.listdir(location)
    statement_files.sort()

    tree = ET.Element('problem')
    statement = ET.SubElement(tree, 'statement', language=language)
    examples = ET.SubElement(tree, 'examples')
    current_example = None

    for statement_file in statement_files:
        if statement_file.startswith('example'):
            content = open(os.path.join(location, statement_file), 'r').read()
            if statement_file.endswith('.a'):
                ET.SubElement(current_example, 'output').text = content
            else:
                current_example = ET.SubElement(examples, 'example')
                ET.SubElement(current_example, 'input').text = content

    legend = ''
    informatics_statement = ''
    res = [tree, informatics_statement]
    if 'legend.tex' in statement_files:
        text = latex_to_html(location, 'legend.tex')
        legend += text
        informatics_statement += INFORMATICS_LEGEND.format(text)

    if 'input.tex' in statement_files:
        ET.SubElement(statement, 'input_format').text = '{}'
        text = latex_to_html(location, 'input.tex')
        res.append(text)
        informatics_statement += INFORMATICS_INPUT.format(text)

    if 'output.tex' in statement_files:
        ET.SubElement(statement, 'output_format').text = '{}'
        text = latex_to_html(location, 'output.tex')
        res.append(text)
        informatics_statement += INFORMATICS_OUTPUT.format(text)

    if 'interaction.tex' in statement_files:
        text = latex_to_html(location, 'interaction.tex')
        legend += INTERACTION_TEXT[language].format(text)
        informatics_statement += INFORMATICS_INTERACTION.format(text)

    if len(legend) > 0:
        res.append(legend)
        ET.SubElement(statement, 'description').text = '{}'

    notes = ''
    if 'notes.tex' in statement_files:
        text = latex_to_html(location, 'notes.tex')
        notes += text
        informatics_statement += INFORMATICS_NOTES.format(text)

    if 'scoring.tex' in statement_files:
        text = latex_to_html(location, 'scoring.tex')
        notes += SCORING_TEXT[language].format(text)
        informatics_statement += INFORMATICS_SCORING.format(text)
    if len(notes) > 0:
        res.append(notes)
        ET.SubElement(statement, 'notes').text = '{}'

    informatics_statement = INFORMATICS.format(informatics_statement)
    res[1] = informatics_statement
    # TODO: media
    return res


def process_statement_xml(statement):
    result = ''
    in_math = False
    for ch in statement:
        result += ch
        if result[-1] == '>' and not result.endswith('<input>') and not result.endswith('<output>'):
            result += '\n'
        if result.endswith('&lt;'):
            result = result[:-4]
            if in_math:
                result += '\\lt'
            else:
                result += '<'
        if result.endswith('&gt;'):
            result = result[:-4]
            if in_math:
                result += '\\gt'
            else:
                result += '>'
        if result.endswith('&amp;gt;'):
            result = result[:-len('&amp;gt;')]
            result += '\\gt'
        if result.endswith('&amp;lt;'):
            result = result[:-len('&amp;lt;')]
            result += '\\lt'
        if result.endswith('\\textgreater'):
            result = result[:-len('\\textgreater')]
            result += '\\gt'
        if result.endswith('\\textsmaller'):
            result = result[:-len('\\textsmaller')]
            result += '\\lt'
        if result.endswith('\\(') or result.endswith('\\['):
            in_math = True
        if result.endswith('\\)') or result.endswith('\\]'):
            in_math = False
    return result
