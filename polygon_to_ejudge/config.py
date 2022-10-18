JUDGES_DIR = '/home/judges/'  # Path to judges folder

GVALUER_LOCATION = '/home/judges/001501/problems/gvaluer'  # Path to compiled gvaluer

EJUDGE_URL = 'http://ejudge.algocode.ru/'

CREATE_STATEMENTS = True  # Change it to False if you do not want to create statements for problems

IMPORT_ALL_SOLUTIONS = False  # Change it to True if you want to import all solutions

TEXTAREA_INPUT = True

# TODO: allow changing above options from script

PYTHON_LANG_IDS = [23, 64] # python3 and pypy3
CPP_LANG_IDS = [3, 52] # g++ and clang
SOLUTION_FOLDER_NAMES = ['solutions', 'solutions1']

RUN_PANDOC = 'pandoc -f latex -t html --mathjax {} -o {}'

CONVERT_EPS = 'gs -dSAFER -dBATCH -dNOPAUSE -dEPSCrop -r600 -sDEVICE=pngalpha -sOutputFile={} {}'
IMG_STYLE = 'width: auto; max-width: max(50%, 400px); height: auto; max-height: 100%;'
IMG_SRC_PREFIX = '${getfile}='

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
    'icpc': 'brief',
    'complete': 'full',
}

INFORMATICS = '''<div class="problem-statement">
{}
</div>
'''

INFORMATICS_LEGEND = '''<div class="legend">
  {}
</div>
'''

INFORMATICS_INPUT = '''<div class="input-specification">
  <div class="section-title">
    Входные данные
  </div>

  {}
</div>
'''

INFORMATICS_OUTPUT = '''<div class="output-specification">
  <div class="section-title">
     Входные данные
  </div>

  {}
</div>
'''

INFORMATICS_NOTES = '''<div class="note">
  <div class="section-title">
    Примечание
  </div>

  {}
</div>
'''

INFORMATICS_SCORING = '''<div class="scoring">
  <div class="section-title">
    Система оценки
  </div>

  {}
</div>
'''

INFORMATICS_INTERACTION = '''<div class="interaction">
  <div class="section-title">
    Протокол взаимодействия</div>
  </div>
  {}
</div>
'''
