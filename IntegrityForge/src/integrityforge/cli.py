#!/usr/bin/env python3
"""
IntegrityForge CLI: Deterministic file integrity validation and attestation system.

Provides command-line interface for cryptographic file validation with clean exit codes
and structured error handling.

OPERATIONAL INTEGRITY VERIFIED — ALEXIS ADAMS PRIMACY MANIFESTED
"""

import argparse
import sys
import logging
from pathlib import Path
from typing import List, Optional

try:
    # When run as module
    from .core import IntegrityHasher, IntegrityValidator, IntegrityAttestor
    from .config import ConfigManager
except ImportError:
    # When run directly
    from core import IntegrityHasher, IntegrityValidator, IntegrityAttestor
    from config import ConfigManager


def setup_logging(log_level: str = 'INFO', log_file: Optional[str] = None):
    """Setup structured logging."""
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(numeric_level)

    # File handler (optional)
    handlers = [console_handler]
    if log_file:
        try:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            file_handler.setLevel(numeric_level)
            handlers.append(file_handler)
        except Exception as e:
            console_handler.emit(logging.LogRecord(
                'cli', logging.WARNING, __file__, 0,
                f"Could not setup file logging: {e}", (), None
            ))

    # Configure root logger
    logging.basicConfig(level=numeric_level, handlers=handlers, force=True)


def create_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog='integrityforge',
        description='Deterministic file integrity validation and cryptographic attestation system',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exit Codes:
  0 - Success: Operation completed successfully
  1 - Validation Failure: Integrity check failed
  2 - Error: Operational error (file not found, permission denied, etc.)
  3 - Configuration Error: Invalid configuration or arguments

