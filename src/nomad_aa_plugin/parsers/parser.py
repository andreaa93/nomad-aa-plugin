from typing import (
    TYPE_CHECKING,
)

import pandas as pd

import h5py

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )

from nomad.units import ureg
from nomad.datamodel.datamodel import EntryArchive
from nomad.parsing import MatchingParser
from nomad.parsing.parser import MatchingParser
from nomad.utils import hash
from pdi_nomad_plugin.utils import (
    create_archive,
)

from nomad_aa_plugin.schema_packages.schema_package import (
    MyClassFive,
    MyClassOne,
    MyClassOneHDF5,
    MyClassTwo,
    MyClassTwoHDF5,
)


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

        my_class_one_subsec = MyClassOne()
        my_class_one_subsec.my_value = df_csv["ValueTwo"]
        my_class_one_subsec.my_time = df_csv["ValueTwo2"]

        # check which args the function m_add_subsection accepts: packages/nomad-FAIR/nomad/metainfo/metainfo.py
        # DO NOT use list.append() to add a subsection to a section!
        child_archive.data.m_add_sub_section(MyClassTwo.my_class_one, my_class_one_subsec)

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

        main_archive.data.reference = f"../uploads/{upload_id}/archive/{entry_id}#data"

        create_archive(
            main_archive.m_to_dict(),
            archive.m_context,
            main_archive_filename,
            filetype,
            logger,
        )
        
        archive.data = MyClassFive()
        archive.data.name = "My namy name"
        archive.data.reference = f"../uploads/{upload_id}/archive/{entry_id}#data"


def set_dataset_unit(hdf_file, dataset_name, attribute_value):
    """
    Set the unit attribute for a dataset in an HDF5 file.

    """
    if dataset_name in hdf_file:
        dataset = hdf_file[dataset_name]
        dataset.attrs['units'] = attribute_value

class MyParserFour(MatchingParser):
    def parse(
        self,
        mainfile: str,
        archive: EntryArchive,
        logger,
    ) -> None:
        
        data_file = mainfile.split('/')[-1]

        # other useful strings:
        # folder_name = mainfile.split('/')[-2]
        # upload_path = f"{mainfile.split('raw/')[0]}raw/"

        df_csv = pd.read_csv(mainfile, sep=',') #, decimal=',', engine='python')
    
        child_archives = {
            'experiment': EntryArchive(),
            'instrument': EntryArchive(),
            'process': EntryArchive(),
        }

        my_name = "And"
        filetype = 'yaml'

        # # # # # HDF5 FILE CREATION # # # # #
        hdf_filename = f'{data_file[:-4]}.h5'
        with archive.m_context.raw_file(hdf_filename, 'w') as newfile:
            with h5py.File(newfile.name, 'w') as hdf:
                group_name = f"my_group_{my_name}"
                group = hdf.create_group(group_name)
                group.create_dataset('value', data=df_csv["ValueFour"])
                group.create_dataset('time', data=df_csv["ValueFour2"])
                group.attrs['signal'] = 'value'
                group.attrs['axes'] = 'time'
                group.attrs['NX_class'] = 'NXdata'

        child_archives['process'].data = MyClassTwoHDF5()
        child_archives['process'].data.my_name = f'{my_name}'
        child_archives['process'].data.my_class_one = []

        child_archives['process'].data.my_class_one.append(MyClassOneHDF5())

        child_archives['process'].data.my_class_one[0].my_value = f'/uploads/{archive.m_context.upload_id}/raw/{hdf_filename}#/{group_name}/value'
        child_archives['process'].data.my_class_one[0].my_time = f'/uploads/{archive.m_context.upload_id}/raw/{hdf_filename}#/{group_name}/time'

        # other code ....

        # reopen the hdf5 file to add units
        with archive.m_context.raw_file(hdf_filename, 'a') as newfile:
            with h5py.File(newfile.name, 'a') as hdf:
                hdf[f"my_group_{my_name}/value"].attrs['units'] = 'K'
                hdf[f"my_group_{my_name}/time"].attrs['units'] = 'sec'
                
        
        example_filename = f'{my_name}_testHDF5.archive.{filetype}'

        create_archive(
            child_archives['process'].m_to_dict(),
            archive.m_context,
            example_filename,
            filetype,
            logger,
        )

        archive.data = MyClassOne()


class MyParserFive(MatchingParser):
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

        my_class_one_subsec = MyClassOne()
        # use .to_numpy() method to avoid the error: 
        # Quantity cannot wrap upcast type <class 'pandas.core.series.Series'>
        my_class_one_subsec.my_value = ureg.Quantity(
            df_csv["ValueFive"].to_numpy(),
            ureg('celsius'),
        )
        # use .to_numpy() method to avoid the error: 
        # Quantity cannot wrap upcast type <class 'pandas.core.series.Series'>
        my_class_one_subsec.my_time =  ureg.Quantity(
            df_csv["ValueFive2"].to_numpy(),
            ureg('minute'),
        )

        # use the syntax my_variable.to('hour').magnitude to convert the units

        # check which args the function m_add_subsection accepts: packages/nomad-FAIR/nomad/metainfo/metainfo.py
        # DO NOT use list.append() to add a subsection to a section!
        child_archive.data.m_add_sub_section(MyClassTwo.my_class_one, my_class_one_subsec)

        create_archive(
            child_archive.m_to_dict(),
            archive.m_context,
            example_filename,
            filetype,
            logger,
        )

        archive.data = MyClassOne()