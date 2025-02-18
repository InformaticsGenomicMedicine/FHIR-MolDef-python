from pydantic import Field, model_validator
from fhir.resources import fhirtypes
from moldefresource.moleculardefinition import MolecularDefinition
import moldefresource.fhirtypeextra as fhirtypeextra
from pydantic.json_schema import SkipJsonSchema
from exception import ElementNotAllowedError,InvalidMoleculeTypeError

class SequenceProfile(MolecularDefinition):
    """FHIR Sequence Profile

    Args:
        MolecularDefinition (MolecularDefinition): The base class for molecular definitions.

    Raises:
        ValueError: If `memberState` or `location` is included in the profile.

    Returns:
        SequenceProfile: An instance of the SequenceProfile class.
    """
    #https://github.com/pydantic/pydantic/discussions/6699#discussioncomment-8642547 (H-G-11 comment)
    memberState: SkipJsonSchema[fhirtypes.ReferenceType] = Field(  # type: ignore
        default=None, repr=False, exclude=True
    )

    location: SkipJsonSchema[fhirtypeextra.MolecularDefinitionLocationType] = Field(  # type: ignore
        default=None, repr=False, exclude=True
    )

    # Combined validator to exclude both `memberState` and `location` during validation
    @model_validator(mode="before")
    def validate_exclusions(cls, values):
        for field in ["memberState", "location"]:
            if field in values:
                raise ElementNotAllowedError(f"`{field}` is not allowed in SequenceProfile.")
        return values

    @model_validator(mode="after")
    def validate_moleculeType(cls, values):
        if not values.moleculeType or not values.moleculeType.model_dump(exclude_unset=True):
            raise InvalidMoleculeTypeError(
                "The `moleculeType` field must contain exactly one item. `moleculeType` has a 1..1 cardinality for SequenceProfile."
            )
        return values

    @classmethod
    def elements_sequence(cls):
        """returning all elements names from
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
