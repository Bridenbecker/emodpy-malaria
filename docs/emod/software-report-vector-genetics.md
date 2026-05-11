# ReportVectorGenetics


The vector genetics report is a CSV-formatted report that collects information on how many vectors
of each genome/allele combination exist at each time, node, and vector state. Information can only
be collected on one species per report.




## Configuration


To generate this report, the following parameters must be configured in the custom_reports.json file:

{{ read_csv('../csv/report-vector-genetics.csv', keep_default_na=False) }}

The following is an example of an input file for this report:

```json
{
    "Reports": [
        {
            "class": "ReportVectorGenetics",
            "Species": "arabiensis2",
            "Gender": "VECTOR_FEMALE",
            "Stratify_By": "GENOME",
            "Start_Day": 365,
            "End_Day": 465,
            "Filename_Suffix": "Node1",
            "Node_IDs_Of_Interest": [1]
        },
        {
            "class": "ReportVectorGenetics",
            "Species": "arabiensis2",
            "Gender": "VECTOR_BOTH_GENDERS",
            "Stratify_By": "ALLELE_FREQ",
            "Alleles_For_Stratification": ["a0", "a1", "b0", "b1"],
            "Filename_Suffix": "Test67"
        },
        {
            "class": "ReportVectorGenetics",
            "Species": "arabiensis2",
            "Gender": "VECTOR_FEMALE",
            "Stratify_By": "ALLELE",
            "Allele_Combinations_For_Stratification": [["a0", "b0"], ["a1", "b1"]],
            "Include_Vector_State_Columns": 0
        },
        {
            "class": "ReportVectorGenetics",
            "Species": "arabiensis2",
            "Stratify_By": "SPECIFIC_GENOME",
            "Gender": "VECTOR_FEMALE",
            "Specific_Genome_Combinations_For_Stratification": [
                {"Allele_Combination": [["X", "X"], ["a0", "*"], ["b1", "b0"]]},
                {"Allele_Combination": [["X", "X"], ["a1", "a0"], ["b0", "*"]]},
                {"Allele_Combination": [["X", "X"], ["a1", "*"], ["b1", "b0"]]},
                {"Allele_Combination": [["X", "X"], ["a1", "a0"], ["b1", "*"]]}
            ],
            "Combine_Similar_Genomes": 1,
            "Include_Vector_State_Columns": 1
        }
    ],
    "Use_Defaults": 1
}
```

## Output file data


The output report will contain the following information.

### Stratification columns


| Parameter | Data type | Description |
| --- | --- | --- |
| `Time` | integer | The day of the simulation that the data was collected. |
| `NodeID` | integer | The External ID of the node that the data is being collected for. |
| `Alleles` | string | If **Stratify_By** = ALLELE, then the column will be all of the possible alleles plus the values in **Allele_Combinations_For_Stratification**. |
| `Genome` | string | If **Stratify_By** = GENOME or SPECIFIC_GENOME, then this is the 'Genome' column and for each time and NodeID, the column will contain the possible combinations of genomes. |

### Data columns


