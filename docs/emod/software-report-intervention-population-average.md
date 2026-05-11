# ReportInterventionPopAvg


ReportInterventionPopAvg is a CSV-formatted report that gives population average
data on the usage of interventions.  It provides data on the fraction of people
or nodes that have an intervention as well as averages on the intervention's efficacy.
For each persistent intervention that has been distributed to a node or person,
the report provides one line in the CSV for each intervention used in that node.
Since node-level interventions (usually vector control) can only have one per node,
the data will be for that one intervention.  The individual-level interventions
will have data for the people in that node.

The report will only collect data on persistent interventions.  These are interventions
that a person has between time steps.  These are things like SimpleBednet.  In contrast,
diagnostic interventions are usually executed in the time step they are distributed
and do not exist between time steps.

Not all interventions provide data for this report.  If an intervention does not
provide support, there should be one warning in the standard out indicating this.

For information on what interventions have what effects, please check the following:

* [Individual-level interventions](parameter-campaign-individual-interventions.md)
* [Node-level interventions](parameter-campaign-node-interventions.md)

## Configuration


To generate this report, the following parameters must be configured in the custom_reports.json file:

{{ read_csv('../csv/report-intervention-population-average.csv', keep_default_na=False) }}

```json
{
    "Reports": [
        {
            "class": "ReportInterventionPopAvg",
            "Filename_Suffix": "AllNodes",
            "Start_Day": 90,
            "End_Day": 1000,
            "Node_IDs_Of_Interest": [],
            "Min_Age_Years": 5,
            "Max_Age_Years": 10,
            "Must_Have_IP_Key_Value": "Risk:HIGH",
            "Must_Have_Intervention": "UsageDependentBednet"
        }
    ],
    "Use_Defaults": 1
}
```

## Output file data


The report will contain the following output data, divided between stratification columns and data
columns.


### Stratification columns

| Parameter | Data type | Description |
| --- | --- | --- |
| `Time` | integer | The day of the simulation that the data was collected. |
| `NodeID` | integer | The External ID of the node for the data in the row in the report. |

### Data columns

| Parameter | Data type | Description |
| --- | --- | --- |
| `NodePopulation` | integer | The population of the node that has the indicated intervention. |
| `InterventionName` | string | The name of the intervention. This can be custom using the **Intervention_Name** parameter of the intervention or it will be the default name which is usually just the class name. |
| `FractionHas` | float | For individual-level interventions, this will be the fraction of the people in the node that have at least one of the indicated interventions. For node-level interventions, this will almost always be 1.0 since most of those interventions only allow one per node. |
| `AvgNumberOfInterventions` | float | For individuals that have the intervention, this will be the average number of instances of that intervention per person. For nodes that have the intervention, this will be the number of instances of that intervention in the node - it is a count and not an average. |
| `AvgEfficacy-Attracting` | float | For interventions that have an attracting effect like **HumanHostSeekingTrap**, individual-level interventions will have the average attracting efficacy for the people that have this intervention in this node during this time step. Node-level interventions will have the attracting efficacy of the intervention. |
| `AvgEfficacy-Repelling` | float | For interventions that have a repelling effect like **IRSHousingModification**, individual-level interventions will have the average repelling efficacy for the people that have this intervention in this node during this time step. Node-level interventions will have the repelling efficacy of the intervention. |
| `AvgEfficacy-Blocking` | float | For interventions that have a blocking effect like **SimpleBednet**, individual-level interventions will have the average blocking efficacy for the people that have this intervention in this node during this time step. Node-level interventions will have the blocking efficacy of the intervention. |
| `AvgEfficacy-Killing` | float | For interventions that have a killing effect like **SimpleBednet**, individual-level interventions will have the average killing efficacy for the people that have this intervention in this node during this time step. Node-level interventions will have the killing efficacy of the intervention. |
| `AvgEfficacy-Usage` | float | For interventions that have a usage effect like **UsageDependentBednet**, individual-level interventions will have the average usage efficacy for the people that have this intervention in this node during this time step. There are no node-level interventions with this effect at this time. |
| `AvgEfficacy-AcquisitionBlocking` | float | For interventions that have an acquisition blocking effect like **SimpleVaccine**, individual-level interventions will have the average acquisition blocking efficacy for the people that have this intervention in this node during this time step. There are no node-level interventions with this effect at this time. |
| `AvgEfficacy-TransmissionBlocking` | float | For interventions that have a transmission blocking effect like **SimpleVaccine**, individual-level interventions will have the average transmission blocking efficacy for the people that have this intervention in this node during this time step. There are no node-level interventions with this effect at this time. |
| `AvgEfficacy-MortalityBlocking` | float | For interventions that have a mortality blocking effect like **SimpleVaccine**, individual-level interventions will have the average mortality blocking efficacy for the people that have this intervention in this node during this time step. There are no node-level interventions with this effect at this time. |
| `DrugConcentration` | float | For drug interventions, this will be the concentration of the drugs involved in the intervention averaged over the people in the node with the drug during this time step. For drug interventions like **MultiPackComboDrug**, each person will contribute the sum of the concentrations of the drugs they have taken from the pack. There are no node-level interventions with this effect at this time. |

