from typing import ClassVar

from fhir.resources import fhirtypes
from pydantic import model_validator

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


class Variation(MolecularDefinition):
    """FHIR Allele Profile

    Args:
        MolecularDefinition (MolecularDefinition): The base class for molecular definitions.

    Raises:
        ValueError: If `memberState` is included in the profile.

    Returns:
        Allele: An instance of the Allele class.

    """
    memberState: ClassVar[fhirtypes.ReferenceType| None] #type: ignore

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
        """Validates that the 'representation' field contains at least two item.

        Args:
            values (BaseModel): The validated model instance.

        Raises:
            RepresentationCardinalityError: If 'representation' is missing or empty.

        Returns:
            BaseModel: The validated model instance if the check passes.

        """
        reps = getattr(values, "representation", None) or []
        if len(reps) < 2:
            raise RepresentationCardinalityError(
                "The `representation` field must contain exactly one item. `representation` has a 2..* cardinality for Allele."

            )
        return values


    # @model_validator(mode="after")
    # def validate_focus(cls, values): TODO: keep working on this part
    #NOTE: potentially need to change allele validate_focus

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