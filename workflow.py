from pathlib import Path

import pyam
from nomenclature import DataStructureDefinition, RegionProcessor, process
from scenariocompass import ClimateCategorization, ScenarioCompassProcessor

try:
    from climate_processor import MAGICCProcessor, MAGICCRunType, Workflow
    from climate_processor.gcages_wrapper import SCI_OUTPUT_VARIABLES_DIAGNOSTIC

    FOUND_MAGICC = True
except ImportError:
    FOUND_MAGICC = False


here = Path(__file__).absolute().parent


def main(df: pyam.IamDataFrame) -> pyam.IamDataFrame:
    """Project/instance-specific workflow for scenario processing"""

    # Run the validation and region-processing
    definition = DataStructureDefinition(here / "definitions")
    df = process(
        df,
        definition,
        processor=[
            RegionProcessor.from_directory(here / "mappings", definition),
            ScenarioCompassProcessor(),
        ],
    )

    if FOUND_MAGICC:
        df = df.filter(region="World", keep=False).append(
            MAGICCProcessor(
                workflow=Workflow.SCI_V1_1,
                run_type=MAGICCRunType.COMPLETE,
                magicc_worker_number=4,
                include_input_data=True,
                magicc_variables=SCI_OUTPUT_VARIABLES_DIAGNOSTIC,
            ).apply(df.filter(region="World"))
        )
        # manual fix for https://github.com/iiasa/climate-processor/issues/105
        df.rename(unit={"GtC / yr": "GtC/yr"}, inplace=True)

        # change suffix for backward compatibility with SCI v1.1 release format
        df.rename(
            variable={
                i: i.replace("[SCI v1.1/MAGICC v7.6.0a3]", "[MAGICC v7.6.0a3]")
                for i in df.variable
                if "[SCI v1.1/MAGICC v7.6.0a3]" in i
            },
            inplace=True,
        )
        df.meta.rename(
            columns={
                i: i.replace("[SCI v1.1/MAGICC v7.6.0a3]", "[MAGICC v7.6.0a3]")
                for i in df.meta.columns
                if "[SCI v1.1/MAGICC v7.6.0a3]" in i
            },
            inplace=True,
        )
        df = ClimateCategorization().apply(df)

    return df