## Example


The following is an example of ReportInterventionPopAvg.csv.

| Time | NodeID | NodePopulation | InterventionName | FractionHas | AvgNumberOfInterventions | AvgEfficacy-Attracting | AvgEfficacy-Repelling | AvgEfficacy-Blocking | AvgEfficacy-Killing | AvgEfficacy-Usage | AvgEfficacy-AcquisitionBlocking | AvgEfficacy-TransmissionBlocking | AvgEfficacy-MortalityBlocking | DrugConcentration |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 268 | 2 | 1000 | AdherentDrug-Piperaquine | 0.008 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.110735 |
| 268 | 2 | 1000 | AntimalarialDrug | 0.097 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8.5187e-05 |
| 268 | 2 | 1000 | ArtificialDiet | 1 | 1 | 0.5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 268 | 2 | 1000 | HumanHostSeekingTrap | 0.098 | 1 | 0 | 0 | 0 | 0.3 | 0 | 0 | 0 | 0 | 0 |
| 268 | 2 | 1000 | Ivermectin | 0.092 | 1 | 0 | 0 | 0 | 0.3 | 0 | 0 | 0 | 0 | 0 |
| 268 | 2 | 1000 | Larvicides | 1 | 1 | 0 | 0 | 0 | 0.0681233 | 0 | 0 | 0 | 0 | 0 |
| 268 | 2 | 1000 | SimpleBednet | 0.206 | 1 | 0 | 0.1 | 0 | 0.450683 | 1 | 0 | 0 | 0 | 0 |
| 268 | 2 | 1000 | SimpleIndividualRepellent | 0.102 | 1 | 0 | 0.2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 268 | 2 | 1000 | SpaceSpraying | 1 | 1 | 0 | 0 | 0 | 0.075 | 0 | 0 | 0 | 0 | 0 |
| 268 | 2 | 1000 | SpatialRepellentHousingModification | 0.092 | 1 | 0 | 0.3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 268 | 2 | 1000 | UsageDependentBednet | 0.086 | 1 | 0 | 0.1 | 1 | 0.5 | 1 | 0 | 0 | 0 | 0 |
| 268 | 1 | 1000 | AdherentDrug-Piperaquine | 0.006 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.104079 |
| 268 | 1 | 1000 | AntimalarialDrug | 0.1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8.50645e-05 |
| 268 | 1 | 1000 | ArtificialDiet | 1 | 1 | 0.5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 268 | 1 | 1000 | HumanHostSeekingTrap | 0.112 | 1 | 0 | 0 | 0 | 0.3 | 0 | 0 | 0 | 0 | 0 |
| 268 | 1 | 1000 | Ivermectin | 0.106 | 1 | 0 | 0 | 0 | 0.3 | 0 | 0 | 0 | 0 | 0 |
| 268 | 1 | 1000 | Larvicides | 1 | 1 | 0 | 0 | 0 | 0.0681233 | 0 | 0 | 0 | 0 | 0 |
| 268 | 1 | 1000 | SimpleBednet | 0.193 | 1 | 0 | 0.1 | 0 | 0.450683 | 1 | 0 | 0 | 0 | 0 |
| 268 | 1 | 1000 | SimpleIndividualRepellent | 0.09 | 1 | 0 | 0.2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 268 | 1 | 1000 | SpaceSpraying | 1 | 1 | 0 | 0 | 0 | 0.075 | 0 | 0 | 0 | 0 | 0 |
| 268 | 1 | 1000 | SpatialRepellentHousingModification | 0.101 | 1 | 0 | 0.3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 268 | 1 | 1000 | UsageDependentBednet | 0.091 | 1 | 0 | 0.1 | 1 | 0.5 | 1 | 0 | 0 | 0 | 0 |
| 269 | 2 | 1000 | AdherentDrug-Piperaquine | 0.008 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.108067 |
| 269 | 2 | 1000 | AntimalarialDrug | 0.097 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6.97451e-05 |
| 269 | 2 | 1000 | ArtificialDiet | 1 | 1 | 0.5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 269 | 2 | 1000 | HumanHostSeekingTrap | 0.098 | 1 | 0 | 0 | 0 | 0.3 | 0 | 0 | 0 | 0 | 0 |
| 269 | 2 | 1000 | Ivermectin | 0.092 | 1 | 0 | 0 | 0 | 0.3 | 0 | 0 | 0 | 0 | 0 |
| 269 | 2 | 1000 | Larvicides | 1 | 1 | 0 | 0 | 0 | 0.0667608 | 0 | 0 | 0 | 0 | 0 |
| 269 | 2 | 1000 | SimpleBednet | 0.206 | 1 | 0 | 0.1 | 0 | 0.448428 | 1 | 0 | 0 | 0 | 0 |
| 269 | 2 | 1000 | SimpleIndividualRepellent | 0.102 | 1 | 0 | 0.2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 269 | 2 | 1000 | SpaceSpraying | 1 | 1 | 0 | 0 | 0 | 0.075 | 0 | 0 | 0 | 0 | 0 |
| 269 | 2 | 1000 | SpatialRepellentHousingModification | 0.092 | 1 | 0 | 0.3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 269 | 1 | 1000 | AdherentDrug-Piperaquine | 0.006 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.101571 |
| 269 | 1 | 1000 | AntimalarialDrug | 0.1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6.96448e-05 |
| 269 | 1 | 1000 | ArtificialDiet | 1 | 1 | 0.5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 269 | 1 | 1000 | HumanHostSeekingTrap | 0.112 | 1 | 0 | 0 | 0 | 0.3 | 0 | 0 | 0 | 0 | 0 |
| 269 | 1 | 1000 | Ivermectin | 0.106 | 1 | 0 | 0 | 0 | 0.3 | 0 | 0 | 0 | 0 | 0 |
| 269 | 1 | 1000 | Larvicides | 1 | 1 | 0 | 0 | 0 | 0.0667608 | 0 | 0 | 0 | 0 | 0 |
| 269 | 1 | 1000 | SimpleBednet | 0.193 | 1 | 0 | 0.1 | 0 | 0.448428 | 1 | 0 | 0 | 0 | 0 |
| 269 | 1 | 1000 | SimpleIndividualRepellent | 0.09 | 1 | 0 | 0.2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 269 | 1 | 1000 | SpaceSpraying | 1 | 1 | 0 | 0 | 0 | 0.075 | 0 | 0 | 0 | 0 | 0 |
| 269 | 1 | 1000 | SpatialRepellentHousingModification | 0.101 | 1 | 0 | 0.3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
