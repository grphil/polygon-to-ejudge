JUDGES_DIR = '/home/judges/'  # Path to judges folder

GVALUER_LOCATION = '/home/judges/001501/problems/gvaluer'  # Path to compiled gvaluer

CREATE_STATEMENTS = True  # Change it to False if you do not want to create statements for problems

IMPORT_ALL_SOLUTIONS = False  # Change it to True if you want to import all solutions


RUN_PANDOC = 'pandoc -f latex -t html --mathjax {} -o {}'

SCORING_TEXT = {
    'ru_RU': '<h3>Оценивание</h3>\n{}',
    'en_EN': '<h3>Scoring</h3>\n{}',
}

INTERACTION_TEXT = {
    'ru_RU': '<h3>Формат взаимодействия</h3>\n{}',
    'en_EN': '<h3>Interaction</h3>\n{}',
}

PROBLEM_CFG_START = "# -*- coding: utf-8 -*-\n\n[problem]"

GVALUER_GLOBAL_PART = '''global {
    stat_to_judges 1;
    stat_to_users 0;
}
'''

GVALUER_GROUP_BEGIN = 'group {} {{'
GVALUER_TESTS = '    tests {}-{};'
GVALUER_SCORE = '    {}score {};'
GVALUER_REQUIRES = '    requires {};'
GVALUER_SET_MARKED = '    sets_marked_if_passed {};'
GVALUER_OFFLINE = '    offline;'
GVALUER_GROUP_END = '}\n'


FEEDBACK_POLICY = {
    'none': 'hidden',
    'points': 'brief',
    'complete': 'full'
}
