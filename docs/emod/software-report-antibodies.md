# ReportAntibodies


The antibodies report (ReportAntibodiesCapacity.csv or ReportAntibodiesConcentration.csv)  is a csv-formatted report that
provides antibodies data for each qualifying individual on user-determined days of simulation. For example,
individuals between ages 5 and 10 years old, living in node 1, who have the intervention "UsageDependentBednet" and
have the individual property "Risk:LOW" will be documented from day 365 to day 465 of the simulation at 10 day intervals.
The report contains one row per individual per reporting day, with each antibody represented as a separate column.
The values in the report can be either the concentration or capacity of each antibody, depending on user configuration.

Note: This report gets very large, very quickly as well as adding processing time. It is advised to use the
**Reporting_Interval** and other filtering options to limit the size of the report.


## Configuration


To generate this report, the following parameters must be configured in the custom_reports.json file:

{{ read_csv('../csv/report-antibodies.csv', keep_default_na=False) }}

```json
{
    "Reports": [
        {
            "class": "ReportAntibodies",
            "Filename_Suffix": "Node1",
            "Start_Day": 365,
            "End_Day": 465,
            "Node_IDs_Of_Interest": [ 1 ],
            "Min_Age_Years": 5,
            "Max_Age_Years": 10,
            "Must_Have_IP_Key_Value": "Risk:LOW",
            "Must_Have_Intervention": "UsageDependentBednet",
            "Reporting_Interval": 10.0,
            "Contain_Capacity_Data": 1,
            "Infected_Only": 0
        }
    ],
    "Use_Defaults": 1
}
```

### Stratification columns


| Parameter | Data type | Description |
| --- | --- | --- |
| `Time` | integer | The day of the simulation that the data was collected. |
| `NodeID` | integer | The External ID of the node that the data is being collected for. |
| `IndividualID` | integer | The ID of the individual who received the drug. |
| `Gender` | enum | The gender of the individual. Possible values are M or F. |
| `AgeYears` | integer | The max age in years of the age bin for the individual. |
| `Infected` | boolean | A true value (1) indicates the individual is currently infected and a false value (0) indicates the individual is not currently infected. |
| `PyrogenicThreshold` | float | The pyrogenic threshold of the individual at the time of the report collection. |
| `FeverKillingRate` | float | The fever infected red blood cells kill rate of the individual at the time of the report collection. |

### Data columns


Note: The report only records people who have been at least exposed to antigens, though they may not currently have measurable antibody levels.
Antibodies that have not been triggered will appear as an empty field in the report.
Antibodies that have been triggered will appear with a numeric value (concentration or capacity) in the report, even if the value is zero.

| Parameter | Data type | Description |
| --- | --- | --- |
| `MSP_X` | float | There will be n number of columns named 'MSP_0' to 'MSP_(n-1)' where n is the number of MSP variants as defined by **Falciparum_MSP_Variants** configuration parameter. The value is the concentration or capacity of each MSP antibody variant, depending on the **Contain_Capacity_Data** setting. |
| `PfEMP1_X` | float | There will be m number of columns named 'PfEMP1_0' to 'PfEMP1_(m-1)' where m is the number of PfEMP1 variants as defined by **Falciparum_PfEMP1_Variants** configuration parameter. The value is the concentration or capacity of each PfEMP1 antibody variant, depending on the **Contain_Capacity_Data** setting. |

## Example


The following are examples of ReportAntibodiesConcentration.csv and ReportAntibodiesCapacity.csv files.

{{ read_csv("csv/report-antibodies-capacity.csv", keep_default_na=False) }}

{{ read_csv("csv/report-antibodies-concentration.csv", keep_default_na=False) }}