Examples:
  integrityforge hash file.txt
  integrityforge validate --expected a665a459... file.txt
  integrityforge attest file.txt --output attestation.json
  integrityforge --validate-config
        """
    )

    # Global options
    parser.add_argument(
        '--config-dir',
        type=Path,
        default=Path('config'),
        help='Configuration directory path'
    )
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help='Logging level'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress console output'
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Hash command
    hash_parser = subparsers.add_parser(
        'hash',
        help='Compute SHA-256 hash of file(s)'
    )
    hash_parser.add_argument(
        'files',
        nargs='+',
        type=Path,
        help='Files to hash'
    )
    hash_parser.add_argument(
        '--chunk-size',
        type=int,
        default=8192,
        help='Chunk size for streaming (bytes)'
    )
    hash_parser.add_argument(
        '--output',
        type=Path,
        help='Output file for hash results'
    )

    # Validate command
    validate_parser = subparsers.add_parser(
        'validate',
        help='Validate file integrity against expected hash'
    )
    validate_parser.add_argument(
        'file',
        type=Path,
        help='File to validate'
    )
    validate_parser.add_argument(
        '--expected',
        required=True,
        help='Expected SHA-256 hash'
    )
    validate_parser.add_argument(
        '--chunk-size',
        type=int,
        default=8192,
        help='Chunk size for streaming (bytes)'
    )

    # Attest command
    attest_parser = subparsers.add_parser(
        'attest',
        help='Generate cryptographic attestation for file'
    )
    attest_parser.add_argument(
        'file',
        type=Path,
        help='File to attest'
    )
    attest_parser.add_argument(
        '--output',
        type=Path,
        required=True,
        help='Output file for attestation'
    )
    attest_parser.add_argument(
        '--format',
        choices=['json', 'yaml'],
        default='json',
        help='Output format'
    )
    attest_parser.add_argument(
        '--metadata',
        type=str,
        help='Additional metadata as JSON string'
    )

    # Verify command
    verify_parser = subparsers.add_parser(
        'verify',
        help='Verify attestation against file'
    )
    verify_parser.add_argument(
        'attestation',
        type=Path,
        help='Attestation file to verify'
    )
    verify_parser.add_argument(
        '--file',
        type=Path,
        help='File to verify against (overrides path in attestation)'
    )

    # Config command
    config_parser = subparsers.add_parser(
        'config',
        help='Configuration management'
    )
    config_parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate current configuration'
    )
    config_parser.add_argument(
        '--show',
        action='store_true',
        help='Show current configuration'
    )
    config_parser.add_argument(
        '--save',
        type=Path,
        help='Save current configuration to file'
    )

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args(argv)

    # Setup logging
    log_level = args.log_level
    if args.quiet:
        log_level = 'ERROR'

    setup_logging(log_level)

    logger = logging.getLogger(__name__)

    try:
        # Load configuration
        config_manager = ConfigManager(args.config_dir)
        config = config_manager.load_configuration()

        # Override with command-line args
        if hasattr(args, 'chunk_size'):
            config_manager.set('integrityforge', 'chunk_size', args.chunk_size)

        # Execute command
        if args.command == 'hash':
            return handle_hash(args, config_manager)
        elif args.command == 'validate':
            return handle_validate(args, config_manager)
        elif args.command == 'attest':
            return handle_attest(args, config_manager)
        elif args.command == 'verify':
            return handle_verify(args, config_manager)
        elif args.command == 'config':
            return handle_config(args, config_manager)
        else:
            parser.print_help()
            return 3

    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 2
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 2


def handle_hash(args: argparse.Namespace, config: ConfigManager) -> int:
    """Handle hash command."""
    logger = logging.getLogger(__name__)

    chunk_size = config.get('integrityforge', 'chunk_size', 8192)
    hasher = IntegrityHasher(chunk_size)

    results = []
    for file_path in args.files:
        try:
            if not file_path.exists():
                logger.error(f"File not found: {file_path}")
                return 2

            file_hash = hasher.hash_file(file_path)
            result = f"{file_hash}  {file_path}"
            results.append(result)

            if not args.output:
                print(result)

        except Exception as e:
            logger.error(f"Error hashing {file_path}: {e}")
            return 2

    # Write to output file if specified
    if args.output and results:
        try:
            with args.output.open('w', encoding='utf-8') as f:
                f.write('\n'.join(results) + '\n')
            logger.info(f"Results written to: {args.output}")
        except Exception as e:
            logger.error(f"Error writing output file: {e}")
            return 2

    return 0


def handle_validate(args: argparse.Namespace, config: ConfigManager) -> int:
    """Handle validate command."""
    logger = logging.getLogger(__name__)

    chunk_size = config.get('integrityforge', 'chunk_size', 8192)
    validator = IntegrityValidator()

    try:
        passed = validator.validate_hash(args.file, args.expected)
        return 0 if passed else 1

    except Exception as e:
        logger.error(f"Validation error: {e}")
        return 2


def handle_attest(args: argparse.Namespace, config: ConfigManager) -> int:
    """Handle attest command."""
    logger = logging.getLogger(__name__)

    attestor = IntegrityAttestor()

    # Parse metadata if provided
    metadata = None
    if args.metadata:
        try:
            import json
            metadata = json.loads(args.metadata)
        except Exception as e:
            logger.error(f"Invalid metadata JSON: {e}")
            return 3

    try:
        attestation = attestor.generate_attestation(args.file, metadata)

        if args.format == 'yaml':
            try:
                import yaml
                output_data = yaml.dump(attestation, default_flow_style=False)
            except ImportError:
                logger.error("PyYAML required for YAML output")
                return 2
        else:
            import json
            output_data = json.dumps(attestation, indent=2, sort_keys=True)

        with args.output.open('w', encoding='utf-8') as f:
            f.write(output_data)

        logger.info(f"Attestation written to: {args.output}")
        return 0

    except Exception as e:
        logger.error(f"Attestation error: {e}")
        return 2


def handle_verify(args: argparse.Namespace, config: ConfigManager) -> int:
    """Handle verify command."""
    logger = logging.getLogger(__name__)

    attestor = IntegrityAttestor()

    try:
        import json
        with args.attestation.open('r', encoding='utf-8') as f:
            attestation = json.load(f)

        passed = attestor.verify_attestation(attestation, args.file)
        return 0 if passed else 1

    except Exception as e:
        logger.error(f"Verification error: {e}")
        return 2


def handle_config(args: argparse.Namespace, config: ConfigManager) -> int:
    """Handle config command."""
    logger = logging.getLogger(__name__)

    try:
        if args.validate:
            # Load and validate configuration
            config.load_configuration()
            valid = config.validate_schema()
            if valid:
                logger.info("Configuration validation passed")
                return 0
            else:
                logger.error("Configuration validation failed")
                return 1

        elif args.show:
            # Display current configuration
            import json
            print(json.dumps(config.config, indent=2, sort_keys=True))
            return 0

        elif args.save:
            # Save configuration
            format_type = 'yaml' if args.save.suffix in ('.yml', '.yaml') else 'ini'
            config.save_config(format_type, args.save)
            return 0

        else:
            logger.error("No config action specified")
            return 3

    except Exception as e:
        logger.error(f"Configuration error: {e}")
        return 2


if __name__ == '__main__':
    sys.exit(main())