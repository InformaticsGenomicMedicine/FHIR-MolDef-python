import json
from pathlib import Path

import pandas as pd
from ga4gh.vrs.extras.translator import AlleleTranslator
from translators.vrs_fhir_translator import VrsFhirAlleleTranslator

from api.seqrepo import SeqRepoAPI

def load_data(input_file, **read_kwargs):
    p = Path(input_file)

    if not p.exists():
        raise FileNotFoundError(f"No such file: {p}")
    
    ext = p.suffix.lower().lstrip(".")

    if ext == "tsv":
        read_kwargs.setdefault("sep", "\t")
        df = pd.read_csv(p, **read_kwargs)
    
    elif ext in {"csv", "txt"}:
        read_kwargs.setdefault("sep", ",")
        df = pd.read_csv(p, **read_kwargs)
    
    elif ext in {"xlsx", "xls"}:
        df = pd.read_excel(p, **read_kwargs)
    # elif ext == "json":
    #     with p.open("r", encoding="utf-8") as f:
    #         return json.load(f)
    else:
        raise ValueError("Unsupported file type. Use: csv, tsv, txt, xlsx, xls.")

    if "expression" not in df.columns:
        raise KeyError("Input must contain a column named 'expression'.")

    return df

def translate_file_with_vrs(input_file, output_file="all_alleles.json", error_file="allele_errors.json"):
    df = load_data(input_file)

    dp = SeqRepoAPI().seqrepo_dataproxy
    trl = AlleleTranslator(data_proxy=dp)
    allele_translator = VrsFhirAlleleTranslator()

    translations = []
    errors = []

    for idx, expr in df['expressions'].items():
        try:
            vo = trl.translate_from(expr)
            fo = allele_translator.translate_allele_to_fhir(vo)

            translations.append({
                "ROW_INDEX": int(idx),
                "EXPRESSION": expr,
                "VRS_ALLELE": vo.model_dump(exclude_none=True),
                "FHIR_Allele": fo.model_dump()
            })
        except Exception as e:
            errors.append({"ROW_INDEX": int(idx), "EXPRESSION": expr, "ERROR": str(e)})

    output_path = Path(output_file)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(translations, f, indent=2, ensure_ascii=False)

    error_path = Path(error_file)
    with error_path.open("w", encoding="utf-8") as f:
        json.dump(errors, f, indent=2, ensure_ascii=False)

    return output_path, error_path


# def _extract_expression_column(df, column):
#      if column in df.columns:
#           return column
     
# def _dump_vrs_model(vo):
#     if hasattr(vo, "model_dump"):
#          return vo.model_dump()
#     raise TypeError("unexpected VRS model type")


