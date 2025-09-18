import argparse
import json
import logging
import sys
from pathlib import Path

import pandas as pd
from ga4gh.vrs.extras.translator import AlleleTranslator
from ga4gh.vrs.models import Allele

from api.seqrepo import SeqRepoAPI
from translators.vrs_fhir_translator import VrsFhirAlleleTranslator


class AlleleToFhirTranslator:
    def __init__(self):
        self.dp = SeqRepoAPI().seqrepo_dataproxy
        self.trl = AlleleTranslator(data_proxy=self.dp)
        self.fhir = VrsFhirAlleleTranslator()

    def _stats(self, df, translations):
        total = len(df)
        translated = len(translations)
        untranslatable = total - translated
        return {
            "Total Rows": total,
            "Translatable": translated,
            "Untranslatable": untranslatable,
        }

    def _write_out(self,path, rows):
        with path.open("w", encoding="utf-8") as f:
            for row in rows:
                f.write(json.dumps(row,ensure_ascii=False) + "\n")

    def load_data(self, input_file, **read_kwargs):
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

        elif ext == "jsonl":
            read_kwargs.setdefault("lines",True)
            df = pd.read_json(p, **read_kwargs)

        else:
            raise ValueError(f"Unsupported file type for '{p.name}'. Use: csv, tsv, txt, xlsx, xls, jsonl.")

        return df

    def tabular_file_translation(self,input_file, output_file="all_alleles.jsonl", error_file="allele_errors.jsonl", column="expression",dry_run=False):

        df = self.load_data(input_file)

        if column not in df.columns:
            raise KeyError(f"Column '{column}' not found in file {input_file}. Available columns: {df.columns.tolist()}")

        fhir_translations = []
        errors = []

        for idx, expr in df[column].items():
            try:
                vo = self.trl.translate_from(expr)
                fo = self.fhir.translate_allele_to_fhir(vo)

                fhir_translations.append({
                    "ROW_INDEX": int(idx),
                    "EXPRESSION": expr,
                    "VRS_ALLELE": vo.model_dump(exclude_none=True),
                    "FHIR_ALLELE": fo.model_dump()
                })
            except Exception as e:
                errors.append({"ROW_INDEX": int(idx), "EXPRESSION": expr, "ERROR": str(e)})

        output_path = Path(output_file)
        error_path = Path(error_file)

        if not dry_run:
            self._write_out(path=output_path,rows=fhir_translations)
            if errors:
                self._write_out(path=error_path,rows=errors)

        stats = self._stats(df, fhir_translations)
        return output_path, error_path, stats

    def jsonl_file_translation(self, input_file, output_file="all_alleles.jsonl", error_file="allele_errors.jsonl", column="out", dry_run=False):

        df = self.load_data(input_file)
        if column not in df.columns:
            raise KeyError(f"Column '{column}' not found. Available: {df.columns.tolist()}")


        vrs_alleles = []
        error_vrs_translation = []
        unexpected_error = []

        for idx, vo in df[column].items():
            if not isinstance(vo,dict):
                unexpected_error.append({"ROW_INDEX": int(idx), "ERROR": f"Expected dict in '{column}', got {type(vo).__name__}."})
                continue

            if "errors" in vo:
                error_vrs_translation.append({"ROW_INDEX": int(idx), "ERROR": vo["errors"]})
            elif vo.get('type') == "Allele":
                try:
                    vrs_alleles.append({"ROW_INDEX": int(idx), "VRS_Allele": Allele(**vo)})
                except Exception as e:
                    error_vrs_translation.append({"ROW_INDEX": int(idx), "ERROR": f"Failed to instantiate Allele: {e}"})
            else:
                unexpected_error.append({"ROW_INDEX": int(idx), "ERROR": f"Unexpected out.type={vo.get('type')}"})

        fhir_translations = []
        error_fhir_translation = []

        for vo in vrs_alleles:
            idx = vo["ROW_INDEX"]
            allele = vo["VRS_Allele"]

            try:
                fhir_allele_profile = self.fhir.translate_allele_to_fhir(allele)
                fhir_translations.append({
                    "ROW_INDEX": idx,
                    "VRS_ALLELE": allele.model_dump(exclude_none=True),
                    "FHIR_ALLELE": fhir_allele_profile.model_dump()
                })
            except Exception as e:
                error_fhir_translation.append({
                    "ROW_INDEX": idx,
                    "VRS_ALLELE": allele.model_dump(exclude_none=True),
                    "ERROR": str(e)
                })

        output_path = Path(output_file)
        error_path = Path(error_file)

        if not dry_run:
            self._write_out(path=output_path,rows=fhir_translations)
            all_errors = error_vrs_translation + error_fhir_translation + unexpected_error
            if all_errors:
                self._write_out(path=error_path,rows=all_errors)

        stats = self._stats(df, fhir_translations)

        return output_path, error_path, stats

    def translate_file(self, input_file, **kwargs):
        ext = Path(input_file).suffix.lower().lstrip(".")
        if ext == "jsonl":
            return self.jsonl_file_translation(input_file,**kwargs)
        else:
            return self.tabular_file_translation(input_file,**kwargs)

    def main(self,argv=None):
        parser = argparse.ArgumentParser(
            prog="allele-to-fhir-translator",
            description="Load a dataset and translate allele expressions (tabular) or VRS 'out' objects (jsonl) to FHIR"
        )

        parser.add_argument("input_path", help="Input file to process (csv, tsv, txt, xlsx, xls, jsonl)")
        parser.add_argument("--out", default="all_alleles.jsonl", help="Output file for translations (default: all_alleles.jsonl)")
        parser.add_argument("--errors", default="allele_errors.jsonl", help="Output file for errors (default: allele_errors.jsonl)")
        parser.add_argument("--column", required=True, help="Name of the column to read (REQUIRED)")
        parser.add_argument("--verbose", action="store_true",help="Enable detailed logging")
        parser.add_argument("--dry-run", action="store_true",help="Run without writing output files")
        parser.add_argument("--overwrite", action="store_true", help="Allow overwriting existing files")

        args = parser.parse_args(argv)

        logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
        logging.info("Starting Translation Job")
        logging.debug("Arguments: %s",args)

        if not args.dry_run and not args.overwrite:
            for p in [args.out, args.errors]:
                if Path(p).exists():
                    parser.error(f"Refusing to overwrite '{p}'. Pass --overwrite to allow.")

        out_path,err_path, stats = self.translate_file(
            input_file=args.input_path,
            output_file=args.out,
            error_file=args.errors,
            column=args.column,
            dry_run=args.dry_run,
            )

        if args.dry_run:
            logging.info("Dry run mode: no files written")
        else:
            logging.info("Wrote results to %s and errors to %s", out_path, err_path)

        logging.info("Done: Total Rows=%d Translatable=%d Untranslatable=%d", stats['Total Rows'], stats['Translatable'], stats['Untranslatable'])

        return 0

if __name__ == "__main__":
    sys.exit(AlleleToFhirTranslator().main())
