from src.resource.moleculardefinition import MolecularDefinition
from pydantic import Field, model_validator
import typing
from fhir.resources import fhirtypes
import src.resource.fhirtypeextra as fhirtypeextra


class SequenceProfile(MolecularDefinition):
    """FHIR Sequence Profile

    Args:
        MolecularDefinition (MolecularDefinition): The base class for molecular definitions.

    Raises:
        ValueError: If `memberState` or `location` is included in the profile.

    Returns:
        SequenceProfile: An instance of the SequenceProfile class.
    """

    # Redefine `memberState` as a private attribute or exclude it
    memberState: typing.List[fhirtypes.ReferenceType] = Field(  # type: ignore
        default=None, repr=False, exclude=True
    )
    # Redefine `location` as a private attribute or exclude it
    location: typing.List[fhirtypeextra.MolecularDefinitionLocationType] = Field(  # type: ignore
        default=None, repr=False, exclude=True
    )

    # Combined validator to exclude both `memberState` and `location` during validation
    @model_validator(mode="before")
    def validate_exclusions(cls, values):
        for field in ["memberState", "location"]:
            if field in values:
                raise ValueError(f"`{field}` is not allowed in SequenceProfile.")
        return values

    # Override model_json_schema to remove `memberState` and `location`
    @classmethod
    def model_json_schema(cls, *args, **kwargs):
        schema = super().model_json_schema(*args, **kwargs)
        # Remove `memberState` and `location` from the schema if they exist
        if "properties" in schema:
            schema["properties"].pop("memberState", None)
            schema["properties"].pop("location", None)
        return schema

    @classmethod
    def elements_sequence(cls):
        """returning all elements names from
        ``MolecularDefinition`` according specification,
        with preserving original sequence order.
        """

        return [
            "identifier",
            "type",
            "representation",
        ]


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
            "type",
            "location",
            "representation",
        ]
