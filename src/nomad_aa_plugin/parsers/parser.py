from typing import (
    TYPE_CHECKING,
)
import pandas as pd 

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


from nomad.utils import hash

from pdi_nomad_plugin.utils import (
    create_archive,
)

from nomad_aa_plugin.schema_packages.schema_package import MyClassTwo, MyClassOne, MyClassFive

class MyParserOne(MatchingParser):
    def parse(
        self,
        mainfile: str, 
        archive: EntryArchive,
        logger,
    ) -> None:
        
        df_csv = pd.read_csv(mainfile, sep=',') #, decimal=',', engine='python')

        archive.data = MyClassOne()
        archive.data.my_value = df_csv["ValueOne"]
        archive.data.my_time = df_csv["ValueOne2"]


class MyParserTwo(MatchingParser):
    def parse(
        self,
        mainfile: str, 
        archive: EntryArchive,
        logger,
    ) -> None:
        
        df_csv = pd.read_csv(mainfile, sep=',') #, decimal=',', engine='python')

        archive.data = MyClassOne()
    
        child_archive = EntryArchive()

        my_name = "And"
        filetype = 'yaml'

        example_filename = f'{my_name}.archive.{filetype}'

        child_archive.data = MyClassTwo()
        child_archive.data.my_name = f'{my_name}'
        child_archive.data.my_class_one = []

        child_archive.data.my_class_one.append(MyClassOne())

        child_archive.data.my_class_one[0].my_value = df_csv["ValueTwo"]
        child_archive.data.my_class_one[0].my_time = df_csv["ValueTwo2"]

        create_archive(
            child_archive.m_to_dict(),
            archive.m_context,
            example_filename,
            filetype,
            logger,
        )

        archive.data = MyClassOne()


class MyParserThree(MatchingParser):
    def parse(
        self,
        mainfile: str, 
        archive: EntryArchive,
        logger,
    ) -> None:
        
        df_csv = pd.read_csv(mainfile, sep=',') #, decimal=',', engine='python')

        archive.data = MyClassFive()
        archive.data.name = "My namy name"
        

        filetype = 'yaml'
        main_archive_filename = f'main.archive.{filetype}'
        test_filename = f'test.archive.{filetype}'
        
        main_archive = EntryArchive()
        main_archive.data = MyClassFive(
            name="experiment",
        )

        new_archive = EntryArchive()
        new_archive.data = MyClassOne(
            my_name="stuff to be referenced",
            my_value = df_csv["ValueThree"],
            my_time = df_csv["ValueThree2"],
        )

        create_archive(
            new_archive.m_to_dict(),
            archive.m_context,
            test_filename,
            filetype,
            logger,
        )

        entry_id = hash(archive.m_context.upload_id, test_filename)
        upload_id = archive.m_context.upload_id

        main_archive.data.reference = f"/uploads/{upload_id}/archive/{entry_id}#data",


        create_archive(
            main_archive.m_to_dict(),
            archive.m_context,
            main_archive_filename,
            filetype,
            logger,
        )