from collections import OrderedDict
import xml.etree.ElementTree as ET

from .config import GVALUER_GLOBAL_PART, GVALUER_GROUP_BEGIN, GVALUER_TESTS, GVALUER_SCORE, GVALUER_REQUIRES, \
    GVALUER_SET_MARKED, GVALUER_OFFLINE, GVALUER_GROUP_END, FEEDBACK_POLICY


def get_group_desc(group_id, l, r, score, requires, test_score, sets_marked):
    res = []
    res.append(GVALUER_GROUP_BEGIN.format(group_id))
    res.append(GVALUER_TESTS.format(l, r))
    res.append(GVALUER_SCORE.format(test_score, score))
    if len(requires) > 0:
        res.append(GVALUER_REQUIRES.format(', '.join(map(str, requires))))
    if sets_marked:
        res.append(GVALUER_SET_MARKED)
    else:
        res.append(GVALUER_OFFLINE)
    res.append(GVALUER_GROUP_END)
    return '\n'.join(res)


def generate_valuer(tree: ET.ElementTree) -> OrderedDict:
    test_points = []
    test_group = []

    for test in tree.find('judging').find('testset').find('tests'):
        test_data = test.attrib
        test_points.append(int(float(test_data['points'])))
        test_group.append(int(test_data['group']))

    tests = len(test_points)
    groups = max(test_group) + 1
    group_dependencies = [[] for i in range(groups)]
    each_test = [False] * groups
    feedback = [""] * groups

    for group in tree.find('judging').find('testset').find('groups'):
        group_id = int(group.attrib['name'])
        dependencies = group.find('dependencies')
        points_policy = group.attrib['points-policy']
        feedback_policy = group.attrib['feedback-policy']

        if dependencies is not None:
            for dep in dependencies:
                dep_id = int(dep.attrib['group'])
                group_dependencies[group_id].append(dep_id)
        if points_policy == "each-test":
            each_test[group_id] = True
        feedback[group_id] = FEEDBACK_POLICY[feedback_policy]

    min_test = [None] * groups
    max_test = [None] * groups
    group_score = [0] * groups

    for test_id in range(tests):
        if min_test[test_group[test_id]] is None:
            min_test[test_group[test_id]] = test_id + 1
        max_test[test_group[test_id]] = test_id + 1
        group_score[test_group[test_id]] = max(group_score[test_group[test_id]], test_points[test_id])

    valuer = open('valuer.cfg', 'w')
    valuer.write(GVALUER_GLOBAL_PART)
    full_score = 0
    full_user_score = 0
    open_tests = []
    final_open_tests = []
    test_score_list = []
    for group_id in range(groups):
        group_points = ''
        if each_test[group_id]:
            group_points = 'test_'
        valuer.write(get_group_desc(
            group_id,
            min_test[group_id],
            max_test[group_id],
            group_score[group_id],
            group_dependencies[group_id],
            group_points,
            feedback[group_id] != "hidden",
        ))

        open_tests.append('{}-{}:{}'.format(
            min_test[group_id],
            max_test[group_id],
            feedback[group_id],
        ))

        final_open_tests.append('{}-{}:{}'.format(
            min_test[group_id],
            max_test[group_id],
            "full",
        ))

        full_score += group_score[group_id]
        if feedback[group_id] != "hidden":
            full_user_score += group_score[group_id]

        group_score_list = []
        if each_test[group_id]:
            for i in range(min_test[group_id], max_test[group_id] + 1):
                group_score_list.append(str(group_score[group_id]))
        else:
            for i in range(min_test[group_id], max_test[group_id]):
                group_score_list.append('0')
            group_score_list.append(str(group_score[group_id]))
        test_score_list.append(' '.join(group_score_list))

    valuer.close()

    config = OrderedDict()
    config['full_score'] = full_score
    config['full_user_score'] = full_user_score
    config['open_tests'] = ', '.join(open_tests)
    config['final_open_tests'] = ', '.join(final_open_tests)
    config['test_score_list'] = '  '.join(test_score_list)
    config['valuer_cmd'] = "../gvaluer"
    config['interactive_valuer'] = True
    config['valuer_sets_marked'] = True
    config['olympiad_mode'] = True
    config['run_penalty'] = 0
    return config
