# ReportEventRecorder


The health events and interventions report (ReportEventRecorder.csv) provides information on each
individual's demographics and health status at the time of an event. Additionally, it is possible to
see the value of specific **IndividualProperties**, as assigned in the demographics file (see
[NodeProperties and IndividualProperties](parameter-demographics.md#nodeproperties-and-individualproperties) for more information).

This report is highly customizable; see the Configuration section, below, for details and instructions.
Disease-specific information and examples are provided at the end of page.


## Configuration


To generate this report, the following parameters must be configured in the config.json file (applies
to all simulation types):

{{ read_csv('../csv/report-event-recorder.csv', keep_default_na=False) }}

```json
{
    "Report_Event_Recorder": 1,
    "Report_Event_Recorder_Events": [],
    "Report_Event_Recorder_Ignore_Events_In_List": 1,
    "Report_Event_Recorder_Individual_Properties": ["Risk"],
    "Report_Event_Recorder_Start_Day": 1,
    "Report_Event_Recorder_End_Day": 300,
    "Report_Event_Recorder_Node_IDs_Of_Interest": [1, 2, 3],
    "Report_Event_Recorder_PropertyChange_IP_Key_Of_Interest": "",
    "Report_Event_Recorder_Min_Age_Years": 20,
    "Report_Event_Recorder_Max_Age_Years": 60,
    "Report_Event_Recorder_Must_Have_IP_Key_Value": "Risk:HIGH",
    "Report_Event_Recorder_Must_Have_Intervention": ""
}
```

## Output file data


The report contains the following data channels for malaria simulations.

| Data channel | Data type | Description |
| --- | --- | --- |
| `Time` | float | The time of the event, in days. |
| `Node_ID` | integer | The identification number of the node. |
| `Event_Name` | string | The event being logged. If **Report_Event_Recorder_Ignore_Events_In_List** is set to 0, then the event name will be one of the ones listed under **Report_Event_Recorder_Events**. Otherwise, it will be the name of any other event that occurs and is not listed under **Report_Event_Recorder_Events**. |
| `Individual_ID` | integer | The individual's unique identifying number. |
| `Age` | integer | The age of the individual in units of days. Divide by 365 to obtain age in years. |
| `Gender` | character | The gender of the individual: "M" for male, or "F" for female. |
| `Infected` | boolean | Describes whether the individual is infected or not; 0 when not infected, 1 for infected. |
| `Infectiousness` | float | A value ranging from 0 to 1 that indicates how infectious an individual is, with 0 = not infectious and 1 = very infectious. HIV and malaria simulation types have specific definitions listed below. |
| `<IP Key>` | string | An additional column will be added to the report for each IP Key listed in **Report_Event_Recorder_Individual_Properties**. The values shown in each column will be the value for the indicated key, for that individual, at the time of the event. |
| `RelativeBitingRate` | float | A number indicating the likelihood of an individual being bitten by mosquitoes. This can include any biting rates set by the user and/or a value based on the age or size of the individual. |
| `HasClinicalSymptoms` | T/F | T implies that the person's fever has been above **Clinical_Fever_Threshold_Low** for at least **Min_Days_Between_Clinical_Incidents** since the person was a NewClinicalCase (their fever first peaked above **Clinical_Fever_Threshold_High**), F implies that the person is not considered to have clinical symptoms. |
| `TrueParasiteDensity` | float | The number of infected red blood cells per microliter of blood. |
| `TrueGametocyteDensity` | float | The true number of gametocytes per microliter of blood. |

## Example


The following is an example of a ReportEventRecorder.csv report from a malaria simulation:

| Time | Node_ID | Event_Name | Individual_ID | Age | Gender | Infected | Infectiousness | RelativeBitingRate | TrueParasiteDensity | TrueGametocyteDensity | HasClinicalSymptoms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 30 | 7 | EveryUpdate | 15 | 4797.43 | M | 1 | 0 | 1 | 19791.2 | 0 | T |
| 35 | 7 | EveryUpdate | 1037 | 642.683 | F | 1 | 0.227641 | 1 | 644.143 | 42.5087 | F |
| 35 | 7 | EveryUpdate | 1058 | 12432.7 | F | 1 | 0.036678 | 1 | 970.459 | 7.63285 | F |
| 35 | 7 | EveryUpdate | 1065 | 14232.2 | F | 1 | 0.006245 | 1 | 110913 | 7.63259 | T |
| 35 | 7 | EveryUpdate | 1093 | 19206.8 | F | 1 | 0.035739 | 1 | 1020.28 | 7.63263 | F |
| 35 | 7 | EveryUpdate | 1114 | 17144.3 | M | 1 | 0.006236 | 1 | 73854.4 | 7.63208 | T |
| 35 | 7 | EveryUpdate | 1135 | 5739.73 | F | 1 | 0.007743 | 1 | 106963 | 9.4479 | T |
| 35 | 7 | EveryUpdate | 1149 | 6064.07 | F | 1 | 0.044953 | 1 | 1138.48 | 9.00229 | F |
| 35 | 7 | EveryUpdate | 1163 | 21692.3 | M | 1 | 0.006216 | 1 | 118332 | 7.63267 | T |
| 35 | 7 | EveryUpdate | 1170 | 14238.3 | F | 1 | 0.006216 | 1 | 118332 | 7.6325 | T |
| 35 | 7 | EveryUpdate | 6924 | 7388.82 | F | 1 | 0.03641 | 1 | 1248.47 | 7.63267 | F |
| 35 | 7 | EveryUpdate | 6938 | 20377.8 | F | 1 | 0.006216 | 1 | 118331 | 7.63272 | T |
| 35 | 7 | EveryUpdate | 6952 | 29412.4 | M | 1 | 0.006216 | 1 | 118333 | 7.63291 | T |
| 35 | 7 | EveryUpdate | 6959 | 32766.3 | M | 1 | 0.037062 | 1 | 952.578 | 7.63273 | F |
| 35 | 7 | EveryUpdate | 6966 | 1245.33 | F | 1 | 0.025033 | 1 | 64225.2 | 30.0704 | T |
| 35 | 7 | EveryUpdate | 6994 | 13428.8 | F | 1 | 0.006236 | 1 | 113029 | 7.63279 | T |
| 40 | 7 | EveryUpdate | 15 | 4807.43 | M | 1 | 1 | 1 | 14.8706 | 940.014 | F |
