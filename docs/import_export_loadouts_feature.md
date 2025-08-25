# Import/Export Loadouts Feature

## Overview
This feature will enable users to export all their custom stratagem loadouts to a JSON file and import loadouts from a JSON file. This provides a convenient way to back up loadouts, transfer them between installations, or share them with other users.

## Goals
*   Provide a mechanism to export all current custom loadouts to a user-specified JSON file.
*   Provide a mechanism to import loadouts from a user-selected JSON file, completely replacing existing custom loadouts.
*   Ensure data integrity during import by validating the JSON file format.
*   Integrate import/export options intuitively within the existing UI.

## User Stories
*   **As a user, I want to export all my custom loadouts** so that I can back them up or share them with friends.
*   **As a user, I want to import a set of loadouts from a file** so that I can restore my saved loadouts or use loadouts shared by others.
*   **As a user, I want to be notified if an imported loadout file is invalid** so that I understand why my loadouts were not updated.

## Acceptance Criteria
*   A new UI element (e.g., button) is available to trigger the export of all custom loadouts.
*   Upon export, a JSON file containing all custom loadout names and their associated stratagem IDs/keys is created at a user-specified location.
*   A new UI element (e.g., button) is available to trigger the import of loadouts.
*   Upon successful import, all existing custom loadouts are replaced by the loadouts from the selected JSON file.
*   If the imported JSON file is malformed or does not contain valid loadout data, an error message is displayed, and the existing loadouts remain unchanged.
*   The UI automatically refreshes to display the newly imported loadouts after a successful import.
*   The feature exclusively handles all loadouts; no partial import/export is supported.
*   The exported/imported file format is standard JSON with a `.json` extension.
