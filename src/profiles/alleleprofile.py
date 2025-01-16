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

    @model_validator(mode="before")
    def validate_memberState_exclusion(cls, values):
        if "memberState" in values:
            raise ValueError("`memberState` is not allowed in AlleleProfile.")
        return values
    
    @model_validator(mode="after")
    def validate_moleculeType(cls, values):
        if not values.moleculeType:
            raise ValueError(
                "The `moleculeType` field must contain exactly one item. `moleculeType` has a 1..1 cardinality for AlleleProfile."
            )
        return values

    @model_validator(mode="after")
    def validate_location_cardinality(cls, values):
        if not values.location: #
            raise ValueError(
                "The `location` field must contain exactly one item. `location` has a 1..1 cardinality for AlleleProfile."
            )
        return values
    
    @model_validator(mode="after")
    def validate_representation_cardinality(cls, values):
        
        if not values.representation: 
            raise ValueError(
                "The `representation` field must contain exactly one item. `representation` has a 1..* cardinality for AlleleProfile."

            )
        return values

    @model_validator(mode="after")
    def validate_focus(cls, values):
        allele_state = []
        context_state = []

        for value in values.representation:
            if value.focus:
                if not value.focus.coding:
                    raise ValueError("The 'focus.coding' field must contain at least one entry.")

                for coding in value.focus.coding:
                    if coding.code == "allele-state":
                        allele_state.append(coding)

                        if not coding.system:
                            raise ValueError("Each 'allele-state' coding entry must have a 'system' defined.")

                    elif coding.code == "context-state":
                        context_state.append(coding)

                        if not coding.system:
                            raise ValueError("Each 'context-state' coding entry must have a 'system' defined.")

        if len(allele_state) == 0:
            raise ValueError("At least one 'allele-state' must be present in 'focus.coding'.")

        if len(context_state) > 1:
            raise ValueError("Only one 'context-state' is allowed (0..1 cardinality).")

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
