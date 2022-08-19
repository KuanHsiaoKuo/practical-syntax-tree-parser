"""
解析器核心类
"""

import sys, os
import toml
import re


class PracticalSyntaxTreeParser:
    def __init__(self, language: str, parser_type: str, file_path: str):
        """
        :param language:
        :param parser_type:
        """
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
        self.file_path = file_path

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

    def parse(self):
        if self.parser_type == 'single':
            self.single_parse()
        elif self.parser_type == 'cargo':
            self.cargo_parse()

    def cargo_parse(self):
        if not self.file_path.endswith('.toml'):
            sys.exit('请传入Cargo.toml文件地址')
        cargo_content = toml.load(self.file_path)
        print(cargo_content)
        for config_name, config_detail in cargo_content.items():
            print(f"{config_name}:{self.explain[config_name]}")

    # 单文件解析
    def single_parse(self):
        # print(self.tomls)
        with open(self.file_path, 'r') as f:
            source_code = f.read()
        self.module_import(source_code)
        # self.parse_types(source_code)

    # 模块、引用解析
    def module_import(self, source_code):
        import_mods = self.parse_core(source_code, self.module)
        for import_mod in import_mods:
            print(import_mod)
            mod_name = import_mod.replace(';', '').split(' ')[-1]
            self.find_mod_file(self.file_path, mod_name)

    # 寻找同名mod文件路径
    def find_mod_file(self, file_path, mod_name):
        """
        1. lib/main中：同级目录 > mod同名文件
        2. 非lib/main中：同级目录 > 同名目录 > mod同名文件
        :param file_path:
        :param mod_name:
        :return:
        """
        start_file = file_path.split('/')[-1]
        if start_file in ('main.rs', 'lib.rs'):
            file_dir = file_path.replace(f"/{start_file}", '')
            # 查看是否有同名文件存在
            mod_file_path = f"{file_dir}/{mod_name}.rs"
            if os.path.exists(mod_file_path):
                print(f'{mod_name}存在同名模块文件:{mod_file_path}')
            else:
                print(f'{mod_name}存在未知情况')
        else:
            file_dir = file_path.replace(f"/{start_file}", '')
            # 查看是否有同名文件夹存在
            mod_dir_path = f"{file_dir}/{start_file.replace('.rs', '')}/{mod_name}.rs"
            if os.path.exists(mod_dir_path):
                print(f'{mod_name}存在同名模块文件夹:{mod_dir_path}')
            else:
                print(f'{mod_name}存在未知情况')

    # 类型解析
    def parse_types(self, source_code):
        self.parse_core(source_code, self.types)

    def parse_core(self, source_code, parse_regex: dict):
        parse_result = []
        for mod_name, reg_stat in parse_regex.items():
            # print(mod_name, reg_stat)
            explain_name = self.explain.get(mod_name)
            if explain_name:
                reg_result = re.findall(reg_stat, source_code)
                if reg_result:
                    print(f"\n## {explain_name}")
                    # 为了打印出正则表达式中的转义符号：\n \ \t
                    print(f"> {reg_stat}".encode("unicode_escape").decode('utf-8'))
                    for index, item in enumerate(reg_result):
                        print(f"{index + 1}. {item[0]}")
                        parse_result.append(item[0])
        return parse_result


if __name__ == "__main__":
    main_path = '../test_codes/network/src/lib.rs'
    mod_path = '../test_codes/network/src/service.rs'
    mod_define_file_path = '../test_codes/executive/src/lib.rs'
    cargo_file_path = '../test_codes/cargo_collection/substrate_main_cargo.toml'
    test_language, test_parse_type = 'rust', 'single'
    pstp = PracticalSyntaxTreeParser(test_language, test_parse_type, mod_path)
    pstp.parse()
    # pstp.parse(mod_define_file_path)
    # pstp.parse(cargo_file_path)
