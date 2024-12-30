from moldefresource.moleculardefinition import MolecularDefinition
from pydantic import Field, model_validator
import typing
from fhir.resources import fhirtypes

class AlleleProfile(MolecularDefinition):
    """FHIR Allele Profile

    Args:
        MolecularDefinition (MolecularDefinition): The base class for molecular definitions.

    Raises:
        ValueError: If `memberState` is included in the profile.

    Returns:
        AlleleProfile: An instance of the AlleleProfile class.
    """

    # Redefine `memberState` as a private attribute or exclude it
    memberState: typing.List[fhirtypes.ReferenceType] = Field(  # type: ignore
        default=None, repr=False, exclude=True
    )

    # Add a model_validator to ensure `memberState` is excluded
    @model_validator(mode="before")
    def validate_memberState_exclusion(cls, values):
        if "memberState" in values:
            raise ValueError("`memberState` is not allowed in AlleleProfile.")
        return values

    @classmethod
    def model_json_schema(cls, *args, **kwargs):
        schema = super().model_json_schema(*args, **kwargs)
        # Remove `memberState` from the schema if it exists
        if "properties" in schema and "memberState" in schema["properties"]:
            del schema["properties"]["memberState"]
        return schema

    @classmethod
    def elements_sequence(cls):
        """Returning all elements names from `MolecularDefinition`,
        excluding `memberState`.
        """
        return [
            "identifier",
            "moleculeType",
            "location",
            "representation",
        ]
