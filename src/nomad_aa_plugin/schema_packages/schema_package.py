from typing import (
    TYPE_CHECKING,
)
import plotly.graph_objects as go

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

from nomad.datamodel.data import (
    ArchiveSection,
)

from nomad.datamodel.metainfo.plot import (
    PlotlyFigure,
    PlotSection,
)
from nomad.datamodel.hdf5 import HDF5Reference
from nomad.datamodel.metainfo.plot import PlotSection
from nomad.config import config
from nomad.datamodel.data import Schema
from nomad.datamodel.metainfo.annotations import (ELNAnnotation, ELNComponentEnum, H5WebAnnotation)
from nomad.metainfo import Quantity, SchemaPackage
from nomad.datamodel.data import EntryData
from nomad.metainfo import (
    Quantity,
    SubSection,
    Section,
)

m_package = SchemaPackage()


class MyClassOne(PlotSection, EntryData):

    m_def = Section(
        a_plotly_express={
            'method': 'line',
            'x': '#my_value',
            'y': '#my_time',
            'label': 'Example Express Plot',
            'index': 0,
            'layout': {
                'title': {'text': 'Example Express Plot'},
                'xaxis': {'title': {'text': 'x axis'}},
                'yaxis': {'title': {'text': 'y axis'}},
            },
        },
     )

    my_name = Quantity(
        type=str,
        a_eln=ELNAnnotation(
            component='StringEditQuantity',
        ),
    )

    my_value = Quantity(
        type=float,
        shape=['*'],
        unit = 'K',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
            defaultDisplayUnit='celsius',
        ),
    )

    my_time = Quantity(
        type=float,
        shape=['*'],
        unit = 's',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
            defaultDisplayUnit='minute',
        ),
    )

class MyClassOneHDF5(EntryData, ArchiveSection):
    """ 
    A test class for HDF5 data.
    """

    m_def = Section(a_h5web=H5WebAnnotation(axes='my_time', signal='my_value'))

    my_name = Quantity(
        type=str,
        a_eln=ELNAnnotation(
            component='StringEditQuantity',
        ),
    )

    my_value = Quantity(
        type=HDF5Reference,
        shape=[],
    )

    my_time = Quantity(
        type=HDF5Reference,
        shape=[],
    )

class MyClassTwo(EntryData, ArchiveSection):
    """
    An example class
    """
    m_def = Section(
        a_plot=[
            dict(
                label='Pressure and Temperature',
                x=[
                    'my_class_one/0/my_time',
                ],
                y=[
                    'my_class_one/0/my_value',
                ],
                lines=[
                    dict(
                        mode='lines',
                        line=dict(
                            color='rgb(25, 46, 135)',
                        ),
                    ),
                    dict(
                        mode='lines',
                        line=dict(
                            color='rgb(0, 138, 104)',
                        ),
                    ),
                ],
            ),
            # dict(
            #     x='sources/0/vapor_source/power/time',
            #     y='sources/0/vapor_source/power/value',
            # ),
        ],
    )

    my_name = Quantity(
        type=str,
        a_eln=ELNAnnotation(
            component='StringEditQuantity',
        ),
    )

    my_class_one = SubSection(
        section_def=MyClassOne,
        repeats=True,
    )


class MyClassTwoHDF5(EntryData, ArchiveSection):
    """
    An example class for hdf5 files
    """

    m_def = Section(
        a_h5web=H5WebAnnotation(
            paths=[
                'my_class_one/*',
            ]
        ),
    )

    my_name = Quantity(
        type=str,
        a_eln=ELNAnnotation(
            component='StringEditQuantity',
        ),
    )

    my_class_one = SubSection(
        section_def=MyClassOneHDF5,
        repeats=True,
    )


class MyClassThree(PlotSection, EntryData):
    """
    An example class
    """
    m_def = Section(
        a_plotly_graph_object=[
            {
                'label': 'shaft temperature',
                'index': 0,
                'dragmode': 'pan',
                'data': {
                    'type': 'scattergl',
                    'line': {'width': 2},
                    'marker': {'size': 6},
                    'mode': 'lines+markers',
                    'name': 'Temperature',
                    'x': '#my_time',
                    'y': '#my_value',
                },
                'layout': {
                    'title': {'text': 'Shaft Temperature'},
                    'xaxis': {
                        'showticklabels': True,
                        'fixedrange': True,
                        'ticks': '',
                        'title': {'text': 'Process time [min]'},
                        'showline': True,
                        'linewidth': 1,
                        'linecolor': 'black',
                        'mirror': True,
                    },
                    'yaxis': {
                        'showticklabels': True,
                        'fixedrange': True,
                        'ticks': '',
                        'title': {'text': 'Temperature [°C]'},
                        'showline': True,
                        'linewidth': 1,
                        'linecolor': 'black',
                        'mirror': True,
                    },
                    'showlegend': False,
                },
                'config': {
                    'displayModeBar': False,
                    'scrollZoom': False,
                    'responsive': False,
                    'displaylogo': False,
                    'dragmode': False,
                },
            },
            # {
            #     ...
            # },
        ],
    )
    name = Quantity(
        type=str,
        description="""
        Sample name.
        """,
        a_eln=ELNAnnotation(
            component='StringEditQuantity',
        ),
    )
    my_value = Quantity(
        type=float,
        shape=['*'],
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
        ),
    )

    my_time = Quantity(
        type=float,
        shape=['*'],
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
        ),
    )



class MyClassFour(PlotSection, EntryData):
    """
    Class autogenerated from yaml schema.
    """

    my_value = Quantity(
        type=float,
        shape=['*'],
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
        ),
    )

    my_time = Quantity(
        type=float,
        shape=['*'],
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
        ),
    )
    my_value_bis = Quantity(
        type=float,
        shape=['*'],
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
        ),
    )

    my_time_bis = Quantity(
        type=float,
        shape=['*'],
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
        ),
    )
    
    def normalize(self, archive, logger):

        # plotly figure
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=self.my_time,
                y=self.my_value,
                name='Sub Temp',
                line=dict(color='#2A4CDF', width=4),
                yaxis='y',
            ),
        )
        fig.add_trace(
            go.Scatter(
                x=self.my_time_bis,
                y=self.my_value_bis,
                name='Pyro Temp',
                line=dict(color='#90002C', width=2),
                yaxis='y',
            ),
        )
        fig.update_layout(
            template='plotly_white',
            dragmode='zoom',
            xaxis=dict(
                fixedrange=False,
                autorange=True,
                title='Process time / s',
                mirror='all',
                showline=True,
                gridcolor='#EAEDFC',
            ),
            yaxis=dict(
                fixedrange=False,
                title='Temperature / °C',
                tickfont=dict(color='#2A4CDF'),
                gridcolor='#EAEDFC',
            ),
            showlegend=True,
        )
        self.figures = [PlotlyFigure(label='my figure 1', figure=fig.to_plotly_json())]


class MyClassFive(EntryData, ArchiveSection):
    """
    An example class
    """

    name = Quantity(
        type=str,
        description="""
        Sample name.
        """,
        a_eln=ELNAnnotation(
            component='StringEditQuantity',
        ),
    )

    reference = Quantity(
        type=MyClassOne,
        description="A reference to a NOMAD `MyClassOne` entry.",
        a_eln=ELNAnnotation(
            component="ReferenceEditQuantity",
            label="MyClassOne Reference",
        ),
    )


m_package.__init_metainfo__()
