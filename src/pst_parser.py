"""
解析器核心类
"""

import sys
import toml
import re
import json


class PracticalSyntaxTreeParser:
    def __init__(self, language: str, parser_type: str):
        if language not in self.supported_languanges:
            sys.exit(f"暂不支持{language}, 支持语言：{self.supported_languanges}")
        else:
            self.language = language
        if parser_type not in self.parser_types:
            sys.exit(f"只支持{self.parser_types}")
        else:
            self.parser_type = parser_type
        tomls_config = {
            'rust': 'rules/rust_parse_rules.toml'
        }
        self.tomls = toml.load(tomls_config.get(self.language))
        self.explain = self.tomls['explain']
        self.module = self.tomls['module']

    @property
    def supported_languanges(self):
        return ['rust']

    @property
    def parser_types(self):
        """
        主要支持三种解析方式：单文件、crate和项目（模块）
        :return:
        """
        return ['main', 'module', 'project']

    def parse(self, file_path: str):
        if self.parser_type == 'main':
            self.main_parse()

    # 单文件解析
    def main_parse(self, file_path: str):
        # print(self.tomls)
        with open(file_path, 'r') as f:
            source_code = f.read()
        for mod_name, reg_stat in self.module.items():
            # print(mod_name, reg_stat)
            explain_name = self.explain.get(mod_name)
            if explain_name:
                result = re.findall(reg_stat, source_code)
                if result:
                    print(f"\n## {explain_name}")
                    # 为了打印出正则表达式中的转义符号：\n \ \t
                    print(reg_stat.encode("unicode_escape").decode('utf-8'))
                    for index, item in enumerate(result):
                        print(f"\t{index+1}. {item[0]}")



if __name__ == "__main__":
    main_path = '../test_codes/network/src/lib.rs'
    mod_define_file_path = '../test_codes/executive/src/lib.rs'
    pstp = PracticalSyntaxTreeParser('rust', 'main')
    # pstp.main_parse(main_path)
    pstp.main_parse(mod_define_file_path)