| Parameter | Data type | Description |
| --- | --- | --- |
| `VectorPopulation` | integer | If **Gender** = VECTOR_BOTH_GENDERS or VECTOR_FEMALE, then this column will contain the number of female vectors that are in the states STATE_INFECTIOUS, STATE_INFECTED, or STATE_ADULT. |
| `STATE_INFECTIOUS` | integer | If **Gender** is VECTOR_BOTH_GENDERS or VECTOR_FEMALE, then this column will contain the number of female vectors that are in this state. |
| `STATE_INFECTED` | integer | If **Gender** is VECTOR_BOTH_GENDERS or VECTOR_FEMALE, then this column will contain the number of female vectors that are in this state. |
| `STATE_ADULT` | integer | If **Gender** is VECTOR_BOTH_GENDERS or VECTOR_FEMALE, then this column will contain the number of female vectors that are in this state. |
| `STATE_MALE` | integer | If **Gender** is VECTOR_BOTH_GENDERS or VECTOR_MALE, then this column will contain the number of mature male vectors. |
| `STATE_IMMATURE` | integer | This column contains the number of vectors (male and female) in the 'immature' state. |
| `STATE_LARVA` | integer | This column contains the number of larva (male and female). |
| `STATE_EGG` | integer | This column contains the number of eggs (male and female). |
| `VectorPopulationNumDied` | integer | If **Include_Death_By_State_Columns** is true and **Gender** = VECTOR_BOTH_GENDERS or VECTOR_FEMALE, then this column will contain the number of female vectors that died and were in states STATE_INFECTIOUS, STATE_INFECTED, or STATE_ADULT. |
| `InfectiousNumDied` | integer | If **Include_Death_By_State_Columns** is true, **Include_Vector_State_Columns** is true, and **Gender** = VECTOR_BOTH_GENDERS or VECTOR_FEMALE, then this column will contain the number of infectious, mature, female vectors that died during this time step. |
| `InfectedNumDied` | integer | If **Include_Death_By_State_Columns** is true, **Include_Vector_State_Columns** is true, and **Gender** = VECTOR_BOTH_GENDERS or VECTOR_FEMALE, then this column will contain the number of infected, mature, female vectors that died during this time step. |
| `AdultsNumDied` | integer | If **Include_Death_By_State_Columns** is true, **Include_Vector_State_Columns** is true, and **Gender** = VECTOR_BOTH_GENDERS or VECTOR_FEMALE, then this column will contain the number of mature female vectors that are neither infected or infectious that died during this time step. |
| `MaleNumDied` | integer | If **Include_Death_By_State_Columns** is true, **Include_Vector_State_Columns** is true, and **Gender** = VECTOR_BOTH_GENDERS or VECTOR_MALE, then this column will contain the number of mature male vectors that died during this time step. |
| `VectorPopulationAvgAgeAtDeath` | float | If **Include_Death_By_State_Columns** is true and **Gender** = VECTOR_BOTH_GENDERS or VECTOR_FEMALE, then this column will contain the average age (in days) of the infectious, mature, female vectors that died during this time step. |
| `InfectiousAvgAgeAtDeath` | float | If **Include_Death_By_State_Columns** is true, **Include_Vector_State_Columns** is true, and **Gender** = VECTOR_BOTH_GENDERS or VECTOR_FEMALE, then this column will contain the average age (in days) of the infectious, mature, female vectors that died during this time step. |
| `InfectedAvgAgeAtDeath` | float | If **Include_Death_By_State_Columns** is true, **Include_Vector_State_Columns** is true, and **Gender** = VECTOR_BOTH_GENDERS or VECTOR_FEMALE, then this column will contain the average age (in days) of the infected, mature, female vectors that died during this time step. |
| `AdultsAvgAgeAtDeath` | float | If **Include_Death_By_State_Columns** is true, **Include_Vector_State_Columns** is true, and **Gender** = VECTOR_BOTH_GENDERS or VECTOR_FEMALE, then this column will contain the average age (in days) of the mature, female vectors that are neither infected or infectious that died during this time step. |
| `MaleAvgAgeAtDeath` | float | If **Include_Death_By_State_Columns** is true, **Include_Vector_State_Columns** is true, and **Gender** = VECTOR_BOTH_GENDERS or VECTOR_MALE, then this column will contain the average age (in days) of the mature male vectors that died during this time step. |

## Example


The following are examples of ReportVectorGenetics.csv files.  The Death By State columns are not included in the examples.

This table is stratified by genome and female vectors.

{{ read_csv("csv/report-vector-genetics-genome-female.csv", keep_default_na=False) }}

This table is stratified by genome and male vectors.

{{ read_csv("csv/report-vector-genetics-genome-male.csv", keep_default_na=False) }}

This table is stratified by allele and female vectors, with vector state columns included.

{{ read_csv("csv/report-vector-genetics-allele-female.csv", keep_default_na=False) }}
