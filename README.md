# WL Config Manager

A flexible configuration manager for Python applications that supports multiple file formats, environment variable overrides, and dot notation access.

## Features

- **Multiple Formats** - YAML, JSON, and INI configuration files
- **Dot Notation** - Access nested values with `config.server.port`
- **Environment Variables** - Override config values with environment variables
- **Default Values** - Built-in defaults with easy overrides
- **File Search** - Automatically find config files in standard locations
- **Validation** - Ensure required keys are present
- **CLI Tool** - Command-line interface for config manipulation
- **Type Conversion** - Automatic type conversion for environment variables
- **Live Reload** - Reload configuration without restarting

## Installation

```bash
pip install wl-config-manager
```

## Dependencies

- `wl_version_manager`
- `pyyaml>=5.1`

## Quick Start

### Basic Usage

```python
from wl_config_manager import ConfigManager

# Load config from file
config = ConfigManager(config_path="config.yaml")

# Access values with dot notation
port = config.server.port
debug = config.app.debug

# Or use get() method
database_url = config.get("database.url", default="sqlite:///app.db")
```

### Configuration File Example

```yaml
# config.yaml
app:
  name: "My Application"
  debug: false
  version: "1.0.0"

server:
  host: "0.0.0.0"
  port: 8080
  workers: 4

database:
  url: "postgresql://localhost/myapp"
  pool_size: 10
  echo: false

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

## Configuration Loading

### Search Paths

If no config path is specified, the manager searches these locations in order:

```python
from wl_config_manager import ConfigManager, DEFAULT_SEARCH_PATHS

# Default search paths on Fedora/CentOS:
# - ~/.config/
# - /etc/
# - /etc/app/
# - current working directory

# Use default search paths
config = ConfigManager(search_paths=DEFAULT_SEARCH_PATHS)

# Or specify custom search paths
config = ConfigManager(search_paths=["/opt/myapp", "/etc/myapp"])
```

### File Formats

The format is auto-detected by file extension, or can be specified:

```python
# Auto-detect format
config = ConfigManager(config_path="settings.json")  # JSON
config = ConfigManager(config_path="app.ini")       # INI
config = ConfigManager(config_path="config.yaml")   # YAML

# Explicitly specify format
config = ConfigManager(config_path="myconfig", format="yaml")
```

## Environment Variable Overrides

Override configuration values using environment variables:

```python
# Configure with env prefix
config = ConfigManager(
    config_path="config.yaml",
    env_prefix="MYAPP_"
)

# Environment variables override config file values
# MYAPP_SERVER__PORT=9000 overrides server.port
# MYAPP_APP__DEBUG=true overrides app.debug
# MYAPP_DATABASE__URL=postgres://prod-server/db overrides database.url
```

Environment variable rules:
- Prefix + double underscore (`__`) for nested values
- Values are automatically converted to appropriate types (bool, int, float, string)
- Case-insensitive (environment vars are converted to lowercase)

## Default Configuration

Provide default values that are used if not found in config file or environment:

```python
default_config = {
    "app": {
        "name": "DefaultApp",
        "debug": False
    },
    "server": {
        "port": 8080,
        "host": "localhost"
    }
}

config = ConfigManager(
    config_path="config.yaml",
    default_config=default_config
)
```

## Validation

Ensure required configuration keys are present:

```python
# Validate required keys
config = ConfigManager(
    config_path="config.yaml",
    required_keys=["app.name", "server.port", "database.url"]
)
# Raises ConfigValidationError if any required keys are missing
```

## Accessing Configuration Values

### Dot Notation Access

```python
# Direct attribute access
app_name = config.app.name
port = config.server.port

# Nested access
log_level = config.logging.level

# Safe access with get()
smtp_host = config.get("email.smtp.host", default="localhost")

# Get entire sections
server_config = config.server  # Returns namespace object
server_dict = config.get("server")  # Returns dict
```

### Dictionary-like Access

```python
# The configuration objects support dict-like operations
if "debug" in config.app:
    print(f"Debug mode: {config.app.debug}")

# Iterate over sections
for section, values in config:
    print(f"{section}: {values}")

