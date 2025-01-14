import logging

from nomad.datamodel import EntryArchive

from nomad_aa_plugin.parsers.parser import MyParserOne


def test_parse_file():
    parser = MyParserOne()
    archive = EntryArchive()
    parser.parse('tests/data/test_one.csv', archive, logging.getLogger())

    assert archive.name == 'And'
