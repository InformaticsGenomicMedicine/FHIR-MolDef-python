import argparse
import json
import logging
import sys
from pathlib import Path

import pandas as pd
from ga4gh.vrs.extras.translator import AlleleTranslator

from api.seqrepo import SeqRepoAPI
from translators.vrs_fhir_translator import VrsFhirAlleleTranslator


class AlleleToFhirTranslator:
    def __init__(self):
        self.dp = SeqRepoAPI().seqrepo_dataproxy
        self.trl = AlleleTranslator(data_proxy=self.dp)
        self.fhir = VrsFhirAlleleTranslator()

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
        # elif ext == "json":
        #     with p.open("r", encoding="utf-8") as f:
        #         return json.load(f)
        else:
            raise ValueError("Unsupported file type. Use: csv, tsv, txt, xlsx, xls.")

        return df

    def translate_file(self,input_file, output_file="all_alleles.json", error_file="allele_errors.json", column="expression",dry_run=False):

        df = self.load_data(input_file)

        if column not in df.columns:
            raise KeyError(f"Column '{column}' not found in file {input_file}. Available columns: {df.columns.tolist()}")

        translations = []
        errors = []

        for idx, expr in df[column].items():
            try:
                vo = self.trl.translate_from(expr)
                fo = self.fhir.translate_allele_to_fhir(vo)

                translations.append({
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
            with output_path.open("w", encoding="utf-8") as f:
                json.dump(translations, f, indent=2, ensure_ascii=False)
            with error_path.open("w", encoding="utf-8") as f:
                json.dump(errors, f, indent=2, ensure_ascii=False)

        stats = {"Total Expressions": len(df), "Translatable": len(translations), "Untranslatable": len(errors)}
        return output_path, error_path, stats


    # def _extract_expression_column(df, column):
    #      if column in df.columns:
    #           return column

    # def _dump_vrs_model(vo):
    #     if hasattr(vo, "model_dump"):
    #          return vo.model_dump()
    #     raise TypeError("unexpected VRS model type")

    def main(self,argv=None):
        parser = argparse.ArgumentParser(
            prog="allele-translator",
            description="Load a dataset and translate allele expression to FHIR"
        )

        parser.add_argument("input_path", help="Input file to process (csv, tsv, txt, xlsx, xls)")
        parser.add_argument("--out", default="all_alleles.json", help="Output file for translations (default: all_alleles.json)")
        parser.add_argument("--errors", default="allele_errors.json", help="Output file for errors (default: allele_errors.json)")
        parser.add_argument("--column", default="expression", help="Name of the column containing expressions (default: expression)")
        parser.add_argument("--verbose", action="store_true",help="Enable detailed logging")
        parser.add_argument("--dry-run", action="store_true",help="Run without writing output files")
        parser.add_argument("--overwrite", action="store_true", help="Allow overwriting existing files")

        args = parser.parse_args(argv)

        logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

        logging.info("Starting Translation Job")
        logging.debug("Arguments: %s",args)


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

        logging.info("Done: Total Expressions=%d Translatable=%d Untranslatable=%d", stats['Total Expressions'],stats['Translatable'],stats['Untranslatable'])

        return 0

if __name__ == "__main__":
    sys.exit(AlleleToFhirTranslator().main())
