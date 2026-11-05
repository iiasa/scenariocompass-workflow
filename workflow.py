from pathlib import Path

import pyam
from climate_processor import MAGICCProcessor, Workflow
from nomenclature import DataStructureDefinition, RegionProcessor, process
from scenariocompass import ClimateCategorization

here = Path(__file__).absolute().parent


def main(df: pyam.IamDataFrame) -> pyam.IamDataFrame:
    """Project/instance-specific workflow for scenario processing"""

    # Run the validation and region-processing
    definition = DataStructureDefinition(here / "definitions")
    return process(
        df,
        definition,
        processor=[
            RegionProcessor.from_directory(path=here / "mappings", definition),
            MAGICCProcessor(workflow=Workflow.SCI),
            ClimateCategorization(),
        ],
    )
