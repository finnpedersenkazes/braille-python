"""
Model module - Elm-like architecture for braille applications
Contains generic data structures and state initialization patterns
Application-specific models should be defined in individual example files
"""

from library import printProperty


# Example of a generic model initialization pattern
# Applications should define their own init() and getMessage() functions
# based on their specific needs



def printDiagnostics(brl):
    """Print BrlAPI diagnostics information"""
    import brlapi
    import louis

    printProperty("File Descriptor", str(brl.fileDescriptor))
    printProperty("Server Host", str(brl.host))
    printProperty("Authorization Schemes", str(brl.auth))
    printProperty("Driver Name", str(brl.driverName))
    printProperty("Model Identifier", str(brl.modelIdentifier))
    printProperty("Display Width", str(brl.displaySize[0]))
    printProperty("Display Height", str(brl.displaySize[1]))
    printProperty(".......", ".........................")
    printProperty("DOT1", str(brlapi.DOT1))
    printProperty("DOT2", str(brlapi.DOT2))