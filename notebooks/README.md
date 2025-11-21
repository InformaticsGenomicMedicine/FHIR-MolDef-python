## FHIR-MolDef-Python Educational Notebook Series

This repository includes a set of interactive Jupyter notebooks that provide a hands-on introduction to the 
**FHIR-MolDef-Python** codebase. The notebooks demonstrate how to work with the **HL7 FHIR MolecularDefinition Resource**, exploring its associated **Profiles**, and perform bidirectional translation between **GA4GH VRS (v2.0)** and **HL7 FHIR MolecularDefinition**.

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

### 2. **Translational Notebooks** (`notebooks/translations/`)

- **[VRS to FHIR: Translation to AlleleProfile](translations/vrs_allele_translation.ipynb)**  
   - Demonstrates how to convert **GA4GH VRS (v2.0)** representations into HL7 FHIR **AlleleProfile** resources.  

- **[FHIR to VRS: Translation to VRS Allele](translations/fhir_allele_translation.ipynb)**  
   - Shows the process of translating HL7 FHIR **AlleleProfile** resources back into **GA4GH VRS (v2.0)** representations.  

- **[Allele Factory Demo](translations/allele_factory_demo.ipynb)**
   - Showcases the **Allele Factory Module**, which simplifies the creation of **VRS Alleles** and **FHIR Allele** resources.
   - Since generating these profiles requires a solid understanding of the schema, this module helps users by generating an Allele with just **five input attributes**.
   - The **Allele Factory Module** reduces the learning curve by automating profile generation, making it easier for users to work with VRS and FHIR Alleles without deep prior knowledge of their schemas.

- **[Full Allele Translations](translations/vrs_fhir_full_translation_demo.ipynb)**  
   - Demonstrates the **VRSToFHIR** and **FHIRToVRS** modules, which enable translation of fully populated **VRS Allele** objects into **FHIR Allele** resources, and vice versa.  
   - Since **FHIR includes attributes beyond those defined in VRS**, the translation is asymmetric: every VRS Allele can be represented in FHIR, but only the overlapping fields can be translated from FHIR back to VRS.  
   - This notebook goes beyond the minimal examples by focusing on **full, schema-compliant translations** within that shared subset.  

- **[ClinVar Demo Translations](translations/clinvar_demo_translation.ipynb)**  
   - Demonstrates extraction and translation of ClinVar variation data into FHIR Allele Profiles.
   - Streams compressed .jsonl.gz ClinVar files efficiently and filters for VRS Allele records.
   - Extracts representative VRS Allele objects and performs VRS Allele to FHIR Allele Profile translation.  
   - Currently translates a subset (~20K examples); full dataset support and a CLI tool are in development.  

<!-- ### **Recommended Knowledge**

To get the most out of these notebooks, we recommend the following prerequisites:
   - Familiarity with **Jupyter Notebook** and **Python**.
   - An understanding of the **HL7 FHIR MolecularDefinition** schema, you can review it here: [FHIR MolecularDefinition Schema](https://build.fhir.org/moleculardefinition.html).
   - Knowledge of the **GA4GH VRS (v2.0)** schema, which is essential for bidirectional translation. Documentation is available here: [GA4GH VRS Schema](https://vrs.ga4gh.org/en/stable/).

For setup instructions, including how to run these notebooks in **Codespaces**, refer to the main project [README](../README.md). -->

## Interacting with Notebooks
To interact with the FHIR-MolDef-python, you can use GitHub Codespaces to access and work with the Jupyter Notebooks directly. If you plan to make changes, please fork the repository and submit your suggestions or modifications via an issue and a pull request. Personal accounts receive 120 free hours of Codespaces usage, while Pro accounts receive 180 hours. Be aware that Codespaces has a default timeout period of 30 minutes. For more information about Codespaces, refer to the links provided below. If you're already familiar with Codespaces and Jupyter Notebooks, you can proceed with the instructions below.

If you're new to using **Codespaces**, the following resources may be helpful:
* [Codespaces Overview](https://docs.github.com/en/codespaces/overview)
* [Codespaces Getting Started Documentation](https://docs.github.com/en/codespaces/getting-started/quickstart)

## Access Notebooks (Codespace)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=905915041)

## 1. Starting Codespace
* Start off by clicking the Codespaces badge above to get started.
* A prompt to build a code space will pop up with certain specifications.
* Click on **Create Codespace**.
* **NOTE**: This will take a few minutes to build your virtual machine. A message will appear in the terminal indicating the progress:
    ```bash
    Finishing up...
    Running postCreateCommand...
    ```
* **NOTE**: If you encounter the following GitHub Codespace error:

    > _"Oh no, it looks like you are offline! Make sure you are connected to the internet and try again. If you verified that your connection is fine, your firewall might be blocking the connection."_

    This issue is most likely caused by an active **VPN**. To resolve it:
    
    * Sign out of your **VPN** and try again.
    * If the issue persists, check your security settings or network configuration.

## 2. Selecting Kernel
* Navigate to the notebooks and select a notebook you wish to run.
* Locate the **Select Kernel** option on the top right-hand side of the interface.
* Click on **Select Kernel**.

## 3. Choosing Python Environment
* After clicking **Select Kernel**, a pop-up will appear. Choose **Python Environment...**.
* From the dropdown menu, select:
    ```plaintext
    Python 3.11.11 /usr/local/bin/python
    ```
* **NOTE**: This step must be performed for each notebook that you intend to execute.

## 4. Running Notebooks
* Once the appropriate kernel is selected, you can proceed to run the cells inside the Jupyter notebooks.
* 💡 **Tip**: Use `Shift + Enter` to execute a cell quickly.

## 5. Deactivating Codespace
* On the bottom left corner of your browser, click on **CodeSpaces:** (highlighted in blue).
* A pop-up will appear. Then, click **Stop Current Codespace**.
* Once this is done, you have successfully deactivated your Codespace.

