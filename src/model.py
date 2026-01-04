"""
Model module - Elm-like architecture for braille applications
Contains generic data structures and state initialization patterns
Application-specific models should be defined in individual example files
"""

from library import print_property


# Example of a generic model initialization pattern
# Applications should define their own init() and get_message() functions
# based on their specific needs



def print_diagnostics(brl):
    """Print BrlAPI diagnostics information"""
    import brlapi
    import louis

    print_property("File Descriptor", str(brl.fileDescriptor))
    print_property("Server Host", str(brl.host))
    print_property("Authorization Schemes", str(brl.auth))
    print_property("Driver Name", str(brl.driverName))
    print_property("Model Identifier", str(brl.modelIdentifier))
    print_property("Display Width", str(brl.displaySize[0]))
    print_property("Display Height", str(brl.displaySize[1]))
    print_property(".......", ".........................")
    print_property("DOT1", str(brlapi.DOT1))
    print_property("DOT2", str(brlapi.DOT2))