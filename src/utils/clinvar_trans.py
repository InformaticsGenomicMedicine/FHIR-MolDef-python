#NOTE: This is still in the process of developement, needs more testing and work

import argparse
import gzip

import logging
import time
from datetime import datetime

import orjson
from ga4gh.vrs.models import Allele

from translators.vrs_to_fhir import VrsToFhirAlleleTranslator


class FastTranslation:

    def __init__(self):
        self.vrs_translator = VrsToFhirAlleleTranslator()

    def clinvartranslation(self,inputfile, outputfile, invalid_allele_path, invalid_fhir_path, limit = None):

        started_at_wall = datetime.now()
        t0 = time.perf_counter()

        invalid_allele_log = open(invalid_allele_path, "ab")
        invalid_fhir_trans_log = open(invalid_fhir_path, "ab")
        stats = open("translational_stats.txt", "wb")

        total_translated = 0
        failed_vrs_allele_validation = 0
        failed_vrs_to_fhir_translation = 0
        lines_read = 0
        allele_members_seen = 0

        try:
            with open(outputfile, "ab") as out_f:
                with gzip.open(inputfile, "rt", encoding="utf-8") as f:
                    for line_num, line in enumerate(f, 1):
                        lines_read += 1
                        if limit is not None and line_num > limit:
                            break
                        try:
                            obj = orjson.loads(line)
                            members = obj.get("members", [])
                        except orjson.JSONDecodeError:
                            logging.warning("[Line %d] Skipping: JSON decode error", line_num)
                            continue

                        for member in members:
                            if not (isinstance(member, dict) and member.get("type") == "Allele"):
                                continue
                            allele_members_seen += 1
                            try:
                                vo = Allele(**member)
                            except Exception as e:
                                failed_vrs_allele_validation += 1

                                invalid_allele = {"line": line_num, "error": str(e), "member": member}
                                invalid_allele_log.write(orjson.dumps(invalid_allele) + b"\n")
                                continue

                            try:
                                fhir_obj = self.vrs_translator.translate_allele_to_fhir(vo)

                                valid_translation = {
                                    "line": line_num,
                                    "vrs_allele": vo.model_dump(exclude_none=True),
                                    "fhir_allele": fhir_obj.model_dump(exclude_none=True),
                                }
                                total_translated += 1
                                out_f.write(orjson.dumps(valid_translation) + b"\n")

                            except Exception as e:
                                failed_vrs_to_fhir_translation += 1

                                invalid_translation = {
                                    "line": line_num,
                                    "error": str(e),
                                    "vrs_allele": vo.model_dump(exclude_none=True),
                                }
                                invalid_fhir_trans_log.write(orjson.dumps(invalid_translation) + b"\n")
        finally:
            t1 = time.perf_counter()
            ended_at_wall = datetime.now()
            duration = max(t1 - t0, 1e-9)

            final_stats = {
                "started_at": started_at_wall.isoformat(timespec="seconds"),
                "ended_at": ended_at_wall.isoformat(timespec="seconds"),
                "duration_seconds": round(duration, 3),
                "lines_read": lines_read,
                "allele_members_seen": allele_members_seen,
                "total_translated": total_translated,
                "failed_vrs_allele_validation": failed_vrs_allele_validation,
                "failed_vrs_to_fhir_translation": failed_vrs_to_fhir_translation,
                "total_failed": failed_vrs_allele_validation + failed_vrs_to_fhir_translation,
            }

            stats.write(orjson.dumps(final_stats, option=orjson.OPT_INDENT_2) + b"\n")
            stats.close()

            invalid_allele_log.close()
            invalid_fhir_trans_log.close()

    def main(self):
        parser = argparse.ArgumentParser(
            prog="allele-to-fhir-translator",
            description="Load a dataset and translate allele expressions (tabular) or VRS 'out' objects (jsonl) to FHIR"
        )
        parser.add_argument("input_gzip", help="Path to gzipped JSONL file")
        parser.add_argument("--invalid-allele-log", default="invalid_alleles.jsonl")
        parser.add_argument("--invalid-fhir-log", default="invalid_fhir_trans.jsonl")
        parser.add_argument("--limit", type=int, help="Process only this many lines from input")
        parser.add_argument("--verbose", action="store_true", help="Enable detailed logging")

        args = parser.parse_args()

        logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
        logging.info("Starting Translation Job")


        self.clinvartranslation(
            inputfile=args.input_gzip,
            outputfile="vrs_to_fhir_translations.jsonl",
            invalid_allele_path=args.invalid_allele_log,
            invalid_fhir_path=args.invalid_fhir_log,
            limit=args.limit,
        )

if __name__ == "__main__":
    FastTranslation().main()
