# ReportInfectionStatsMalaria


The malaria infection statistics report (ReportInfectionStatsMalaria.csv) provides per-infection
parasite burden data for every active infection in the simulation at each reporting interval. For
each infection it records the individual's identity and demographics, the infectiousness of the
individual, the current age of the infection, and — depending on configuration — the counts of
hepatocytes, infected red blood cells (IRBCs), and gametocytes associated with that infection.
Because the report produces one row per active infection per individual per reporting interval, the
output can be large; use **Start_Day**, **End_Day**, and **Reporting_Interval** to limit its size.

This report is only available for `MALARIA_SIM` simulations.


## Configuration


To generate this report, configure the following parameters in the custom_reports.json file:

{{ read_csv('../csv/report-infection-stats-malaria.csv', keep_default_na=False) }}

!!! note
    A row is only written if every enabled column meets its corresponding threshold. If any
    enabled threshold is not met, the entire row is omitted.

```json
{
    "Reports": [
        {
            "class": "ReportInfectionStatsMalaria",
            "Start_Day": 3860,
            "End_Day": 3880,
            "Reporting_Interval": 1,
            "Include_Column_Hepatocyte": 1,
            "Include_Column_IRBC": 1,
            "Include_Column_Gametocyte": 1,
            "Include_Data_Threshold_Hepatocytes": 0,
            "Include_Data_Threshold_IRBC": 0,
            "Include_Data_Threshold_Gametocytes": 0
        }
    ],
    "Use_Defaults": 1
}
```

## Output file data


The output file is named `ReportInfectionStatsMalaria.csv`. The report contains the following
columns.

| Column | Data type | Description |
| --- | --- | --- |
| `Time` | float | The simulation time in days when the data was collected. |
| `NodeID` | integer | The external ID of the node where the individual is currently present. |
| `IndividualID` | integer | The unique ID of the individual carrying the infection. |
| `Gender` | enum | The gender of the individual. Possible values are M or F. |
| `AgeYears` | float | The age of the individual in years at the time of data collection. |
| `InfectionID` | integer | The unique ID of the infection. |
| `Infectiousness` | float | The infectiousness of the individual — the probability that a feeding mosquito will become infected. This value is based on the total number of gametocytes in the bloodstream contributed by all of the individual's infections. |
| `Duration` | float | The duration in days of this infection at the time of data collection. |
| `Hepatocytes` | integer | The number of infected hepatocytes associated with this infection. Only present if **Include_Column_Hepatocyte** is true. |
| `IRBCs` | integer | The number of infected red blood cells associated with this infection. Only present if **Include_Column_IRBC** is true. |
| `Gametocytes` | integer | The total number of mature gametocytes (male and female combined) associated with this infection. Only present if **Include_Column_Gametocyte** is true. |

## Example


The following is an example of ReportInfectionStatsMalaria.csv.

{{ read_csv("csv/report-infection-stats-malaria.csv", keep_default_na=False) }}
