# KeepMeUpdated Plugins

This is the official plugins repository for **KeepMeUpdated** - a powerful, self-hosted scheduling and notification platform.

KeepMeUpdated uses a dynamic plugin architecture that allows you to extend notification destinations without modifying the core backend codebase. This repository serves as the official registry for core plugins.

## Available Plugins

| Plugin | ID | Type | Description | File |
|---|---|---|---|---|
| **Gotify** | `gotify` | Channel | Send push notifications to a Gotify server. | [`gotify.py`](gotify.py) |
| **OpenWeatherMap** | `weather_owm` | Data Source | Provides live weather context variables like `{temperature}`. | [`weather.py`](weather.py) |
| **Apprise Meta-Channel** | `apprise` | Channel | Send notifications to hundreds of services simultaneously. | [`apprise_channel.py`](apprise_channel.py) |
| **MQTT (Home Assistant)** | `mqtt` | Channel | Publish payloads to an MQTT broker to trigger automations. | [`mqtt_channel.py`](mqtt_channel.py) |
| **Webhook (HTTP Request)** | `webhook` | Channel | Trigger external webhooks or APIs via GET/POST requests. | [`webhook_channel.py`](webhook_channel.py) |
| **CoinGecko Crypto** | `coingecko` | Data Source | Fetch live cryptocurrency prices and 24h changes. | [`coingecko_datasource.py`](coingecko_datasource.py) |
| **RSS / News Fetcher** | `rss_feed` | Data Source | Fetch the latest headline and summary from any RSS feed. | [`rss_datasource.py`](rss_datasource.py) |
| **Daily Inspiration** | `inspiration` | Data Source | Fetch a random or daily motivational quote via ZenQuotes. | [`inspiration_datasource.py`](inspiration_datasource.py) |
| **Google Assistant** | `google_assistant` | Channel | Play voice messages on Google Nest devices using text-to-speech. | [`google_assistant_channel.py`](google_assistant_channel.py) |

## How to Use in KeepMeUpdated

1. Open your KeepMeUpdated dashboard.
2. Navigate to the **Settings** -> **Plugin Repositories** section.
3. Add a new repository pointing to the URL where this repository's `registry.json` is hosted.
4. KeepMeUpdated will automatically fetch, load, and make the plugins available for your scheduled notifications!

### Plugin-Specific Prerequisites

Some plugins require specific environmental configurations when KeepMeUpdated is running in Docker:

- **Google Assistant (`google_assistant`)**: This plugin relies on mDNS (ZeroConf) to scan your local network for Cast devices. For the auto-discovery "Scan" feature to work, your KeepMeUpdated Docker containers must be run with `network_mode: "host"` so they can receive local network broadcasts. If you use the default Docker bridge network, discovery will fail, and you must manually enter the exact IP address of your Google Nest device in the "Device Name" field instead.

## Repository Structure

A KeepMeUpdated plugin repository consists of:

1. **`registry.json`**: A JSON file containing metadata about the available plugins, including their IDs, names, descriptions, versions, and relative file paths. KeepMeUpdated uses this to discover available plugins in the repository.
2. **Python Plugin Scripts** (e.g., `gotify.py`): Python files containing the plugin logic. These scripts inherit from `BaseNotificationChannel` and define the UI schemas and execution logic.

## Creating Your Own Plugin

KeepMeUpdated supports two types of plugins: **Channels** (for sending notifications) and **Data Sources** (for providing dynamic context variables).

To contribute a new plugin to this repository:

1. Create a new Python file (e.g., `my_plugin.py`).
2. Define a class that inherits from either `BaseNotificationChannel` or `BaseDataSourcePlugin` (imported from KeepMeUpdated core).
3. Implement the required schema methods:
   - `get_plugin_id()`: Returns a unique string ID.
   - `get_name()`: Returns the display name.
   - `get_config_schema()`: Returns a JSON schema for the plugin's configuration.
   - For Channels: `get_notification_schema()` Returns a schema for the notification payload.
   - For Data Sources: `get_context_schema()` Returns a list of provided variables.
4. Implement the execution logic:
   - `validate_config()`: Validates the user's saved configuration.
   - For Channels: `send(...)`: An `async` method that handles sending the notification.
   - For Data Sources: `fetch_context()`: An `async` method that returns a dictionary of variables.
5. Add an entry for your plugin in `registry.json`.

For more details on KeepMeUpdated and how the plugin architecture works, refer to the main KeepMeUpdated repository.
