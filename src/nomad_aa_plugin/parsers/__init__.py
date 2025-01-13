from nomad.config.models.plugins import ParserEntryPoint
from pydantic import Field


class MyParserOneEntryPoint(ParserEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from nomad_aa_plugin.parsers.parser import MyParserOne

        return MyParserOne(**self.dict())


parser_one_entry_point = MyParserOneEntryPoint(
    name='MyParserOne',
    description='My parser entry point configuration.',
    mainfile_name_re=r'.+\.csv',
    mainfile_mime_re="(?:text/plain|text/csv)",  # 'text/plain',  
    mainfile_contents_dict={
        '__has_all_keys': ['ValueOne', 'ValueOne2'],
        '__has_comment': '#',
    },
)

class MyParserTwoEntryPoint(ParserEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from nomad_aa_plugin.parsers.parser import MyParserTwo

        return MyParserTwo(**self.dict())


parser_two_entry_point = MyParserTwoEntryPoint(
    name='MyParserTwo',
    description='My parser entry point configuration.',
    mainfile_name_re=r'.+\.csv',
    mainfile_mime_re="(?:text/plain|text/csv)",  # 'text/plain',  
    mainfile_contents_dict={
        '__has_all_keys': ['ValueTwo', 'ValueTwo2'],
        '__has_comment': '#',
    },
)

class MyParserThreeEntryPoint(ParserEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from nomad_aa_plugin.parsers.parser import MyParserThree

        return MyParserThree(**self.dict())


parser_three_entry_point = MyParserThreeEntryPoint(
    name='MyParserThree',
    description='My parser entry point configuration.',
    mainfile_name_re=r'.+\.csv',
    mainfile_mime_re="(?:text/plain|text/csv)",  # 'text/plain',  
    mainfile_contents_dict={
        '__has_all_keys': ['ValueThree', 'ValueThree2'],
        '__has_comment': '#',
    },
)


class MyParserFourEntryPoint(ParserEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from nomad_aa_plugin.parsers.parser import MyParserFour

        return MyParserFour(**self.dict())


parser_four_entry_point = MyParserFourEntryPoint(
    name='MyParserFour',
    description='My parser entry point configuration.',
    mainfile_name_re=r'.+\.csv',
    mainfile_mime_re="(?:text/plain|text/csv)",  # 'text/plain',  
    mainfile_contents_dict={
        '__has_all_keys': ['ValueFour', 'ValueFour2'],
        '__has_comment': '#',
    },
)
