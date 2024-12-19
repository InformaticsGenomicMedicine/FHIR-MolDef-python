from __future__ import annotations as _annotations
from fhir_core.types import create_fhir_type


MolecularDefinitionType = create_fhir_type(
    "MolecularDefinitionType",
    "src.resource.moleculardefinition.MolecularDefinition",
)

MolecularDefinitionLocationType = create_fhir_type(
    "MolecularDefinitionLocationType",
    "src.resource.moleculardefinition.MolecularDefinitionLocation",
)

MolecularDefinitionLocationSequenceLocationType = create_fhir_type(
    "MolecularDefinitionLocationSequenceLocationType",
    "src.resource.moleculardefinition.MolecularDefinitionLocationSequenceLocation",
)

MolecularDefinitionLocationSequenceLocationCoordinateIntervalType = create_fhir_type(
    "MolecularDefinitionLocationSequenceLocationCoordinateIntervalType",
    "src.resource.moleculardefinition.MolecularDefinitionLocationSequenceLocationCoordinateInterval",
)

MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystemType = create_fhir_type(
    "MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystemType",
    "src.resource.moleculardefinition.MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystem",
)

MolecularDefinitionLocationFeatureLocationType = create_fhir_type(
    "MolecularDefinitionLocationFeatureLocationType",
    "src.resource.moleculardefinition.MolecularDefinitionLocationFeatureLocation",
)

MolecularDefinitionRepresentationType = create_fhir_type(
    "MolecularDefinitionRepresentationType",
    "src.resource.moleculardefinition.MolecularDefinitionRepresentation",
)

MolecularDefinitionRepresentationLiteralType = create_fhir_type(
    "MolecularDefinitionRepresentationLiteralType",
    "src.resource.moleculardefinition.MolecularDefinitionRepresentationLiteral",
)

MolecularDefinitionRepresentationExtractedType = create_fhir_type(
    "MolecularDefinitionRepresentationExtractedType",
    "src.resource.moleculardefinition.MolecularDefinitionRepresentationExtracted",
)

MolecularDefinitionRepresentationRepeatedType = create_fhir_type(
    "MolecularDefinitionRepresentationRepeatedType",
    "src.resource.moleculardefinition.MolecularDefinitionRepresentationRepeated",
)

MolecularDefinitionRepresentationConcatenatedType = create_fhir_type(
    "MolecularDefinitionRepresentationConcatenatedType",
    "src.resource.moleculardefinition.MolecularDefinitionRepresentationConcatenated",
)

MolecularDefinitionRepresentationConcatenatedSequenceElementType = create_fhir_type(
    "MolecularDefinitionRepresentationConcatenatedSequenceElementType",
    "src.resource.moleculardefinition.MolecularDefinitionRepresentationConcatenatedSequenceElement",
)

MolecularDefinitionRepresentationRelativeType = create_fhir_type(
    "MolecularDefinitionRepresentationRelativeType",
    "src.resource.moleculardefinition.MolecularDefinitionRepresentationRelative",
)

MolecularDefinitionRepresentationRelativeEditType = create_fhir_type(
    "MolecularDefinitionRepresentationRelativeEditType",
    "src.resource.moleculardefinition.MolecularDefinitionRepresentationRelativeEdit",
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
