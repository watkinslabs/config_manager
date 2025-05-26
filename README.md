# WL Config Manager

A flexible configuration manager for Python applications supporting multiple file formats, environment variable overrides, and dot notation access.

## Features

- **Multiple Formats**: YAML, JSON, and INI support
- **Environment Variables**: Override config values with env vars
- **Dot Notation**: Access nested config values with simple syntax
- **Default Values**: Merge user config with application defaults
- **Validation**: Ensure required keys are present
- **Auto-Discovery**: Find config files in standard locations
- **CLI Tools**: Command-line utilities for config management
- **Logging Integration**: Built-in logging support

## Installation

```bash
pip install wl_config_manager
```

## Quick Start

```python
from wl_config_manager import ConfigManager

# Load configuration with defaults
default_config = {
    'app': {
        'name': 'MyApp',
        'debug': False
    },
    'server': {
        'host': '127.0.0.1',
        'port': 8080
    }
}

config = ConfigManager(
    config_path='config.yaml',
    default_config=default_config,
    env_prefix='MYAPP_',
    required_keys=['app.name', 'server.host']
)

# Access with dot notation
print(config.app.name)
print(config.server.port)

# Get with fallback
debug_mode = config.get('app.debug', False)

# Modify values
config.set('app.version', '2.0.0')
config.save('updated_config.yaml')
```

## Configuration Files

### YAML Example
```yaml
app:
  name: MyApp
  version: 1.0.0
  debug: true

server:
  host: 0.0.0.0
  port: 8080
  timeout: 30

database:
  url: sqlite:///app.db
  pool_size: 5
```

### JSON Example
```json
{
  "app": {
    "name": "MyApp",
    "version": "1.0.0",
    "debug": true
  },
  "server": {
    "host": "0.0.0.0",
    "port": 8080,
    "timeout": 30
  }
}
```

## Environment Variables

Override config values using environment variables with your chosen prefix:

```bash
export MYAPP_SERVER__HOST=0.0.0.0
export MYAPP_SERVER__PORT=9000
export MYAPP_APP__DEBUG=true
```

Use double underscores (`__`) for nested values.

## Advanced Usage

### Search Paths
```python
search_paths = [
    os.path.expanduser('~/.config/myapp'),
    '/etc/myapp',
    os.getcwd()
]

config = ConfigManager(search_paths=search_paths)
```

### Validation
```python
config = ConfigManager(
    config_path='config.yaml',
    required_keys=['database.url', 'api.key', 'server.port']
)
```

### Multiple Updates
```python
updates = {
    'app': {
        'name': 'UpdatedApp',
        'version': '2.0.0'
    },
    'features': {
        'cache_enabled': True
    }
}
config.update(updates)
```

### Class Methods
```python
# From dictionary
config = ConfigManager.from_dict({
    'app': {'name': 'DictApp'}
})

# From environment only
config = ConfigManager.from_env('MYAPP_')
```

## Command Line Interface

The package includes a powerful CLI for config management:

```bash
# Get configuration values
wl_config_manager get config.yaml app.name
wl_config_manager get config.yaml server --format=json

# Set values
wl_config_manager set config.yaml app.debug true
wl_config_manager set config.yaml new.nested.value 42

# Create new config
wl_config_manager create new_config.yaml --vars='{"app.name":"NewApp"}'

# Validate configuration
wl_config_manager validate config.yaml --required=app.name,server.port

# Convert between formats
wl_config_manager convert config.yaml config.json

# List all values
wl_config_manager list config.yaml --section=server

# Environment variables to config
wl_config_manager env MYAPP_ --format=yaml
```

## Error Handling

The package provides specific exception types for different error conditions:

```python
from wl_config_manager import ConfigManager
from wl_config_manager.errors import (
    ConfigError,
    ConfigFileError, 
    ConfigFormatError,
    ConfigValidationError
)

try:
    config = ConfigManager(
        config_path='config.yaml',
        required_keys=['missing.key']
    )
except ConfigFileError as e:
    print(f"File error: {e}")
except ConfigValidationError as e:
    print(f"Missing keys: {e.get_missing_keys()}")
except ConfigError as e:
    print(f"General config error: {e}")
```

## Logging

Enable detailed logging for debugging:

```python
import logging
from wl_config_manager import setup_file_logging

# File logging (when running as root)
if os.geteuid() == 0:
    setup_file_logging(app_name='myapp')

# Or configure log level
config = ConfigManager(
    config_path='config.yaml',
    log_level=logging.DEBUG
)
```

## API Reference

### ConfigManager Class

#### Constructor Parameters
- `config_path`: Path to configuration file
- `default_config`: Dictionary of default values
- `env_prefix`: Environment variable prefix
- `search_paths`: List of paths to search for config files
- `format`: Force specific format ('yaml', 'json', 'ini')
- `required_keys`: List of required configuration keys
- `log_level`: Logging verbosity level

#### Methods
- `get(key=None, default=None)`: Get configuration value
- `set(key, value)`: Set configuration value
- `update(data, prefix=None)`: Update multiple values
- `save(config_path=None)`: Save configuration to file
- `reload()`: Reload from source file
- `get_config()`: Get entire config as dictionary
- `items(section=None)`: Get key-value pairs

#### Class Methods
- `from_dict(config_dict, **kwargs)`: Create from dictionary
- `from_env(env_prefix, **kwargs)`: Create from environment variables

## Testing

Run the test suite:

```bash
# Install development dependencies
pip install pytest pyyaml

# Run tests
pytest tests/

# Run with coverage
pytest --cov=wl_config_manager tests/
```

## License

BSD 3-Clause License

## Changelog

### Version 1.0.0
- Initial release
- Support for YAML, JSON, and INI formats
- Environment variable overrides
- Dot notation access
- CLI tools
- Comprehensive test suite