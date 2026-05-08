import sys, io
# Ensure UTF-8 stdout (handles Windows cp1252 console)
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

"""
EMOD Parameter Documentation Audit Script
Compares schema.json parameter names against docs/csv/ parameter tables.

Schema structure (top-level keys):
  schema['config']        : dict of group_name -> dict of param_name -> param_def
                            These are the top-level config.json parameters.
  schema['interventions'] : {'Events': ['idmAbstractType:CampaignEvent'], ...}
                            Campaign event classes live in idmTypes.
  schema['reports']       : {'Reports': ['idmType:IReport'], ...}
                            Report classes live in idmTypes.
  schema['idmTypes']      : all named types referenced from the above sections:
    idmAbstractType:Intervention
      idmAbstractType:IndividualIntervention : class_name -> param_name -> param_def
      idmAbstractType:NodeIntervention       : class_name -> param_name -> param_def
    idmAbstractType:EventCoordinator         : class_name -> param_name -> param_def
    idmAbstractType:CampaignEvent            : class_name -> param_name -> param_def
    idmAbstractType:NodeSet                  : class_name -> param_name -> param_def
    idmType:IReport                          : report_class_name -> param_name -> param_def
    idmType:*                                : named sub-object types (nested params)

Nested params: when a param has item_type or type referencing an idmType:*, those
sub-object params are NOT top-level and are missed by a flat scan. The nested
traversal below finds them all.
"""

import json
import csv
import os
import re
from pathlib import Path
from collections import defaultdict


# ── Helpers for nested-schema traversal ──────────────────────────────────────

def idmtype_refs(pdef):
    """Return all idmType:* keys referenced in a param def's item_type or type fields."""
    refs = []
    for field in ("item_type", "type"):
        val = pdef.get(field, "")
        for m in re.finditer(r"idmType:\w+", str(val)):
            t = m.group()
            if t not in refs:
                refs.append(t)
    return refs

def collect_nested(idm, type_key, result, visited):
    """
    Recursively collect params reachable inside an idmType:* object.
    Handles both direct param dicts (have a 'type' key) and sub-class dicts
    (e.g. idmType:WaningEffect whose values are class defs, not param defs).
    result: dict  param_name -> set of idmType_keys where it appears nested.
    visited: shared set to avoid cycles.
    """
    if type_key in visited:
        return
    visited.add(type_key)
    type_def = idm.get(type_key)
    if not isinstance(type_def, dict):
        return
    for key, val in type_def.items():
        if not isinstance(val, dict) or key in ("class", "Sim_Types"):
            continue
        if "type" in val:
            # val is a direct param definition
            result.setdefault(key, set()).add(type_key)
            for ref in idmtype_refs(val):
                collect_nested(idm, ref, result, visited)
        else:
            # val is a sub-class definition (key is a class name, val holds its params)
            for pname, pdef in val.items():
                if isinstance(pdef, dict) and "type" in pdef:
                    result.setdefault(pname, set()).add(type_key)
                    for ref in idmtype_refs(pdef):
                        collect_nested(idm, ref, result, visited)

def build_nested_params(schema, idm):
    """
    Walk config, interventions, and event coordinators to find all params that
    live inside idmType:* sub-objects (not visible to a flat schema scan).
    Returns dict: param_name -> set of idmType_keys where it is nested.
    """
    nested = {}

    def walk_class_params(class_params):
        """For each param with an idmType ref, collect its nested params."""
        if not isinstance(class_params, dict):
            return
        for pname, pdef in class_params.items():
            if not isinstance(pdef, dict) or pname in ("class", "Sim_Types"):
                continue
            for ref in idmtype_refs(pdef):
                collect_nested(idm, ref, nested, set())

    # 1. Config groups — params like Vector_Species_Params, Insecticides, Malaria_Drug_Params
    for group_content in schema.get("config", {}).values():
        if isinstance(group_content, dict):
            walk_class_params(group_content)

    # 2. Individual and Node interventions
    intervention = idm.get("idmAbstractType:Intervention", {})
    for abs_type, class_dict in intervention.items():
        if isinstance(class_dict, dict):
            for class_params in class_dict.values():
                walk_class_params(class_params)

    # 3. Event coordinators
    for class_params in idm.get("idmAbstractType:EventCoordinator", {}).values():
        walk_class_params(class_params)

    # 4. Campaign events and node sets
    for abs_key in ("idmAbstractType:CampaignEvent", "idmAbstractType:NodeSet"):
        for class_params in idm.get(abs_key, {}).values():
            walk_class_params(class_params)

    return nested


