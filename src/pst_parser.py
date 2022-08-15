"""
解析器核心类
"""

import sys


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
        pass


if __name__ == "__main__":
    pstp = PracticalSyntaxTreeParser('rust', 'main')
