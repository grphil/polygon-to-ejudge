from collections import OrderedDict
import os

from .config import JUDGES_DIR


def get_ejudge_contest_dir(contest_id: int) -> str:
    contest_id = "{:06d}".format(int(contest_id))
    contest_dir = os.path.join(JUDGES_DIR, contest_id)
    return contest_dir


class UnquotedStr:
    def __init__(self, val):
        self.val = val


class Config:
    def __init__(self, contest_id: int):
        self.common = OrderedDict()
        self.languages = []
        self.problems = []
        self.testers = []
        self.end_comments = []
        self.contest_id = contest_id

        contest_dir = get_ejudge_contest_dir(contest_id)
        self.serve_cfg_path = os.path.join(contest_dir, "conf", "serve.cfg")

        serve_cfg = open(self.serve_cfg_path, "r")
        section_name = 'global'
        section_configs = OrderedDict()
        comments = []

        for line in serve_cfg.readlines():
            line = line.strip()
            if line.startswith('#'):
                comments.append(line)
                continue

            if len(line) == 0:
                continue

            if len(comments) > 0:
                for comment in comments:
                    section_configs[comment] = True
                comments = []

            if line.startswith('[') and line.endswith(']'):
                self.add_config(section_name, section_configs)
                section_configs.clear()
                section_name = line[1:-1]
                continue

            if '=' in line:
                key = line[:line.find('=')].strip()
                value = line[line.find('=') + 1:].strip()
                if len(value) > 1 and value[0] == '"' and value[-1] == '"':
                    value = value[1:-1]
                else:
                    try:
                        value = int(value)
                    except:
                        value = UnquotedStr(value)
                section_configs[key] = value
            else:
                section_configs[line] = True
        if section_name:
            self.add_config(section_name, section_configs)

        if len(comments) > 0:
            self.end_comments = comments.copy()

        serve_cfg.close()

    def add_config(
            self,
            section_name: str,
            section_configs: OrderedDict,
    ) -> None:
        if section_name == 'global':
            self.common = section_configs.copy()
        elif section_name == 'problem':
            self.problems.append(section_configs.copy())
        elif section_name == 'language':
            self.languages.append(section_configs.copy())
        elif section_name == 'tester':
            self.testers.append(section_configs.copy())
        else:
            raise Exception('unknown config section: {}'.format(section_name))

    @staticmethod
    def print_prepare(key: str, value) -> str:
        if isinstance(value, bool):
            if value:
                return key
            else:
                return '{} = 0'.format(key)
        if isinstance(value, str):
            return '{} = "{}"'.format(key, value)
        if isinstance(value, int):
            return '{} = {}'.format(key, value)
        if isinstance(value, UnquotedStr):
            return '{} = {}'.format(key, value.val)
        raise Exception("Unknown value type")

    @staticmethod
    def print_config(configs: OrderedDict, fout, beginning="") -> None:
        for key, value in configs.items():
            print(beginning, Config.print_prepare(key, value), file=fout, sep='')
        print(file=fout)

    def write(self):
        def get_id(configs: OrderedDict) -> int:
            if 'id' in configs:
                return configs['id']
            else:
                return -1

        fout = open(self.serve_cfg_path, 'w')
        self.print_config(self.common, fout)

        self.languages.sort(key=get_id)
        self.problems.sort(key=get_id)

        for language in self.languages:
            print('[language]', file=fout)
            self.print_config(language, fout)

        for problem in self.problems:
            print('[problem]', file=fout)
            self.print_config(problem, fout)

        for tester in self.testers:
            print('[tester]', file=fout)
            self.print_config(tester, fout)

        for line in self.end_comments:
            print(line, file=fout)
        fout.close()