# ── Paths ────────────────────────────────────────────────────────────────────
SCHEMA_PATH = Path("C:/work/dev/emodpy-dev/emodpy-malaria-1/schema.json")
CSV_DIR     = Path("C:/work/dev/emodpy-dev/emodpy-malaria-1/docs/csv")

# ── 1. Parse schema.json ─────────────────────────────────────────────────────
print("Loading schema.json …")
with open(SCHEMA_PATH, encoding="utf-8") as f:
    schema = json.load(f)

idm = schema.get("idmTypes", {})

def params_from_dict(d):
    """Return param names from a flat dict of {param_name: param_def}."""
    return {k for k, v in d.items()
            if isinstance(v, dict) and k not in ("class", "Sim_Types")
            and not k.startswith("logLevel_")}

# --- config params ---
schema_config_params = set()
for group_name, group_content in schema.get("config", {}).items():
    if isinstance(group_content, dict):
        schema_config_params.update(params_from_dict(group_content))

print(f"  Config params in schema          : {len(schema_config_params)}")

# --- campaign / intervention params ---
schema_campaign_params = set()

# Individual interventions
indiv_iv = idm.get("idmAbstractType:Intervention", {}).get("idmAbstractType:IndividualIntervention", {})
for class_name, class_params in indiv_iv.items():
    if isinstance(class_params, dict):
        schema_campaign_params.update(params_from_dict(class_params))

# Node interventions
node_iv = idm.get("idmAbstractType:Intervention", {}).get("idmAbstractType:NodeIntervention", {})
for class_name, class_params in node_iv.items():
    if isinstance(class_params, dict):
        schema_campaign_params.update(params_from_dict(class_params))

# Event coordinators
for ec_group in idm.get("idmAbstractType:EventCoordinator", {}).values():
    if isinstance(ec_group, dict):
        schema_campaign_params.update(params_from_dict(ec_group))

# Campaign event (CampaignEvent, CampaignEventByYear)
for ce_name, ce_params in idm.get("idmAbstractType:CampaignEvent", {}).items():
    if isinstance(ce_params, dict):
        schema_campaign_params.update(params_from_dict(ce_params))

# NodeSets
for ns_name, ns_params in idm.get("idmAbstractType:NodeSet", {}).items():
    if isinstance(ns_params, dict):
        schema_campaign_params.update(params_from_dict(ns_params))

# Waning effects and other idmType entries (sub-objects used inside interventions)
for type_key, type_val in idm.items():
    if type_key.startswith("idmType:") and isinstance(type_val, dict):
        for inner_key, inner_val in type_val.items():
            if isinstance(inner_val, dict):
                schema_campaign_params.update(params_from_dict(inner_val))
                for sub_key, sub_val in inner_val.items():
                    if isinstance(sub_val, dict) and "type" in sub_val:
                        schema_campaign_params.add(sub_key)

print(f"  Campaign/intervention params      : {len(schema_campaign_params)}")

# --- report params ---
schema_report_params = set()
ireport = idm.get("idmType:IReport", {})
schema_report_classes = set(ireport.keys())
for class_name, class_params in ireport.items():
    if isinstance(class_params, dict):
        schema_report_params.update(params_from_dict(class_params))

print(f"  Report params in schema           : {len(schema_report_params)}")
print(f"  Report classes                    : {sorted(schema_report_classes)}")
print()

# All schema params combined
all_schema_params = schema_config_params | schema_campaign_params | schema_report_params

# ── 2. Build nested params from schema traversal ──────────────────────────────
print("Building nested params map …")
nested_params = build_nested_params(schema, idm)
print(f"  Nested params found               : {len(nested_params)}")
print()

# ── 3. Read all CSV files ─────────────────────────────────────────────────────
print("Reading CSV files …")

csv_params_by_file   = defaultdict(set)  # filename -> set of param names
csv_params_all       = set()             # all param names across all CSVs
csv_params_config    = set()
csv_params_campaign  = set()
csv_params_demo      = set()
csv_params_report    = set()
csv_params_other     = set()

report_csv_files     = []  # track report CSVs that have column headers

