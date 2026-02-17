## Overview

Welcome to the  **FHIR-MolDef-python** repository! This repository provides a Python-based implementation of the HL7 (Health Level Seven) Fast Healthcare Interoperability Resources (FHIR) Molecular Definition standard. It enables you to create instances of the MolecularDefinition resource and currently supports three profiles: Sequence,Allele, and Variant. A profile in FHIR is a structured extension of a resource that defines specific constraints and usage guidelines for particular use cases.

Additionally, this repository facilitates seamless, bidirectional translation between Global Alliance for Genomics and Health (GA4GH) Variant Representation Specification (VRS) Alleles (v2.0) and the FHIR Allele Profile, ensuring interoperability between these two standards.

<!-- To help you get started, we provide Jupyter notebooks that serve as an educational guide. These notebooks introduce the MolecularDefinition resource, explain its profiles, and showcase the translation process between VRS Alleles (v2.0) and FHIR Allele with practical examples. -->


## Disclaimer

* This project uses the `MolecularDefinition` schema from the lastest in-progress development: [Work in Progress Schema](https://build.fhir.org/branches/cg-im-moldef_work_in_progress_2/moleculardefinition.html). 
 
* It does **not** match with the schema in the HL7 FHIR 6.0.0 Ballot 2 release: [FHIR Ballot 2 Schema](https://hl7.org/fhir/6.0.0-ballot2/moleculardefinition.html).  


> **NOTE: This page may occasionally be unavailable due to active development. If so, please try again later, as this downtime is beyond our group's control.**

<!-- * **Note**: The [Work in Progress Schema](https://build.fhir.org/branches/cg-im-moldef_work_in_progress_2/moleculardefinition.html) page may occasionally be unavailable due to active development. This downtime is beyond our group's control. If the page is temporarily inaccessible, we recommend trying again later. -->

## Core Functionality

| Category     | Currently Supports |
|--------------|--------------------|
| **Resource** | HL7 FHIR MolecularDefinition resource generation |
| **Profiles** | Sequence, Allele, and Variant profiles |
| **Translation** | Bidirectional VRS 2.0 translations (full + minimal) |
| **Notebooks** | Interactive Jupyter notebooks with examples (**see the Notebooks README for details**) |
| **Pipeline** | Extract VRS Allele objects from ClinVar variation files and translate them into the FHIR Allele Profile |

<!-- ## Features

### Resource
* **Generation of Molecular Definition Resources**: Effortlessly create fully compliant Molecular Definition resources based on the HL7 FHIR standard.

### Profile
* **Sequence**: Sequence is a specialized subclass of the MolecularDefinition resource, enabling you to create sequence-specific representations.

* **Allele**: Allele is a specialized subclass of the MolecularDefinition resource, allowing you to create and manage allele-specific representations.

### Translation
* **Bidirectional Translation**: Perform seamless, bidirectional translations between FHIR Allele and VRS Alleles (version 2.0), ensuring interoperability and data consistency across diverse platforms.

### Notebooks
* **Educational Jupyter Notebooks**: Access interactive Jupyter notebooks for a hands-on learning experience, complete with practical examples and educational insights into the implementation’s functionality. -->

## Installation Status

* This package is not currently published on PyPI, but we plan to make it available soon. In the meantime, clone the repository and follow the instructions below to work with the code locally.

## Prerequisites

* **Python 3.11 or Higher**: This package requires Python 3.11 or a newer version. Please ensure it is installed on your machine.
* **Virtual Environment (Recommended)**: Using a virtual environment is highly recommended to isolate dependencies for this project.

## Dependencies & Infrastructure

* This package currently relies on a **local installation of SeqRepo**, which is required to perform the bidirectional translations.  
* We are in the process of writing documentation for installing SeqRepo locally, as well as providing a **docker-compose.yml** configuration to run SeqRepo (and future UTA support) in a containerized environment.

## Local Setup

Follow these steps to set up the project for local development.

### 1. Clone the Repository
Make sure you’re logged into GitHub, then clone the repository and navigate into it:

```bash
git clone https://github.com/YourUsername/FHIR-MolDef-python.git
cd FHIR-MolDef-python
```

### 2. Create and Activate a Virtual Environment
We recommend using Python’s built-in `venv` module.

   ```bash
   python -m venv venv
   ```

Activate the virtual environment

- **macOS/Linux**
   ```bash
   source venv/bin/activate
   ```
- **Windows** 
   ```bash
   venv\Scripts\activate
   ```

### 3. Install the Package
- **Installation (until the package is published)**
   ```bash
   pip install . 
   ```

- **Local Development**
   ```bash
   pip install -e .[dev]
   ```

### 4. Verify Installation
Confirm the package was installed successfully
   ```bash
   pip show FHIR-MolDef-python
   ```

## Contributing

* Contributions are highly appreciated! Feel free to fork the repository and submit a pull request with your changes. You can also report issues or suggest improvements by opening an issue in the tracker. Thank you for your support!

## Acknowledgments

This project builds upon the following community standards and open-source implementations:

### Standards

- [GA4GH Variation Representation Specification (VRS)](https://vrs.ga4gh.org/)
- [HL7 FHIR MolecularDefinition](https://hl7.org/fhir/6.0.0-ballot2/moleculardefinition.html)

### Software

- [vrs-python](https://github.com/ga4gh/vrs-python)
- [biocommons.seqrepo](https://github.com/biocommons/biocommons.seqrepo)
- [fhir.resources](https://github.com/nazrulworld/fhir.resources)
- [fhir-core](https://github.com/nazrulworld/fhir-core)

We gratefully acknowledge the communities and contributors who develop and maintain these resources.