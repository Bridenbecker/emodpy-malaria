# ReportFpgNewInfections


The full parasite genetics new infections report (ReportFpgNewInfections.csv) provides very detailed information on
new human infections for simulations where **Malaria_Model** is set to MALARIA_MECHANISTIC_MODEL_WITH_PARASITE_GENETICS.

!!! seealso
    [FPG model](malaria-model-fpg.md) — For an overview of the FPG model, genome configuration, and the full FPG workflow.

When **Report_Crossover_Data_Instead** is set to true, it provides less detailed information on the new infections
and includes GenomeCrossoverLocations data column that provides a list of crossovers that created this new infection's
genome.



## Configuration


To generate this report, configure the following parameters in the custom_report.json file:

{{ read_csv('../csv/report-fpg-new-infections.csv', keep_default_na=False) }}

```json
{
    "Reports": [
        {
            "Start_Day": 500,
            "End_Day": 1000,
            "Filename_Suffix": "Crossovers",
            "Node_IDs_Of_Interest": [],
            "Min_Age_Years": 0,
            "Max_Age_Years": 1000,
            "Must_Have_IP_Key_Value": "",
            "Must_Have_Intervention": "",
            "Report_Crossover_Data_Instead": 1,
            "class": "ReportFpgNewInfections"
        }
    ],
    "Use_Defaults": 1
}
```

## Output data with Report_Crossover_Data_Instead = 0


Each row of the report is one new human infection.
The report contains the following stratification columns:

| Parameter | Data type | Description |
| --- | --- | --- |
| `SporozoiteToHuman_Time` | float | The day of the simulation this infection happened. |
| `SporozoiteToHuman_NodeID` | integer | The ID of the node in which this infection happened. |
| `SporozoiteToHuman_VectorID` | integer | The ID of the vector from which the human got this infection. |
| `SporozoiteToHuman_BiteID` | integer | The ID of the bite from which the human got this infection. |
| `SporozoiteToHuman_HumanID` | integer | The ID of the human that got this infection. |
| `SporozoiteToHuman_NewInfectionID` | integer | The ID of this infection. |
| `SporozoiteToHuman_NewGenomeID` | integer | The genome ID of this infection. |
| `HomeNodeID` | integer | The home node ID of the human (the node in which they started the simulation) who received this new infection. |
| `GametocyteToVector_Time` | float | The day the vector acquired gametocytes (bit an infectious human) that eventually became this new infection. |
| `GametocyteToVector_NodeID` | integer | The ID of the node in which the vector acquired gametocytes. |
| `GametocyteToVector_VectorID` | integer | The ID of the vector from which the human got this infection. |
| `GametocyteToVector_BiteID` | integer | The ID of the bite during which the vector acquired gametocytes that became this new infection. |
| `GametocyteToVector_HumanID` | integer | The ID of the human from whom the vector acquired gametocytes that became this new infection. |
| `FemaleGametocyteToVector_InfectionID` | integer | The ID of the vector to human infection that generated female gametocytes that were acquired by the vector that became this infection. |
| `FemaleGametocyteToVector_GenomeID` | integer | The genome ID of the female gametocytes that were acquired by the vector that became this infection. |
| `MaleGametocyteToVector_InfectionID` | integer | The ID of the vector to human infection that generated male gametocytes that were acquired by the vector that became this infection. |
| `MaleGametocyteToVector_GenomeID` | integer | The genome ID of the male gametocytes that were acquired by the vector that became this infection. |

## Output data with Report_Crossover_Data_Instead = 1


Each row of the report is one new human infection. This is the output when **Report_Crossover_Data_Instead** is set to true (1).
The report contains the following stratification columns:

| Parameter | Data type | Description |
| --- | --- | --- |
| `SporozoiteToHuman_Time` | float | The day of the simulation this infection happened. |
| `SporozoiteToHuman_NewInfectionID` | integer | The ID of this infection. |
| `SporozoiteToHuman_NewGenomeID` | integer | The genome ID of this infection. |
| `FemaleGametocyteToVector_InfectionID` | integer | The ID of the vector to human infection that generated female gametocytes that were acquired by the vector that became this infection. |
| `FemaleGametocyteToVector_GenomeID` | integer | The genome ID of the female gametocytes that were acquired by the vector that became this infection. |
| `MaleGametocyteToVector_InfectionID` | integer | The ID of the vector to human infection that generated male gametocytes that were acquired by the vector that became this infection. |
| `MaleGametocyteToVector_GenomeID` | integer | The genome ID of the male gametocytes that were acquired by the vector that became this infection. |
| `GenomeCrossoverLocations` | array of integers | The genome locations of crossovers that happened during the recombination to create the genome of this infection. |

## Examples


The following is an example of ReportFpgNewInfections.csv with Report_Crossover_Data_Instead = 0

{{ read_csv("csv/report-fpg-new-infections.csv", keep_default_na=False) }}

The following is an example of ReportFpgNewInfections.csv with Report_Crossover_Data_Instead = 1

{{ read_csv("csv/report-fpg-new-infections-crossovers.csv", keep_default_na=False) }}