# Get items from a section
for key, value in config.items("server"):
    print(f"{key} = {value}")
```

## Modifying Configuration

### Set Values

```python
# Set single value
config.set("app.version", "2.0.0")
config.set("server.port", 9000)

# Create nested structures
config.set("new_feature.enabled", True)
config.set("new_feature.options.timeout", 30)

# Update multiple values
config.update({
    "version": "2.0.0",
    "debug": True
})

# Update with prefix
config.update({"port": 9000, "workers": 8}, prefix="server")
```

### Save Configuration

```python
# Save to original file
config.save()

# Save to different file
config.save("new_config.yaml")

# Save in different format
config.save("config.json")  # Auto-converts to JSON
```

## Advanced Usage

### Reload Configuration

```python
# Reload from source file (picks up external changes)
config.reload()
```

### Create from Dictionary

```python
config_dict = {
    "app": {"name": "MyApp"},
    "server": {"port": 8080}
}

config = ConfigManager.from_dict(config_dict)
```

### Create from Environment Only

```python
# Load configuration entirely from environment variables
config = ConfigManager.from_env("MYAPP_")
```

### Logging Configuration

```python
# Set logging level for config manager
config = ConfigManager(
    config_path="config.yaml",
    log_level=logging.DEBUG  # See config loading details
)

# Set up file logging
from wl_config_manager import setup_file_logging

setup_file_logging(
    log_dir="/var/log",
    app_name="myapp",
    log_level=logging.INFO
)
```

## Command Line Interface

The package includes a CLI tool for managing configurations:

### View Configuration

```bash
# Get entire config
wl_config_manager get config.yaml

# Get specific value
wl_config_manager get config.yaml server.port

# Get with default
wl_config_manager get config.yaml app.missing --default="not found"

# Output as JSON
wl_config_manager get --format=json config.yaml
```

### Modify Configuration

```bash
# Set values
wl_config_manager set config.yaml app.debug true
wl_config_manager set config.yaml server.port 9000

# Create new config file
wl_config_manager create --format=yaml new_config.yaml

# Create from template
wl_config_manager create --template=default.yaml --vars='{"app":{"name":"MyApp"}}' config.yaml
```

### Validate Configuration

```bash
# Check required keys
wl_config_manager validate --required=app.name,server.port config.yaml
```

### Convert Formats

```bash
# Convert between formats
wl_config_manager convert config.ini config.yaml
wl_config_manager convert settings.yaml settings.json
```

### List Configuration

```bash
# List all values
wl_config_manager list config.yaml

# List section only
wl_config_manager list config.yaml --section=server
```

### Environment Variables

```bash
# Show config from environment variables
wl_config_manager env MYAPP_ --format=json
```

## Error Handling

The module provides specific exceptions for different error types:

```python
from wl_config_manager import (
    ConfigError,           # Base exception
    ConfigFileError,       # File not found/readable
    ConfigFormatError,     # Invalid file format
    ConfigValidationError  # Validation failures
)

try:
    config = ConfigManager(config_path="config.yaml")
except ConfigFileError as e:
    print(f"Config file error: {e}")
    print(f"File path: {e.file_path}")
except ConfigValidationError as e:
    print(f"Validation error: {e}")
    print(f"Missing keys: {e.get_missing_keys()}")
```

## Best Practices

1. **Use Environment Variables for Secrets**
   ```bash
   export MYAPP_DATABASE__PASSWORD="secret"
   export MYAPP_API__KEY="secret-key"
   ```

2. **Provide Sensible Defaults**
   ```python
   default_config = {
       "server": {"port": 8080, "host": "0.0.0.0"},
       "logging": {"level": "INFO"}
   }
   ```

3. **Validate Critical Configuration**
   ```python
   required_keys = ["database.url", "app.secret_key"]
   config = ConfigManager(required_keys=required_keys)
   ```

4. **Use Type Hints with Config Objects**
   ```python
   from typing import TYPE_CHECKING
   if TYPE_CHECKING:
       from types import SimpleNamespace
   
   def setup_server(server_config: SimpleNamespace):
       port = server_config.port
       host = server_config.host
   ```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.