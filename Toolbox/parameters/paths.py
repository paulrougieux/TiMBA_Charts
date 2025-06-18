from pathlib import Path

PACKAGEDIR = Path(__file__).resolve().parent.parent
SCINPUTPATH = PACKAGEDIR / Path("Input") / Path("Scenario_Files")
SCFOLDERPATH = Path("Input")
ADDINFOPATH = Path("Input") / Path("Additional_Information")
COUNTRYINFO = "country_info.csv"
COMMODITYINFO = "commodity_info.csv"
FORESTINFO = "Forest_world500.csv"
HISTINFO = "FAO_Data.csv"
FORMIP = "external_model_data.csv"

FORMIPPATH = PACKAGEDIR / ADDINFOPATH / FORMIP