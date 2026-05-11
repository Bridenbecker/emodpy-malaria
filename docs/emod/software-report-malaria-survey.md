# MalariaSurveyJSONAnalyzer


The malaria survey report (MalariaSurveyJSONAnalyzer.json) is a JSON-formatted report that provides
detailed information on an individual for each event that occurs during the reporting interval.
Multiple files can be created for each reporting interval.




## Configuration


To generate this report, the following parameters must be configured in the custom_reports.json file:

{{ read_csv('../csv/report-malaria-survey.csv', keep_default_na=False) }}

```json
{
    "Reports": [
        {
            "class": "MalariaSurveyJSONAnalyzer",
            "Filename_Suffix": "Node1",
            "Start_Day": 365,
            "End_Day": 465,
            "Node_IDs_Of_Interest": [1],
            "Min_Age_Years": 5,
            "Max_Age_Years": 10,
            "Must_Have_IP_Key_Value": "Accessibility:YES",
            "Must_Have_Intervention": "UsageDependentBednet",
            "Event_Trigger_List": ["EveryUpdate"],
            "Reporting_Interval": 10,
            "Max_Number_Reports": 1,
            "Pretty_Format": 1,
            "IP_Key_To_Collect": "Risk"
        }
    ],
    "Use_Defaults": 1
}
```

## Output file data


The report contains the following information:

| Parameter | Data type | Description |
| --- | --- | --- |
| `ntsteps` | integer | The number of days of the simulation for which data was collected. It equals the reporting interval unless the simulation ended before the reporting interval. |
| `patient_array` | array of strings | An array where there is an entry for each individual that experiences the specified event(s) during the reporting interval. If no events are listed, an exception is thrown. The data in a patient array contain two types of data: data that has one value for each timestep or day and data that is an array of data. |

### Patient_array channels


| Parameter | Data type | Description |
| --- | --- | --- |
| `id` | string | The individual ID of the person. |
| `node_id` | string | The External ID of the node that the person is currently in on the first event. |
| `initial_age` | float | The initial age of the person (in days) when the report started tracking them. This value will be non-zero for individuals created at initialization, but should be zero for the rest of the population. |
| `local_birthday` | float | The day that the individual was born/created, in relation to the start of the report. |

Each of the following statistics is presented as an array, where each entry is the value of that field
at the time of the event.

| Parameter | Description |
| --- | --- |
| `strain_ids` | The antigen/clade ID and the genome ID of the individual's current infection. |
| `ip_data` | If an **IP_Key_To_Collect** was specified, this will be that value. If it was not specified, this will show the value for all of the IPs. |
| `true_asexual_parasites` | The actual parasite density of the individual. |
| `true_gametocytes` | The actual gametocyte density of the individual. |
| `smeared_true_asexual_parasites` | The actual parasite density, smeared using NASBADensityWithUncertainty. |
| `smeared_true_gametocytes` | The actual gametocyte density, smeared using NASBADensityWithUncertainty. |
| `asexual_parasites` | The parasite density measured using the BLOOD_SMEAR_PARASITES diagnostic. |
| `gametocytes` | The gametocyte density measured using the BLOOD_SMEAR_GAMETOCYTES diagnostic. |
| `pcr_parasites` | The parasite density measured using the PCR_PARASITES diagnostic. |
| `pcr_gametocytes` | The gametocyte density measured using the PCR_GAMETOCYTES diagnostic. |
| `pfhrp2` | The HRP2 measured using the PF_HRP2 diagnostic. |
| `smeared_asexual_parasites` | Positive fields of view (pos_asexual_fields) with parasite density. |
| `smeared_gametocytes` | Positive fields of view (pos_gametocyte_fields) with gametocyte density. |
| `infectiousness` | Infectiousness of the individual at the time of the event. |
| `infectiousness_smeared` | Binomial infectiousness smearing. |
| `infectiousness_age_scaled` | Infectiousness adjusted for age dependent Surface Area Biting. |
| `pos_asexual_fields` | The number of positive fields of view for parasite smears. |
| `pos_gametocyte_fields` | The number of positive fields of view for gametocyte smears. |
| `temps` | The individual's body temperature in Celsius if they have a fever, otherwise it is -1. |

## Example


The following is a sample of a MalariaSurveyJSONAnalyzer file.

```json
{
    "ntsteps": 73,
    "patient_array": [
        {
            "id": 5,
            "node_id": 340461476,
            "initial_age": 2497.267822266,
            "local_birthday": -2466.267822266,
            "strain_ids": [[0, 9947867]],
            "ip_data": [""],
            "true_asexual_parasites": [392.6246337891],
            "true_gametocytes": [0],
            "smeared_true_asexual_parasites": [48.01840209961],
            "smeared_true_gametocytes": [0],
            "asexual_parasites": [380],
            "gametocytes": [0],
            "pcr_parasites": [98.8094329834],
            "pcr_gametocytes": [0],
            "pfhrp2": [9.302060127258],
            "smeared_asexual_parasites": [397.7009277344],
            "smeared_gametocytes": [0],
            "infectiousness": [0],
            "infectiousness_smeared": [0],
            "infectiousness_age_scaled": [0],
            "pos_asexual_fields": [126],
            "pos_gametocyte_fields": [0],
            "temps": [38.01483154297]
        },
        {
            "id": 11,
            "node_id": 340461476,
            "initial_age": 1387.354614258,
            "local_birthday": -1315.354614258,
            "strain_ids": [[0, 505461], [0, 0]],
            "ip_data": [""],
            "true_asexual_parasites": [444.5673217773],
            "true_gametocytes": [0],
            "smeared_true_asexual_parasites": [1481.205932617],
            "smeared_true_gametocytes": [0],
            "asexual_parasites": [490],
            "gametocytes": [0],
            "pcr_parasites": [463.1502380371],
            "pcr_gametocytes": [0],
            "pfhrp2": [10.62057304382],
            "smeared_asexual_parasites": [449.572052002],
            "smeared_gametocytes": [0],
            "infectiousness": [0],
            "infectiousness_smeared": [0],
            "infectiousness_age_scaled": [0],
            "pos_asexual_fields": [135],
            "pos_gametocyte_fields": [0],
            "temps": [38.0454750061]
        }
    ]
}
```
