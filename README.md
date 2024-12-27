## Overview

Welcome to the **FHIR-MolDef-python** repository! This project provides a Python-based implementation of the HL7 FHIR Molecular Definition standard. It is designed to simplify the creation of Molecular Definition resources, including Molecular Definition Allele Profiles, and to enable seamless bidirectional translations between Allele Profiles and VRS Alleles.

## Features

- **Generation of Molecular Definition Resources**  
  Effortlessly generate fully compliant Molecular Definition resources based on the HL7 FHIR standard.

- **Allele Profile Support**  
  Leverage the Allele Profile, a child class of the Molecular Definition resource, to create and manage allele-specific representations. 
  
- **Bidirectional Translation**  
  Perform reliable and seamless bidirectional translations between Allele Profiles and VRS Alleles (version 1.3), ensuring data interoperability and consistency across platforms.

- **Educational Jupyter Notebooks**  
  Leverage interactive Jupyter notebooks for a hands-on learning experience, providing practical examples and educational insights into the implementation and its functionality.

## Interacting with Notebooks
To interact with the FHIR-MolDef-python, you can use GitHub Codespaces to access and work with the Jupyter Notebooks directly. If you plan to make changes, please fork the repository and submit your suggestions or modifications via an issue and a pull request. Personal accounts receive 120 free hours of Codespaces usage, while Pro accounts receive 180 hours. Be aware that Codespaces has a default timeout period of 30 minutes. For more information about Codespaces, refer to the links provided below. If you're already familiar with Codespaces and Jupyter Notebooks, you can proceed with the instructions below.

If you're new to using **Codespaces**, the following resources may be helpful:
- [Codespaces Overview](https://docs.github.com/en/codespaces/overview)
- [Codespaces Getting Started Documentation](https://docs.github.com/en/codespaces/getting-started/quickstart)

## Access Notebooks (Codespace)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=905915041)

## 1. Starting Codespace
- Start off by clicking the Codespaces badge above to get started.
- A prompt to build a code space will pop up with certain specifications.
- Click on **Create Codespace**.
- ⚠️ **NOTE**: This will take a few minutes to build your virtual machine. A message will appear in the terminal indicating the progress:
    ```bash
    Finishing up...
    Running postCreateCommand...
    ```

## 2. Selecting Kernel
- Navigate to the notebooks and select a notebook you wish to run.
- Locate the **Select Kernel** option on the top right-hand side of the interface.
- Click on **Select Kernel**.

## 3. Choosing Python Environment
- After clicking **Select Kernel**, choose **Python Environment...**.
- From the dropdown menu, select:
    ```plaintext
    Python 3.11.11 /usr/local/bin/python
    ```

## 4. Running Notebooks
- Once the appropriate kernel is selected, you can proceed to run the cells inside the Jupyter notebooks.
- 💡 **Tip**: Use `Shift + Enter` to execute a cell quickly.

## 5. Deactivating Codespace
- On the bottom left corner of your browser, click on **CodeSpaces:**.
- Then click **Stop Current Codespace**.
- ✅ Once this is done, you have successfully deactivated your Codespace.

## Acknowledgments

- **[vrs-python](https://github.com/ga4gh/vrs-python)**
- **[biocommons.seqrepo](https://github.com/biocommons/biocommons.seqrepo)**
- **[HL7 FHIR](https://hl7.org/fhir/6.0.0-ballot2/moleculardefinition.html)**
- **[fhir.resource](https://github.com/nazrulworld/fhir.resources)**
- **[fhir-core](https://github.com/nazrulworld/fhir-core)**