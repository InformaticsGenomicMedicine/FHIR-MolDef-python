from fhir.resources import fhirtypes
from pydantic import Field, model_validator
from pydantic.json_schema import SkipJsonSchema

from exceptions.fhir import (
    InvalidMoleculeTypeError,
    LocationCardinalityError,
    MemberStateNotAllowedError,
    MissingAlleleStateError,
    MissingFocusCodingError,
    MultipleContextStateError,
    RepresentationCardinalityError,
)
from resources.moleculardefinition import MolecularDefinition


class Allele(MolecularDefinition):
    """FHIR Allele Profile

    Args:
        MolecularDefinition (MolecularDefinition): The base class for molecular definitions.

    Raises:
        ValueError: If `memberState` is included in the profile.

    Returns:
        Allele: An instance of the Allele class.

    """

    memberState: SkipJsonSchema[fhirtypes.ReferenceType] = Field(  # type: ignore
        default=None, repr=False, exclude=True
    )

    @model_validator(mode="before")
    def validate_memberState_exclusion(cls, values):
        """Validates that the 'memberState' field is not present in the input values.

        Args:
            values (dict): Dictionary of input values to validate.

        Raises:
            MemberStateNotAllowedError: If 'memberState' is present and not None.

        Returns:
            dict: The original input values if validation passes.

        """
        if "memberState" in values and values["memberState"] is not None:
            raise MemberStateNotAllowedError("`memberState` is not allowed in Allele.")
        return values

    @model_validator(mode="after")
    def validate_moleculeType(cls, values):
        """Validates that the 'moleculeType' field is present and contains exactly one item.

        Args:
            values (BaseModel): The validated model instance.

        Raises:
            InvalidMoleculeTypeError: If 'moleculeType' is missing or empty.

        Returns:
            BaseModel: The validated model instance if the check passes.

        """
        if not values.moleculeType or not values.moleculeType.model_dump(exclude_unset=True):
            raise InvalidMoleculeTypeError(
                "The `moleculeType` field must contain exactly one item. `moleculeType` has a 1..1 cardinality for Allele."
            )
        return values

    @model_validator(mode="after")
    def validate_location_cardinality(cls, values):
        """Validates that the 'location' field contains exactly one item.

        Args:
            values (BaseModel): The validated model instance.

        Raises:
            LocationCardinalityError: If 'location' is missing or contains more than one item.

        Returns:
            BaseModel: The validated model instance if the check passes.

        """
        if not values.location or len(values.location) > 1:
            raise LocationCardinalityError(
                "The `location` field must contain exactly one item. `location` has a 1..1 cardinality for Allele."
            )
        return values

    @model_validator(mode="after")
    def validate_representation_cardinality(cls, values):
        """Validates that the 'representation' field contains at least one item.

        Args:
            values (BaseModel): The validated model instance.

        Raises:
            RepresentationCardinalityError: If 'representation' is missing or empty.

        Returns:
            BaseModel: The validated model instance if the check passes.

        """
        if not values.representation:
            raise RepresentationCardinalityError(
                "The `representation` field must contain exactly one item. `representation` has a 1..* cardinality for Allele."

            )
        return values

    @model_validator(mode="after")
    def validate_focus(cls, values):
        """Validates the structure and contents of the 'focus' field within each representation.

        Args:
            values (BaseModel): The validated model instance.

        Raises:
            MissingFocusCodingError: If focus.coding is missing or empty, or if any allele-state or context-state coding lacks a system.
            MissingAlleleStateError: If no 'allele-state' codings are found.
            MultipleContextStateError: If more than one 'context-state' coding is present.

        Returns:
            BaseModel: The validated model instance if all constraints pass.

        """
        allele_state = []
        context_state = []

        for value in values.representation:
            if value.focus:
                if not value.focus.coding:
                    raise MissingFocusCodingError("The 'focus.coding' field must contain at least one entry.")

                for coding in value.focus.coding:
                    if coding.code == "allele-state":
                        allele_state.append(coding)

                        if not coding.system:
                            raise MissingFocusCodingError("Each 'allele-state' coding entry must have a 'system' defined.")

                    elif coding.code == "context-state":
                        context_state.append(coding)

                        if not coding.system:
                            raise MissingFocusCodingError("Each 'context-state' coding entry must have a 'system' defined.")

        if len(allele_state) == 0:
            raise MissingAlleleStateError("At least one 'allele-state' must be present in 'focus.coding'.")

        if len(context_state) > 1:
            raise MultipleContextStateError("Only one 'context-state' is allowed (0..1 cardinality).")

        return values

    @classmethod
    def elements_sequence(cls):
        """Returning all elements names from `MolecularDefinition`,
        excluding `memberState`.
        """
        return [
            "id",
            "meta",
            "implicitRules",
            "language",
            "text",
            "contained",
            "extension",
            "modifierExtension",
            "identifier",
            "description",
            "moleculeType",
            "location",
            "representation",
        ]
