# Settings Exporter for Cura

This repository contains a Cura plugin to export the current Cura settings to a .json file.\
This allows profiles to be exported from Cura and used via the Command Line Interface with the CuraEngine.

## Install

- Clone repository
- Copy repository content into `cura\x.x\plugins\SettingsExport\SettingsExport`
- Restart Cura

## Usage

Extensions → Settings Exporter → Export Settings → Pick location and name of the export file

## Structure of the output

Print settings are located in `settings` → `extruders` → `<extruder_nr>` → `all`\
Additional metadata and the settings tree are also exported, including the formulas used to calculate the values.

```json
{
  "metadata": {
    "global": {
      "machine": {...},
      "user": {...},
      "quality_changes": {...},
      "intent": {...},
      "quality": {...},
      "material": {...},
      "variant": {...},
      "definition_changes": {...},
      "definition": {...}
    },
    "extruders": {
      "0": {
        "extruder_train": {...},
        "user": {...},
        "quality_changes": {...},
        "intent": {...},
        "quality": {...},
        "material": {...},
        "variant": {...},
        "definition_changes": {...},
        "definition": {...}
      }
      "1": {
        ...
      }
      ...
    }
  },
  "settings": {
    "global": {
      "all": {...},
      "user": {...},
      "quality_changes": {...},
      "intent": {...},
      "quality": {...},
      "material": {...},
      "variant": {...},
      "definition_changes": {...},
      "definition": {...}
    },
    "extruders": {
      "0": {
        "all": {...},
        "user": {...},
        "quality_changes": {...},
        "intent": {...},
        "quality": {...},
        "material": {...},
        "variant": {...},
        "definition_changes": {...},
        "definition": {...}
      }
      "1": {
        ...
      }
      ...
    }
  }
}
```