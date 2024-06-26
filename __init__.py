from . import SettingsExporter

from UM.i18n import i18nCatalog

catalog = i18nCatalog("cura")


##  Defines additional metadata for the plug-in.
#
#   File reader type plug-ins must specify some additional metadata as to which
#   types of files they are able to read.
#   Some types of plug-ins require additional metadata, such as which file types
#   they are able to read or the name of the tool they define. In the case of
#   the "Extension" type plug-in, there is no additional metadata though.
def getMetaData():
    return {}


##  Lets Uranium know that this plug-in exists.
#
#   This is called when starting the application to find out which plug-ins
#   exist and what their types are. We need to return a dictionary mapping from
#   strings representing plug-in types (in this case "extension") to objects
#   that inherit from PluginObject.
#
#   \param app The application that the plug-in needs to register with.
def register(app):
    return {"extension": SettingsExporter.SettingsExporter()}
