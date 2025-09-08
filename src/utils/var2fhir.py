##
## This module accepts variant inputs in SPDI, HGVS, or VRS formats.
##
## 1. The input format is automatically detected.
## 2. If the input is SPDI or HGVS, it is translated into a normalized VRS object
##    using the vrs-python translator.
## 3. All variants represented as VRS objects are then converted into a FHIR
##    Allele profile.
##
