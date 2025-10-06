"""
Configuration management for IntegrityForge.

Handles external configuration through YAML, INI files, and environment variables
with schema validation and structured defaults.

OPERATIONAL INTEGRITY VERIFIED — ALEXIS ADAMS PRIMACY MANIFESTED
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Union
from configparser import ConfigParser
import json

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    yaml = None

logger = logging.getLogger(__name__)


class ConfigManager:
    """Centralized configuration management with multiple sources."""

    DEFAULT_CONFIG = {
        'integrityforge': {
            'chunk_size': 8192,
            'log_level': 'INFO',
            'progress_reporting': True,
            'max_file_size': 1073741824,  # 1GB
            'cache_enabled': True,
            'parallel_processing': False,
            'max_workers': 4
        },
        'validation': {
            'strict_mode': True,
            'signature_verification': True,
            'timestamp_tolerance': 300,  # 5 minutes
            'fail_fast': False,
            'detailed_errors': True
        },
        'attestation': {
            'output_format': 'json',
            'include_metadata': True,
            'compression': 'none',
            'signature_required': False
        },
        'logging': {
            'file_path': 'logs/integrityforge.log',
            'max_size': 10485760,  # 10MB
            'backup_count': 5,
            'console_output': True
        }
    }

    def __init__(self, config_dir: Union[str, Path] = None):
        """Initialize configuration manager."""
        self.config_dir = Path(config_dir) if config_dir else Path('config')
        self.config = self.DEFAULT_CONFIG.copy()
        self._loaded_sources = []

        logger.debug(f"ConfigManager initialized with config_dir: {self.config_dir}")

    def load_configuration(self) -> Dict[str, Any]:
        """
        Load configuration from all sources in priority order:
        1. Environment variables
        2. YAML files
        3. INI files
        4. Defaults
        """
        # Start with defaults
        self.config = self._deep_copy(self.DEFAULT_CONFIG)

        # Load from files
        self._load_yaml_config()
        self._load_ini_config()

        # Override with environment variables
        self._load_env_config()

        # Validate configuration
        self._validate_config()

        logger.info(f"Configuration loaded from {len(self._loaded_sources)} sources")
        return self.config

    def get(self, section: str, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        if section in self.config and key in self.config[section]:
            return self.config[section][key]
        return default

    def set(self, section: str, key: str, value: Any):
        """Set configuration value."""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value

    def save_config(self, format: str = 'yaml', file_path: Union[str, Path] = None):
        """Save current configuration to file."""
        if not file_path:
            if format == 'yaml':
                file_path = self.config_dir / 'runtime.yml'
            else:
                file_path = self.config_dir / 'runtime.ini'

        self.config_dir.mkdir(exist_ok=True)

        if format == 'yaml':
            self._save_yaml(file_path)
        else:
            self._save_ini(file_path)

        logger.info(f"Configuration saved to: {file_path}")

    def _load_yaml_config(self):
        """Load YAML configuration files."""
        if not YAML_AVAILABLE:
            logger.warning("PyYAML not available, skipping YAML config loading")
            return

        yaml_files = [
            self.config_dir / 'config.yml',
            self.config_dir / 'config.yaml',
            self.config_dir / 'validation.yml'
        ]

        for yaml_file in yaml_files:
            if yaml_file.exists():
                try:
                    with yaml_file.open('r', encoding='utf-8') as f:
                        yaml_config = yaml.safe_load(f)

                    if yaml_config:
                        self._merge_config(yaml_config)
                        self._loaded_sources.append(f"YAML: {yaml_file}")
                        logger.debug(f"Loaded YAML config: {yaml_file}")

                except Exception as e:
                    logger.error(f"Error loading YAML config {yaml_file}: {e}")

    def _load_ini_config(self):
        """Load INI configuration files."""
        ini_files = [
            self.config_dir / 'runtime.ini',
            self.config_dir / 'config.ini'
        ]

        for ini_file in ini_files:
            if ini_file.exists():
                try:
                    parser = ConfigParser()
                    parser.read(ini_file, encoding='utf-8')

                    ini_config = {}
                    for section_name in parser.sections():
                        ini_config[section_name] = dict(parser[section_name])

                    # Convert string values to appropriate types
                    ini_config = self._parse_ini_values(ini_config)

                    self._merge_config(ini_config)
                    self._loaded_sources.append(f"INI: {ini_file}")
                    logger.debug(f"Loaded INI config: {ini_file}")

                except Exception as e:
                    logger.error(f"Error loading INI config {ini_file}: {e}")

    def _load_env_config(self):
        """Load configuration from environment variables."""
        env_mappings = {
            'INTEGRITYFORGE_CHUNK_SIZE': ('integrityforge', 'chunk_size', int),
            'INTEGRITYFORGE_LOG_LEVEL': ('integrityforge', 'log_level', str),
            'INTEGRITYFORGE_MAX_FILE_SIZE': ('integrityforge', 'max_file_size', int),
            'INTEGRITYFORGE_CACHE_ENABLED': ('integrityforge', 'cache_enabled', self._str_to_bool),
            'INTEGRITYFORGE_STRICT_MODE': ('validation', 'strict_mode', self._str_to_bool),
            'INTEGRITYFORGE_LOG_FILE': ('logging', 'file_path', str)
        }

        env_config = {}
        for env_var, (section, key, converter) in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                try:
                    converted_value = converter(value)
                    if section not in env_config:
                        env_config[section] = {}
                    env_config[section][key] = converted_value
                    self._loaded_sources.append(f"ENV: {env_var}")
                except Exception as e:
                    logger.warning(f"Error converting env var {env_var}={value}: {e}")

        if env_config:
            self._merge_config(env_config)
            logger.debug("Loaded environment configuration")

    def _parse_ini_values(self, config: Dict[str, Dict[str, str]]) -> Dict[str, Dict]:
        """Parse string values from INI files to appropriate types."""
        parsed = {}

        for section, values in config.items():
            parsed[section] = {}
            for key, value in values.items():
                # Try to convert to appropriate type
                parsed[section][key] = self._parse_value(value)

        return parsed

    def _parse_value(self, value: str) -> Union[str, int, float, bool]:
        """Parse string value to appropriate type."""
        value = value.strip()

        # Boolean values
        if value.lower() in ('true', 'yes', 'on', '1'):
            return True
        elif value.lower() in ('false', 'no', 'off', '0'):
            return False

        # Integer values
        try:
            return int(value)
        except ValueError:
            pass

        # Float values
        try:
            return float(value)
        except ValueError:
            pass

        # String values (default)
        return value

    def _str_to_bool(self, value: str) -> bool:
        """Convert string to boolean."""
        return value.lower() in ('true', 'yes', 'on', '1')

    def _merge_config(self, new_config: Dict[str, Any]):
        """Merge new configuration with existing config."""
        for section, values in new_config.items():
            if section not in self.config:
                self.config[section] = {}
            if isinstance(values, dict):
                self.config[section].update(values)
            else:
                # Handle non-dict values (for simple key-value configs)
                self.config[section] = values

    def _deep_copy(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create deep copy of configuration."""
        return json.loads(json.dumps(config))

    def _validate_config(self):
        """Validate configuration values."""
        # Validate chunk size
        chunk_size = self.get('integrityforge', 'chunk_size', 8192)
        if not isinstance(chunk_size, int) or chunk_size < 1024:
            logger.warning(f"Invalid chunk_size {chunk_size}, using default")
            self.set('integrityforge', 'chunk_size', 8192)

        # Validate max file size
        max_size = self.get('integrityforge', 'max_file_size', 1073741824)
        if not isinstance(max_size, int) or max_size < 0:
            logger.warning(f"Invalid max_file_size {max_size}, using default")
            self.set('integrityforge', 'max_file_size', 1073741824)

        # Validate log level
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        log_level = self.get('integrityforge', 'log_level', 'INFO').upper()
        if log_level not in valid_levels:
            logger.warning(f"Invalid log_level {log_level}, using INFO")
            self.set('integrityforge', 'log_level', 'INFO')

    def _save_yaml(self, file_path: Path):
        """Save configuration as YAML."""
        if not YAML_AVAILABLE:
            raise ImportError("PyYAML required for YAML output")

        with file_path.open('w', encoding='utf-8') as f:
            yaml.dump(self.config, f, default_flow_style=False, sort_keys=True)

    def _save_ini(self, file_path: Path):
        """Save configuration as INI."""
        parser = ConfigParser()

        for section, values in self.config.items():
            if isinstance(values, dict):
                parser.add_section(section)
                for key, value in values.items():
                    parser.set(section, key, str(value))

        with file_path.open('w', encoding='utf-8') as f:
            parser.write(f)

    def get_loaded_sources(self) -> list:
        """Get list of configuration sources that were loaded."""
        return self._loaded_sources.copy()

    def validate_schema(self, schema_file: Union[str, Path] = None) -> bool:
        """Validate configuration against JSON schema."""
        try:
            import jsonschema
        except ImportError:
            logger.warning("jsonschema not available, skipping schema validation")
            return True

        if not schema_file:
            schema_file = self.config_dir / 'config.schema.json'

        if not schema_file.exists():
            logger.debug("No schema file found, skipping validation")
            return True

        try:
            with schema_file.open('r', encoding='utf-8') as f:
                schema = json.load(f)

            jsonschema.validate(self.config, schema)
            logger.info("Configuration schema validation passed")
            return True

        except jsonschema.ValidationError as e:
            logger.error(f"Configuration schema validation failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Schema validation error: {e}")
            return False