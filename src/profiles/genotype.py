#NOTE: This is a template, most likely will change 
# NOTE: Alpha 

from typing import ClassVar

from fhir.resources import fhirtypes
import resources.fhirtypesextra as fhirtypesextra

from pydantic import model_validator
from exceptions.fhir import ElementNotAllowedError,InvalidTypeError
from resources.moleculardefinition import MolecularDefinition


class Genotype(MolecularDefinition):
    location: ClassVar[fhirtypesextra.MolecularDefinitionLocationType | None]  # type: ignore
    representation: ClassVar[fhirtypesextra.MolecularDefinitionRepresentationType | None]  # type: ignore

    memberState: list[fhirtypes.ReferenceType] | None = Field(  # type: ignore
        None,
        alias="memberState",
        title="Member",
        description="A member or part of this molecule.",
        json_schema_extra={
            "element_property": True,
            # note: Listed Resource Type(s) should be allowed as Reference.
            "enum_reference_types": ["Allele","Haplotype"],
        },
    )

    @model_validator(mode="before")
    def validate_exclusions(cls, values):
        for field in ["location", "representation"]:
            if field in values and values[field] is not None:
                raise ElementNotAllowedError(f"`{field}` is not allowed in Genotype.")
        return values
    
    @model_validator(mode="after")
    def validate_type(cls, values):
        """Validates that the 'type' field is present and contains exactly one item.

        Args:
            values (BaseModel): The validated model instance.

        Raises:
            InvalidTypeError: If 'type' is missing or empty.

        Returns:
            BaseModel: The validated model instance if the check passes.

        """
        if not values.type or not values.type.model_dump(exclude_unset=True):
            raise InvalidTypeError(
                "The `type` field must contain exactly one item. `type` has a 1..1 cardinality for Genotype."
            )
        return values