for csv_file in sorted(CSV_DIR.glob("*.csv")):
    name = csv_file.name

    # Determine category by prefix
    if name.startswith("config-"):
        category = "config"
    elif name.startswith("campaign-"):
        category = "campaign"
    elif name.startswith("demo-"):
        category = "demo"
    elif name.startswith("report-"):
        category = "report"
    else:
        category = "other"

    with open(csv_file, encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        continue

    header = rows[0]
    if not header:
        continue

    first_col = header[0].strip()

    if first_col.lower() == "parameter":
        data_rows = rows[1:]
    else:
        report_csv_files.append(name)
        data_rows = []

    for row in data_rows:
        if not row:
            continue
        param = row[0].strip()
        if param:
            csv_params_by_file[name].add(param)
            csv_params_all.add(param)
            if category == "config":
                csv_params_config.add(param)
            elif category == "campaign":
                csv_params_campaign.add(param)
            elif category == "demo":
                csv_params_demo.add(param)
            elif category == "report":
                csv_params_report.add(param)
            else:
                csv_params_other.add(param)

print(f"  Config CSV params                 : {len(csv_params_config)}")
print(f"  Campaign CSV params               : {len(csv_params_campaign)}")
print(f"  Demo CSV params                   : {len(csv_params_demo)}")
print(f"  Report CSV params                 : {len(csv_params_report)}")
print(f"  Total unique CSV params           : {len(csv_params_all)}")
if report_csv_files:
    print(f"  NOTE: These CSV files appear to be raw data (no Parameter header), skipped:")
    for f in report_csv_files:
        print(f"    {f}")
print()

# ── 4. Compute differences ────────────────────────────────────────────────────

# Parameters present in the schema but not applicable to malaria simulations.
NOT_MALARIA_PARAMS = {
    # Base_Mortality is read in Infection::Update() but InfectionMalaria::Update()
    # overrides that method entirely without calling the parent, so the param
    # has no effect in malaria simulations.
    "Base_Mortality",

    # SimulationConfig::SetFixedParameters() explicitly forces these to 0 for
    # MALARIA_SIM. The C++ comment reads "not used in Malaria".
    "Enable_Susceptibility_Scaling",
    "Enable_Immune_Decay",
    # These two depend on Enable_Susceptibility_Scaling, which is forced to 0,
    # so they are also unreachable in malaria simulations.
    "Susceptibility_Scaling_Rate",
    "Susceptibility_Scaling_Type",

    # Infectivity_* params are read and applied in Node::updateInfectivity().
    # NodeVector::updateInfectivity() completely overrides Node::updateInfectivity()
    # without calling the parent. NodeMalaria inherits from NodeVector and does not
    # override updateInfectivity(), so NodeMalaria always uses NodeVector's version.
    # None of these params have any effect in malaria simulations.
    "Infectivity_Scale_Type",
    "Infectivity_Sinusoidal_Forcing_Amplitude",
    "Infectivity_Sinusoidal_Forcing_Phase",
    "Infectivity_Exponential_Baseline",
    "Infectivity_Exponential_Delay",
    "Infectivity_Exponential_Rate",
    "Infectivity_Boxcar_Forcing_Amplitude",
    "Infectivity_Boxcar_Forcing_Start_Time",
    "Infectivity_Boxcar_Forcing_End_Time",
}

# Parameters that appear in the schema as internal metadata rather than
# user-configurable parameters.
SCHEMA_INTERNAL_PARAMS = {
    "depends-on",
}

# Parameters documented in prose (MD tables) rather than CSV files.
DOCUMENTED_IN_PROSE = {
    "Parasite_Genetics":                                       "malaria-model-fpg.md",
    "IP_Key_Value":                                            "parameter-campaign-targeting-config.md",
    "Is_Equal_To":                                             "parameter-campaign-targeting-config.md",
    "Logic":                                                   "parameter-campaign-targeting-config.md",
    "Inset_Chart_Has_IP":                                      "software-report-inset-chart.md",
    "Inset_Chart_Has_Interventions":                           "software-report-inset-chart.md",
    "Inset_Chart_Include_Pregnancies":                         "software-report-inset-chart.md",
    "Inset_Chart_Reporting_Include_30Day_Avg_Infection_Duration": "software-report-inset-chart.md",
    "Enable_Continuous_Log_Flushing":                          "software-error-logging.md",
    "Enable_Log_Throttling":                                   "software-error-logging.md",
    "Enable_Warnings_Are_Fatal":                               "software-error-logging.md",
    "Serialization_Mask_Node_Read":                            "software-serializing-create.md",
    "Serialization_Mask_Node_Write":                           "software-serializing-create.md",
    "Serialization_Max_Humans_Per_Collection":                 "software-serializing-create.md",
    "Serialization_Precision":                                 "software-serializing-create.md",
    "Serialized_Population_Reading_Type":                      "software-serializing-create.md",
    "Serialized_Population_Writing_Type":                      "software-serializing-create.md",
}

# Remove exclusions from schema sets before diffing
all_schema_params -= NOT_MALARIA_PARAMS
schema_config_params  -= NOT_MALARIA_PARAMS
schema_campaign_params -= NOT_MALARIA_PARAMS
schema_report_params  -= NOT_MALARIA_PARAMS

prose_params = set(DOCUMENTED_IN_PROSE.keys())
all_schema_params -= prose_params
schema_config_params  -= prose_params
schema_campaign_params -= prose_params
schema_report_params  -= prose_params

all_schema_params -= SCHEMA_INTERNAL_PARAMS
schema_config_params  -= SCHEMA_INTERNAL_PARAMS
schema_campaign_params -= SCHEMA_INTERNAL_PARAMS
schema_report_params  -= SCHEMA_INTERNAL_PARAMS

# Parameters in CSVs but NOT in schema
csv_only = csv_params_all - all_schema_params

# Parameters in schema but NOT in any CSV
schema_only = all_schema_params - csv_params_all

# In both
in_both = all_schema_params & csv_params_all

# Split schema-only into report-related vs. other
schema_only_report   = schema_only & schema_report_params
schema_only_config   = schema_only & schema_config_params
schema_only_campaign = schema_only & schema_campaign_params
schema_only_other    = schema_only - schema_only_report - schema_only_config - schema_only_campaign

# Demographics params — in demo-* CSVs but not in schema (expected)
csv_only_demo     = csv_only & csv_params_demo
csv_only_non_demo = csv_only - csv_only_demo

# Nested params — in CSVs but nested inside idmType:* objects in the schema
# (not visible to flat scan; these are valid, not stale)
csv_only_nested     = csv_only_non_demo & set(nested_params.keys())
csv_only_non_demo  -= csv_only_nested

# ── 5. Print results ──────────────────────────────────────────────────────────

SEPARATOR = "=" * 72

print(SEPARATOR)
print("AUDIT RESULTS")
print(SEPARATOR)
print()

print(f"Parameters in BOTH schema and CSVs  : {len(in_both)}")
print(f"Parameters in CSVs only             : {len(csv_only_non_demo)}")
print(f"  (+ {len(csv_only_demo)} demographics params not yet in schema)")
print(f"  (+ {len(csv_only_nested)} nested in idmType:* objects — documented, not stale)")
print(f"Parameters in schema only           : {len(schema_only)}")
print(f"  of which: report params           : {len(schema_only_report)}")
print(f"  of which: config params only      : {len(schema_only_config - schema_only_report)}")
print(f"  of which: campaign params only    : {len(schema_only_campaign - schema_only_report)}")
print(f"  of which: overlap/other           : {len(schema_only_other)}")
print()

# ── CSV-only (possibly stale) ─────────────────────────────────────────────────
print(SEPARATOR)
print(f"CSV-ONLY PARAMETERS ({len(csv_only_non_demo)}) — possibly outdated / renamed / removed")
print(SEPARATOR)
for p in sorted(csv_only_non_demo):
    files = [f for f, ps in csv_params_by_file.items() if p in ps]
    print(f"  {p:<60}  [{', '.join(sorted(files))}]")
print()

# ── CSV params nested in idmType:* objects ────────────────────────────────────
print(SEPARATOR)
print(f"CSV PARAMS NESTED IN SCHEMA ({len(csv_only_nested)}) — valid but inside idmType:* sub-objects")
print(SEPARATOR)
for p in sorted(csv_only_nested):
    type_keys = sorted(nested_params.get(p, set()))
    print(f"  {p:<60}  [{', '.join(type_keys)}]")
print()

# ── Schema-only: report ───────────────────────────────────────────────────────
print(SEPARATOR)
print(f"SCHEMA-ONLY REPORT PARAMETERS ({len(schema_only_report)}) — documented in prose (software-report*.md)")
print(SEPARATOR)
for p in sorted(schema_only_report):
    classes = [cls for cls, prms in ireport.items()
               if isinstance(prms, dict) and p in prms]
    print(f"  {p:<60}  [used by: {', '.join(sorted(classes))}]")
print()

# ── Schema-only: config ───────────────────────────────────────────────────────
schema_only_config_non_report = schema_only_config - schema_only_report
print(SEPARATOR)
print(f"SCHEMA-ONLY CONFIG PARAMETERS ({len(schema_only_config_non_report)}) — possibly undocumented")
print(SEPARATOR)
for p in sorted(schema_only_config_non_report):
    print(f"  {p}")
print()

# ── Schema-only: campaign ─────────────────────────────────────────────────────
schema_only_campaign_non_report = schema_only_campaign - schema_only_report
print(SEPARATOR)
print(f"SCHEMA-ONLY CAMPAIGN PARAMETERS ({len(schema_only_campaign_non_report)}) — possibly undocumented")
print(SEPARATOR)
for p in sorted(schema_only_campaign_non_report):
    print(f"  {p}")
print()

# ── Schema-only: other ────────────────────────────────────────────────────────
print(SEPARATOR)
print(f"SCHEMA-ONLY OTHER PARAMETERS ({len(schema_only_other)}) — overlap between config/campaign categories")
print(SEPARATOR)
for p in sorted(schema_only_other):
    in_cfg = p in schema_config_params
    in_cmp = p in schema_campaign_params
    tag = []
    if in_cfg: tag.append("config")
    if in_cmp: tag.append("campaign")
    print(f"  {p:<60}  [{', '.join(tag) if tag else 'unknown'}]")
print()

# ── Demographics CSV-only ─────────────────────────────────────────────────────
print(SEPARATOR)
print(f"DEMOGRAPHICS CSV-ONLY PARAMETERS ({len(csv_only_demo)}) — not in schema (demographics.json, not config.json)")
print(SEPARATOR)
for p in sorted(csv_only_demo):
    files = [f for f, ps in csv_params_by_file.items() if p in ps]
    print(f"  {p:<60}  [{', '.join(sorted(files))}]")
print()

# ── Excluded: prose-documented ────────────────────────────────────────────────
print(SEPARATOR)
print(f"EXCLUDED — DOCUMENTED IN PROSE ({len(DOCUMENTED_IN_PROSE)}) — in MD tables, not CSVs")
print(SEPARATOR)
by_page = defaultdict(list)
for param, page in DOCUMENTED_IN_PROSE.items():
    by_page[page].append(param)
for page in sorted(by_page):
    print(f"  {page}:")
    for p in sorted(by_page[page]):
        print(f"    {p}")
print()

# ── Excluded: not applicable to malaria ───────────────────────────────────────
print(SEPARATOR)
print(f"EXCLUDED — NOT APPLICABLE TO MALARIA ({len(NOT_MALARIA_PARAMS)})")
print(SEPARATOR)
for p in sorted(NOT_MALARIA_PARAMS):
    print(f"  {p}")
print()

# ── Excluded: internal schema metadata ────────────────────────────────────────
print(SEPARATOR)
print(f"EXCLUDED — INTERNAL SCHEMA METADATA ({len(SCHEMA_INTERNAL_PARAMS)})")
print(SEPARATOR)
for p in sorted(SCHEMA_INTERNAL_PARAMS):
    print(f"  {p}")
print()

# ── Summary table ─────────────────────────────────────────────────────────────
print(SEPARATOR)
print("SUMMARY")
print(SEPARATOR)
print(f"  Total schema params (all sections)  : {len(all_schema_params)}")
print(f"    Config                            : {len(schema_config_params)}")
print(f"    Campaign/Intervention             : {len(schema_campaign_params)}")
print(f"    Report                            : {len(schema_report_params)}")
print(f"  Excluded (prose-documented)         : {len(DOCUMENTED_IN_PROSE)}")
print(f"  Excluded (not malaria)              : {len(NOT_MALARIA_PARAMS)}")
print(f"  Excluded (internal schema)          : {len(SCHEMA_INTERNAL_PARAMS)}")
print(f"  Total CSV params (unique)           : {len(csv_params_all)}")
print(f"    config-* CSVs                     : {len(csv_params_config)}")
print(f"    campaign-* CSVs                   : {len(csv_params_campaign)}")
print(f"    demo-* CSVs                       : {len(csv_params_demo)}")
print(f"    report-* CSVs                     : {len(csv_params_report)}")
print(f"  In both (flat schema match)         : {len(in_both)}")
print(f"  CSV nested in idmType:* objects     : {len(csv_only_nested)}")
print(f"  CSV-only (possibly stale)           : {len(csv_only_non_demo)}")
print(f"  CSV-only (demographics)             : {len(csv_only_demo)}")
print(f"  Schema-only (possibly undocumented) : {len(schema_only)}")
print(f"    Report params (expected)          : {len(schema_only_report)}")
print(f"    Config undocumented               : {len(schema_only_config_non_report)}")
print(f"    Campaign undocumented             : {len(schema_only_campaign_non_report)}")
print(f"    Other/overlap                     : {len(schema_only_other)}")
