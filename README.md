# KeepMeUpdated Plugins

This is the official plugins repository for **KeepMeUpdated** - a powerful, self-hosted scheduling and notification platform.

KeepMeUpdated uses a dynamic plugin architecture that allows you to extend notification destinations without modifying the core backend codebase. This repository serves as the official registry for core plugins.

## Available Plugins

| Plugin | ID | Description | File |
|---|---|---|---|
| **Gotify** | `gotify` | Send push notifications to a Gotify server. | [`gotify.py`](gotify.py) |

## How to Use in KeepMeUpdated

1. Open your KeepMeUpdated dashboard.
2. Navigate to the **Settings** -> **Plugin Repositories** section.
3. Add a new repository pointing to the URL where this repository's `registry.json` is hosted.
4. KeepMeUpdated will automatically fetch, load, and make the plugins available for your scheduled notifications!

## Repository Structure

A KeepMeUpdated plugin repository consists of:

1. **`registry.json`**: A JSON file containing metadata about the available plugins, including their IDs, names, descriptions, versions, and relative file paths. KeepMeUpdated uses this to discover available plugins in the repository.
2. **Python Plugin Scripts** (e.g., `gotify.py`): Python files containing the plugin logic. These scripts inherit from `BaseNotificationChannel` and define the UI schemas and execution logic.

## Creating Your Own Plugin

To contribute a new plugin to this repository:

1. Create a new Python file (e.g., `my_channel.py`).
2. Define a class that inherits from `BaseNotificationChannel` (imported from KeepMeUpdated core).
3. Implement the following required methods:
   - `get_plugin_id()`: Returns a unique string ID.
   - `get_name()`: Returns the display name.
   - `get_config_schema()`: Returns a JSON schema for the channel configuration.
   - `get_notification_schema()`: Returns a JSON schema for the notification payload.
4. Implement the execution logic:
   - `validate_config()`: Validates the user's saved configuration.
   - `send(...)`: An `async` method that handles sending the notification.
5. Add an entry for your plugin in `registry.json`.

For more details on KeepMeUpdated and how the plugin architecture works, refer to the main KeepMeUpdated repository.
