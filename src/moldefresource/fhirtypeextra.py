from __future__ import annotations as _annotations
from fhir_core.types import create_fhir_type


MolecularDefinitionType = create_fhir_type(
    "MolecularDefinitionType",
    "moldefresource.moleculardefinition.MolecularDefinition",
)

MolecularDefinitionLocationType = create_fhir_type(
    "MolecularDefinitionLocationType",
    "moldefresource.moleculardefinition.MolecularDefinitionLocation",
)

MolecularDefinitionLocationSequenceLocationType = create_fhir_type(
    "MolecularDefinitionLocationSequenceLocationType",
    "moldefresource.moleculardefinition.MolecularDefinitionLocationSequenceLocation",
)

MolecularDefinitionLocationSequenceLocationCoordinateIntervalType = create_fhir_type(
    "MolecularDefinitionLocationSequenceLocationCoordinateIntervalType",
    "moldefresource.moleculardefinition.MolecularDefinitionLocationSequenceLocationCoordinateInterval",
)

MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystemType = create_fhir_type(
    "MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystemType",
    "moldefresource.moleculardefinition.MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystem",
)

MolecularDefinitionLocationFeatureLocationType = create_fhir_type(
    "MolecularDefinitionLocationFeatureLocationType",
    "moldefresource.moleculardefinition.MolecularDefinitionLocationFeatureLocation",
)

MolecularDefinitionRepresentationType = create_fhir_type(
    "MolecularDefinitionRepresentationType",
    "moldefresource.moleculardefinition.MolecularDefinitionRepresentation",
)

MolecularDefinitionRepresentationLiteralType = create_fhir_type(
    "MolecularDefinitionRepresentationLiteralType",
    "moldefresource.moleculardefinition.MolecularDefinitionRepresentationLiteral",
)

MolecularDefinitionRepresentationExtractedType = create_fhir_type(
    "MolecularDefinitionRepresentationExtractedType",
    "moldefresource.moleculardefinition.MolecularDefinitionRepresentationExtracted",
)

MolecularDefinitionRepresentationRepeatedType = create_fhir_type(
    "MolecularDefinitionRepresentationRepeatedType",
    "moldefresource.moleculardefinition.MolecularDefinitionRepresentationRepeated",
)

MolecularDefinitionRepresentationConcatenatedType = create_fhir_type(
    "MolecularDefinitionRepresentationConcatenatedType",
    "moldefresource.moleculardefinition.MolecularDefinitionRepresentationConcatenated",
)

MolecularDefinitionRepresentationConcatenatedSequenceElementType = create_fhir_type(
    "MolecularDefinitionRepresentationConcatenatedSequenceElementType",
    "moldefresource.moleculardefinition.MolecularDefinitionRepresentationConcatenatedSequenceElement",
)

MolecularDefinitionRepresentationRelativeType = create_fhir_type(
    "MolecularDefinitionRepresentationRelativeType",
    "moldefresource.moleculardefinition.MolecularDefinitionRepresentationRelative",
)

MolecularDefinitionRepresentationRelativeEditType = create_fhir_type(
    "MolecularDefinitionRepresentationRelativeEditType",
    "moldefresource.moleculardefinition.MolecularDefinitionRepresentationRelativeEdit",
)


__all__ = [
    # New MolecularDefinition Values
    "MolecularDefinitionType",
    "MolecularDefinitionLocationType",
    "MolecularDefinitionLocationSequenceLocationType",
    "MolecularDefinitionLocationSequenceLocationCoordinateIntervalType",
    "MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystemType",
    "MolecularDefinitionLocationFeatureLocationType",
    "MolecularDefinitionRepresentationType",
    "MolecularDefinitionRepresentationLiteralType",
    "MolecularDefinitionRepresentationExtractedType",
    "MolecularDefinitionRepresentationRepeatedType",
    "MolecularDefinitionRepresentationConcatenatedType",
    "MolecularDefinitionRepresentationConcatenatedSequenceElementType",
    "MolecularDefinitionRepresentationRelativeType",
    "MolecularDefinitionRepresentationRelativeEditType",
]
