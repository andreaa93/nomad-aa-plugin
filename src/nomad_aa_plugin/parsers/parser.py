from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

from nomad.config import config
from nomad.datamodel.metainfo.workflow import Workflow
from nomad.parsing.parser import MatchingParser


from nomad.datamodel.datamodel import EntryArchive
from nomad.parsing import MatchingParser


from pdi_nomad_plugin.utils import (
    create_archive,
)

from nomad_aa_plugin.schema_packages.schema_package import MyClassTwo, MyClassOne

class MyParser(MatchingParser):
    def parse(
        self,
        mainfile: str, 
        archive: EntryArchive,
        logger,
    ) -> None:
        
        my_name = "And"
        child_archive = EntryArchive()
        filetype = 'yaml'

        example_filename = f'{my_name}.archive.{filetype}'

        child_archive.data = MyClassTwo()
        child_archive.data.my_name = f'{my_name}'
        child_archive.data.my_class_one = []

        child_archive.data.my_class_one.append(MyClassOne())

        child_archive.data.my_class_one[0].my_value = [1, 2, 3, 4, 5]
        child_archive.data.my_class_one[0].my_time = [1, 2, 3, 4, 5]


        create_archive(
            child_archive.m_to_dict(),
            archive.m_context,
            example_filename,
            filetype,
            logger,
        )

        archive.data = MyClassOne()