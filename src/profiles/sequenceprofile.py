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
