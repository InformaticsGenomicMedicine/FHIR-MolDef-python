## FHIR-MolDef-Python Educational Notebook Series

This repository contains a collection of interactive Jupyter notebooks designed to provide a hands-on introduction to the **FHIR-MolDef-Python** codebase. The notebooks cover working with the **HL7 FHIR MolecularDefinition Resource**, exploring **Profiles**, and implementing bidirectional **translation between GA4GH VRS (v1.3)** and **HL7 FHIR MolecularDefinition**.

For setup instructions, including how to run these notebooks in **Codespaces**, refer to the main project [README](../README.md).

### Notebook Categories

### 1. **Molecular Definition**
- **[MolecularDefinition](molecular_definition_demo.ipynb)**  
   - Demonstrates the Python implementation of the HL7 FHIR **MolecularDefinition** resource.  
   - Includes a structured, step-by-step guide for constructing a MolecularDefinition resource.

---

### 2. **Profiles**
- **[AlleleProfile](allele_profile_demo.ipynb)**  
   - Explores the Python implementation of the **HL7 FHIR AlleleProfile**.  
   - Provides a walkthrough for constructing an AlleleProfile resource.  

- **[SequenceProfile](sequence_profile_demo.ipynb)**  
   - Showcases the Python implementation of the **HL7 FHIR SequenceProfile**.  
   - Guides users through the step-by-step process of building a SequenceProfile resource.

---

### 3. **Translator**
- **[VRS to FHIR Translation](vrs_translation_to_allele_profile_demo.ipynb)**  
   - Demonstrates how to convert **GA4GH VRS (v1.3)** representations into HL7 FHIR **AlleleProfile** resources.  

- **[FHIR to VRS Translation](allele_profile_to_vrs_translation_demo.ipynb)**  
   - Shows the process of translating HL7 FHIR **AlleleProfile** resources back into **GA4GH VRS (v1.3)** representations.  

---

