class FHIRException(Exception):
    """Base exception for FHIR-related errors."""

    pass

class ElementNotAllowedError(FHIRException):
    """Raised when a certain field is disallowed in a profile."""

    pass

class MemberStateNotAllowedError(FHIRException):
    """Raised when 'memberState' is set in Allele but should not be."""

    pass

class InvalidMoleculeTypeError(FHIRException):
    """Raised when 'moleculeType' does not meet its 1..1 cardinality requirement."""

    pass

class LocationCardinalityError(FHIRException):
    """Raised when 'location' does not meet its 1..1 cardinality requirement."""

    pass

class RepresentationCardinalityError(FHIRException):
    """Raised when 'representation' does not meet its 1..* cardinality requirement."""

    pass

class MissingFocusCodingError(FHIRException):
    """Raised when 'focus.coding' is missing or improperly defined in representation."""

    pass

class MissingAlleleStateError(FHIRException):
    """Raised when at least one 'allele-state' coding is not present in 'focus.coding'."""

    pass

class MultipleContextStateError(FHIRException):
    """Raised when more than one 'context-state' coding is present in 'focus.coding'."""

    pass
