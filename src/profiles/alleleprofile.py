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
    #TODO: not sure if i need this anymore
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
    
    @model_validator(mode="after")
    def validate_moleculeType(cls, values):
        
        molType = values.moleculeType

        if not molType:
            raise ValueError(
                "The `moleculeType` field must not be empty (1..1 cardinality for AlleleProfile)."
            )
        return values

    @model_validator(mode="after")
    def validate_location_cardinality(cls, values):
        
        location = values.location

        if not location or len(location) != 1:
            raise ValueError(
                "The `location` field must contain exactly one item (1..1 cardinality for AlleleProfile)."
            )
        return values

    # @model_validator(mode="after")
    #this is going to be for ContextState and allelestate  
    
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
