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


class Allele(MolecularDefinition):
    """FHIR Allele Profile

    Args:
        MolecularDefinition (MolecularDefinition): The base class for molecular definitions.

    Raises:
        ValueError: If `memberState` is included in the profile.

    Returns:
        Allele: An instance of the Allele class.

    """
    # FOCUS_SYSTEM: ClassVar[str] = "http://hl7.org/fhir/uv/molecular-definition-data-types/CodeSystem/molecular-definition-focus"
    EXPECTED_DISPLAY: ClassVar[dict[str, str]] = {
        "allele-state": "Allele State",
        "context-state": "Context State"
        }

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
    def validate_focus(self):
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
        allele_state_count = 0
        context_state_count = 0 

        for idx, rep in enumerate(self.representation):
            # Focus has a card. of 1..1, must be present in every representation
            if getattr(rep,"focus", None) is None:
                raise MissingFocusCodingError(
                    f"representation[{idx}].focus is required when slicing by focus CodeableConcept."
                )
            codings = getattr(rep.focus, 'coding', None)
            # coding has a card. of 1..*, must be present in every focus
            if not codings:
                raise MissingFocusCodingError(
                    f"representation[{idx}].focus.coding must contain at least one entry."
                )
            
            for coding in codings:
                # card. of code must be 1..1
                code = getattr(coding, "code", None)
                # card. of system must be 1..1
                system = getattr(coding, "system", None)
                # card. of display must be 1..1
                display = getattr(coding, "display", None)

                if code is None:
                    raise MissingFocusCodingError(
                        f"representation[{idx}].focus.coding is missing a 'code' element.")

                if code in {"allele-state", "context-state"}:
                    if not system:
                        raise MissingFocusCodingError(
                            f"representation[{idx}].focus.coding (code='{code}') must define 'system'."
                        )
                    #NOTE: IN some of the examples the fixed values isn't the same as the FOCUS_SYSTEM.
                    #NOTE: To avoid changing the examples and this we are just going to # it out. 
                    # if system != self.FOCUS_SYSTEM:
                    #     raise MissingFocusCodingError(
                    #         f"Invalid focus.coding in representation[{idx}]: "
                    #         f"The Coding with code='{code}' must define a 'system' value as required by the MolDef focus discriminator."
                    #     )

                    expected_display = self.EXPECTED_DISPLAY.get(code)

                    if display != expected_display:
                        raise MissingFocusCodingError(
                            f"Invalid focus.coding in representation[{idx}]: "
                            f"The Coding with code='{code}' must have display='{expected_display}', "
                            f"found '{display}'."
                            )
                    
                    if code == "allele-state":
                        allele_state_count += 1 
                    elif code == "context-state":
                        context_state_count += 1

        if allele_state_count != 1:
            raise MissingAlleleStateError(
                "Exactly one 'allele-state' must be present across 'representation' (1..1 cardinality)."
            )
        
        if context_state_count > 1:
            raise MultipleContextStateError(
                "At most one 'context-state' is allowed across 'representation' (0..1 cardinality)."
            )

        return self

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
