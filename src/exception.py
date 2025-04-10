# API Class
class SeqRepoDataProxyCreationError(Exception):
    """Exception raised for errors in translate HGVS expressions."""

    pass

# FHIR Classes

class FHIRException(Exception):
    """Base exception for FHIR-related errors."""

    pass

class ElementNotAllowedError(FHIRException):
    """Raised when a certain field is disallowed in a profile."""

    pass

class MemberStateNotAllowedError(FHIRException):
    """Raised when 'memberState' is set in AlleleProfile but should not be."""

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

# Allele Utils

class InvalidVRSAlleleError(Exception):
    """Raised when the expression is not a valid VRS Allele."""
    pass

class InvalidAlleleProfileError(Exception):
    """Raised when the expression is not a valid AlleleProfile."""
    pass

class InvalidSequenceTypeError(Exception):
    """Raised when the RefSeq identifier has an unrecognized prefix."""
    pass

class InvalidAccessionError(Exception):
    """Raised when the provided RefSeq ID does not match the expected format."""
    pass

class InvalidCoordinateSystemError(Exception):
    """Raised when an invalid coordinate system is specified."""
    pass
