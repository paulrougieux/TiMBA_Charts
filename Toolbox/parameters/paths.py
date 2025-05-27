from pathlib import Path

PACKAGEDIR = Path(__file__).resolve().parent.parent
SCINPUTPATH = PACKAGEDIR / Path("Input") / Path("Scenario_Files")
AIINPUTPATH = PACKAGEDIR / Path("Input") / Path("Additional_Information")
SCFOLDERPATH = Path("Input")
#ADDINFOPATH = Path("Input") / Path("Additional_Information")
COUNTRYINFO = "country_info.csv"
COMMODITYINFO = "commodity_info.csv"
FORESTINFO = "Forest_world500.csv"
HISTINFO = "FAO_Data.csv"