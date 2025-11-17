## Overview

Welcome to the  **FHIR-MolDef-python** repository! This repository provides a Python-based implementation of the HL7 (Health Level Seven) Fast Healthcare Interoperability Resources (FHIR) Molecular Definition standard. It enables you to create instances of the MolecularDefinition resource and currently supports two profiles: Sequence and Allele. A profile in FHIR is a structured extension of a resource that defines specific constraints and usage guidelines for particular use cases.

Additionally, this repository facilitates seamless, bidirectional translation between Global Alliance for Genomics and Health (GA4GH) Variant Representation Specification (VRS) Alleles (v2.0) and the FHIR Allele, ensuring interoperability between these two standards.

To help you get started, we provide Jupyter notebooks that serve as an educational guide. These notebooks introduce the MolecularDefinition resource, explain its profiles, and showcase the translation process between VRS Alleles (v2.0) and FHIR Allele with practical examples.


## Disclaimer

* The `MolecularDefinition` schema used in this project is based on the **most recent schema development** as described here: [Work in Progress Schema](https://build.fhir.org/branches/cg-im-moldef_work_in_progress_2/moleculardefinition.html).  

* It does **not** align with the schema provided in the HL7 FHIR 6.0.0 Ballot 2 version available here: [FHIR Ballot 2 Schema](https://hl7.org/fhir/6.0.0-ballot2/moleculardefinition.html).  

* **Note**: The [Work in Progress Schema](https://build.fhir.org/branches/cg-im-moldef_work_in_progress_2/moleculardefinition.html) page may occasionally be unavailable due to active development. This downtime is beyond our group's control. If the page is temporarily inaccessible, we recommend trying again later.


## Features

### Resource
* **Generation of Molecular Definition Resources**: Effortlessly create fully compliant Molecular Definition resources based on the HL7 FHIR standard.

### Profile
* **Sequence**: Sequence is a specialized subclass of the MolecularDefinition resource, enabling you to create sequence-specific representations.

* **Allele**: Allele is a specialized subclass of the MolecularDefinition resource, allowing you to create and manage allele-specific representations.

### Translation
* **Bidirectional Translation**: Perform seamless, bidirectional translations between FHIR Allele and VRS Alleles (version 2.0), ensuring interoperability and data consistency across diverse platforms.

### Notebooks
* **Educational Jupyter Notebooks**: Access interactive Jupyter notebooks for a hands-on learning experience, complete with practical examples and educational insights into the implementation’s functionality.

## Installation Status

* This package is not currently published on PyPI, but we plan to make it available soon. In the meantime, clone the repository and follow the instructions below to work with the code locally.

## Prerequisites

* **Python 3.11 or Higher**: This package requires Python 3.11 or a newer version. Please ensure it is installed on your machine.
* **Virtual Environment (Recommended)**: Using a virtual environment is highly recommended to isolate dependencies for this project.

## Steps to Set Up Locally

1. **Clone the Repository**:
   Ensure you are logged into your GitHub account. Navigate to the repository on GitHub, click the green **Code** button, and copy the repository link. Then, use the following command to clone the repository to your local machine:

   ```bash
   git clone https://github.com/YourUsername/FHIR-MolDef-python.git
   cd FHIR-MolDef-python
   ```

2. **Set Up a Virtual Environment**:
   For our development, we used Python's built-in `venv` module to create the virtual environment. Once the virtual environment is created, ensure it is activated.

3. **Install the Package in Editable Mode**:
   - If you want to install the package without the development dependencies:
     ```bash
     pip install -e .
     ```

   - Install the package along with development dependencies using the following commands for macOS:
     ```bash
     pip install -e . '.[dev]'
     ```

   - Install the package along with development dependencies using the following commands for Windows:
     ```bash
     pip install -e .[dev]
     ```

4. **Verify Installation**:
   Confirm the package is installed by running:
   ```bash
   pip show FHIR-MolDef-python
   ```


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

## Contributing

* Contributions are highly appreciated! Feel free to fork the repository and submit a pull request with your changes. You can also report issues or suggest improvements by opening an issue in the tracker. Thank you for your support!

## Acknowledgments

This project relies on the following packages and resources. We extend our gratitude to their respective developers and contributors for making these tools freely available:

* **[vrs-python](https://github.com/ga4gh/vrs-python)**
* **[biocommons.seqrepo](https://github.com/biocommons/biocommons.seqrepo)**
* **[biocommons.seqrepo-rest-services](https://github.com/biocommons/seqrepo-rest-service)**
* **[HL7 FHIR](https://hl7.org/fhir/6.0.0-ballot2/moleculardefinition.html)**
* **[fhir.resource](https://github.com/nazrulworld/fhir.resources)**
* **[fhir-core](https://github.com/nazrulworld/fhir-core)**