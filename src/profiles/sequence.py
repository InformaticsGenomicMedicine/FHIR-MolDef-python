from typing import ClassVar

from fhir.resources import fhirtypes
from pydantic import model_validator

import resources.fhirtypesextra as fhirtypesextra
from exceptions.fhir import ElementNotAllowedError, InvalidMoleculeTypeError
from resources.moleculardefinition import MolecularDefinition


class Sequence(MolecularDefinition):
    """FHIR Sequence Profile

    Args:
        MolecularDefinition (MolecularDefinition): The base class for molecular definitions.

    Raises:
        ValueError: If `memberState` or `location` is included in the profile.

    Returns:
        Sequence: An instance of the Sequence class.

    """
    memberState: ClassVar[fhirtypes.ReferenceType | None] #type: ignore
    location: ClassVar[fhirtypesextra.MolecularDefinitionLocationType| None]  # type: ignore

    # Combined validator to exclude both `memberState` and `location` during validation
    @model_validator(mode="before")
    def validate_exclusions(cls, values):
        for field in ["memberState", "location"]:
            if field in values and values[field] is not None:
                raise ElementNotAllowedError(f"`{field}` is not allowed in Sequence.")
        return values

    @model_validator(mode="after")
    def validate_moleculeType(cls, values):
        if not values.moleculeType or not values.moleculeType.model_dump(exclude_unset=True):
            raise InvalidMoleculeTypeError(
                "The `moleculeType` field must contain exactly one item. `moleculeType` has a 1..1 cardinality for Sequence."
            )
        return values

    @classmethod
    def elements_sequence(cls):
        """Returning all elements names from
        ``MolecularDefinition`` according specification,
        with preserving original sequence order.
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
            "moleculeType",
            "representation",
        ]
