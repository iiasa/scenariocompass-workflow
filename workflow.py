from pathlib import Path

import pyam
from climate_processor import MAGICCProcessor, Workflow
from nomenclature import DataStructureDefinition, RegionProcessor, process

here = Path(__file__).absolute().parent


def main(df: pyam.IamDataFrame) -> pyam.IamDataFrame:
    """Project/instance-specific workflow for scenario processing"""

    # Run the validation and region-processing
    dsd = DataStructureDefinition(here / "definitions")
    region_processor = RegionProcessor.from_directory(path=here / "mappings", dsd=dsd)
    magicc_processor = MAGICCProcessor(workflow=Workflow.SCI)
    return process(
        df,
        dsd,
        processor=[
            region_processor,
            magicc_processor,
        ],
    )
