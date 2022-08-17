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
        self.types = self.tomls['types']

    @property
    def supported_languanges(self):
        return ['rust']

    @property
    def parser_types(self):
        """
        主要支持三种解析方式：单文件、crate和项目（模块）
        :return:
        """
        return ['cargo', 'single', 'module', 'project']

    def parse(self, file_path: str):
        if self.parser_type == 'single':
            self.single_parse(file_path)
        elif self.parser_type == 'cargo':
            self.cargo_parse(file_path)

    def cargo_parse(self, file_path: str):
        if not file_path.endswith('.toml'):
            sys.exit('请传入Cargo.toml文件地址')
        cargo_content = toml.load(file_path)
        print(cargo_content)
        for config_name, config_detail in cargo_content.items():
            print(f"{config_name}:{self.explain[config_name]}")

    # 单文件解析
    def single_parse(self, file_path: str):
        # print(self.tomls)
        with open(file_path, 'r') as f:
            source_code = f.read()
        self.module_import(source_code)
        self.parse_types(source_code)

    # 模块、引用解析
    def module_import(self, source_code):
        self.parse_core(source_code, self.module)

    # 类型解析
    def parse_types(self, source_code):
        self.parse_core(source_code, self.types)

    def parse_core(self, source_code, parse_regex: dict):
        for mod_name, reg_stat in parse_regex.items():
            # print(mod_name, reg_stat)
            explain_name = self.explain.get(mod_name)
            if explain_name:
                result = re.findall(reg_stat, source_code)
                if result:
                    print(f"\n## {explain_name}")
                    # 为了打印出正则表达式中的转义符号：\n \ \t
                    print(reg_stat.encode("unicode_escape").decode('utf-8'))
                    for index, item in enumerate(result):
                        print(f"\t{index + 1}. {item[0]}")


if __name__ == "__main__":
    main_path = '../test_codes/network/src/lib.rs'
    mod_define_file_path = '../test_codes/executive/src/lib.rs'
    cargo_file_path = '../test_codes/cargo_collection/substrate_main_cargo.toml'

    pstp = PracticalSyntaxTreeParser('rust', 'cargo')
    # pstp.main_parse(main_path)
    # pstp.parse(mod_define_file_path)
    pstp.parse(cargo_file_path)
