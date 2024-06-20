import json

from UM.Extension import Extension
from UM.Logger import Logger
from UM.i18n import i18nCatalog
from cura.CuraApplication import CuraApplication
from cura.Settings.CuraContainerStack import _ContainerIndexes

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
        # get global stakc containing all settings
        global_stack = CuraApplication.getInstance().getGlobalContainerStack()
        Logger.log("d", "Retrieving metadata and settings ...")

        # dict to save all settings
        settings = {"metadata": {},
                    "settings": {}}

        # add metadata for global_stack (= "machine")
        global_stack_type = global_stack.getMetaDataEntry("type")
        settings["metadata"][global_stack_type] = global_stack.getMetaData()
        for key, value in settings["metadata"][global_stack_type].items():
            # convert all metadata to string
            settings["metadata"][global_stack_type][key] = str(value)

        # get all setting keys
        all_setting_keys = global_stack.getAllKeys()

        # add resolved settings to "all_settings" key
        settings["settings"]["all_settings"] = {}
        for key in all_setting_keys:
            settings["settings"]["all_settings"][key] = global_stack.getProperty(key, "value")

        # loop over all containers in the global stack to get the individual settings
        for index, name in _ContainerIndexes.IndexTypeMap.items():
            # get the current container
            container = global_stack.getContainer(index)

            # add metadata of this container
            settings["metadata"][name] = container.getMetaData()
            for key, value in settings["metadata"][name].items():
                # convert all metadata to string
                settings["metadata"][name][key] = str(value)

            # dict to save container settings
            settings["settings"][name] = {}
            # loop over all container settings
            for key in container.getAllKeys():
                # save settings with name and value in tmp dict
                settings["settings"][name][key] = str(container.getProperty(key, 'value'))

        Logger.log("d", "Export all settings to .json file ...")

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
