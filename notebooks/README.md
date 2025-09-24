## FHIR-MolDef-Python Educational Notebook Series

This repository contains a collection of interactive Jupyter notebooks designed to provide a hands-on introduction to the **FHIR-MolDef-Python** codebase. The notebooks cover working with the **HL7 FHIR MolecularDefinition Resource**, exploring **Profiles**, and implementing bidirectional **translation between GA4GH VRS (v2.0)** and **HL7 FHIR MolecularDefinition**.

### **Recommended Knowledge**

To get the most out of these notebooks, we recommend the following prerequisites:
   - Familiarity with **Jupyter Notebook** and **Python**.
   - An understanding of the **HL7 FHIR MolecularDefinition** schema, you can review it here: [FHIR MolecularDefinition Schema](https://build.fhir.org/moleculardefinition.html).
   - Knowledge of the **GA4GH VRS (v2.0)** schema, which is essential for bidirectional translation. Documentation is available here: [GA4GH VRS Schema](https://vrs.ga4gh.org/en/stable/).

For setup instructions, including how to run these notebooks in **Codespaces**, refer to the main project [README](../README.md).


## Notebook Categories

### 1. **Schema Notebooks** (`notebooks/schema/`)

- **[MolecularDefinition](schema/molecular_definition_demo.ipynb)**  
   - Demonstrates the Python implementation of the HL7 FHIR **MolecularDefinition** resource.  
   - Includes a structured, step-by-step guide for constructing a MolecularDefinition resource.

- **[Allele Profile](schema/allele_profile_demo.ipynb)**  
   - Explores the Python implementation of the **HL7 FHIR Allele**.  
   - Provides a walkthrough for constructing an Allele resource.  

- **[Sequence Profile](schema/sequence_profile_demo.ipynb)**  
   - Showcases the Python implementation of the **HL7 FHIR Sequence**.  
   - Guides users through the step-by-step process of building a Sequence profile.

### 2. **Translation Notebooks** (`notebooks/translations/`)

- **[VRS to FHIR: Translation to AlleleProfile](translations/vrs_allele_translation.ipynb)**  
   - Demonstrates how to convert **GA4GH VRS (v2.0)** representations into HL7 FHIR **AlleleProfile** resources.  

- **[FHIR to VRS: Translation to VRS Allele](translations/fhir_allele_translation.ipynb)**  
   - Shows the process of translating HL7 FHIR **AlleleProfile** resources back into **GA4GH VRS (v2.0)** representations.  

- **[Allele Factory Demo](translations/allele_factory_demo.ipynb)**
   - Showcases the **Allele Factory Module**, which simplifies the creation of **VRS Alleles** and **FHIR Allele** resources.
   - Since generating these profiles requires a solid understanding of the schema, this module helps users by generating an Allele with just **five input attributes**.
   - The **Allele Factory Module** reduces the learning curve by automating profile generation, making it easier for users to work with VRS and FHIR Alleles without deep prior knowledge of their schemas.

- **[Full Allele Translations](vrs_fhir_full_translation_demo.ipynb)**  
   - Demonstrates the **VRSToFHIR** and **FHIRToVRS** modules, which enable translation of fully populated **VRS Allele** objects into **FHIR Allele** resources, and vice versa.  
   - Since **FHIR includes attributes beyond those defined in VRS**, the translation is asymmetric: every VRS Allele can be represented in FHIR, but only the overlapping fields can be translated from FHIR back to VRS.  
   - This notebook goes beyond the minimal examples by focusing on **full, schema-compliant translations** within that shared subset.  