import json
from copy import deepcopy
from typing import Any, Dict, TYPE_CHECKING, Tuple

from UM.Extension import Extension
from UM.Logger import Logger
from UM.i18n import i18nCatalog
from cura.CuraApplication import CuraApplication
from cura.Settings.CuraContainerStack import _ContainerIndexes

if TYPE_CHECKING:
    from cura.Settings.CuraContainerStack import CuraContainerStack

catalog = i18nCatalog("calibration")

VERSION_QT5 = False
try:
    from PyQt6.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot, QUrl
    from PyQt6.QtWidgets import QFileDialog
    from PyQt6.QtGui import QDesktopServices
except ImportError:
    from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot, QUrl
    from PyQt5.QtWidgets import QFileDialog
    from PyQt5.QtGui import QDesktopServices

    VERSION_QT5 = True


class SettingsExporter(QObject, Extension):
    def __init__(self, parent=None) -> None:
        QObject.__init__(self, parent)
        Extension.__init__(self)

        self.setMenuName(catalog.i18nc("@item:inmenu", "Settings Exporter"))
        self.addMenuItem(catalog.i18nc("@item:inmenu", "Export settings"), self.export)

    def export(self):
        # get global stack containing all settings
        global_stack: CuraContainerStack = CuraApplication.getInstance().getGlobalContainerStack()
        Logger.log("d", "Retrieving metadata and settings ...")

        # dict to save all settings
        settings = {"metadata": {},
                    "settings": {}}

        ########################################################################
        # Machine metadata
        ########################################################################
        # add metadata for global_stack (= "machine")
        global_stack_type = global_stack.getMetaDataEntry("type")
        settings["metadata"][global_stack_type] = deepcopy(global_stack.getMetaData())
        for key, value in settings["metadata"][global_stack_type].items():
            # convert all metadata to string
            settings["metadata"][global_stack_type][key] = str(value)

        ########################################################################
        # Extruder container stacks
        ########################################################################
        # get extruders
        extruder_list = global_stack.extruderList

        # add metadata and settings for each extruder
        settings["settings"]["extruders"] = {}
        settings["metadata"]["extruders"] = {}

        for i, extruder_stack in enumerate(extruder_list):
            metadata_dict, settings_dict = self.get_stack_data(extruder_stack)
            settings["metadata"]["extruders"][str(i)] = metadata_dict
            settings["settings"]["extruders"][str(i)] = settings_dict

        ########################################################################
        # Global container stack
        ########################################################################
        # get data from global container stack
        metadata_dict, settings_dict = self.get_stack_data(global_stack)
        settings["metadata"]["global"] = metadata_dict
        settings["settings"]["global"] = settings_dict

        Logger.log("d", "Export all settings to .json file ...")

        ########################################################################
        # Export as JSON
        ########################################################################

        file_name, _ = QFileDialog.getSaveFileName(None, "Save File", "", "JSON (*.json;)")
        if file_name:
            with open(file_name, 'w') as file:
                try:
                    json.dump(settings, file, indent=2)
                except TypeError:
                    Logger.log("e", "non json serializable object:")
                    Logger.log("e", str(settings))
                    return

        Logger.log("d", f"Settings exported to: {file_name}")

    def get_stack_data(self, container_stack: "CuraContainerStack") -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Get all data from this container stack and return it as a dictionary for metadata and settings.

        Args:
            container_stack (CuraContainerStack): A CuraContainerStack to unroll settings from

        Returns:
            dict: metadata
            dict: settings

        """
        metadata = {}
        settings = {"all": {}}

        # all data from this stack
        for key in container_stack.getAllKeys():
            settings["all"][key] = container_stack.getProperty(key, "value")

        # all containers inside the stack
        for i, container in enumerate(container_stack.getContainers()):
            # get the current container
            name = _ContainerIndexes.IndexTypeMap[i]

            # add metadata of this container
            metadata[name] = deepcopy(container.getMetaData())
            for key, value in metadata[name].items():
                # convert all metadata to string
                metadata[name][key] = str(value)

            # dict to save container settings
            settings[name] = {}
            # loop over all container settings
            for key in container.getAllKeys():
                # save settings with name and value in tmp dict
                settings[name][key] = str(container.getProperty(key, 'value'))

        return metadata, settings
