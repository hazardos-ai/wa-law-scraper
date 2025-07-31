"""Command-line interface for the WA Law Scraper registry system."""

import sys
import logging
import argparse
from pathlib import Path

from .registry import RegistryManager, RegistryGenerator


def setup_logging(verbose: bool = False):
    """Set up logging configuration.
    
    Args:
        verbose: Enable debug-level logging if True
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def cmd_generate(args):
    """Generate new registries."""
    registry_manager = RegistryManager(args.data_dir)
    generator = RegistryGenerator(registry_manager, rate_limit_enabled=args.rate_limit)
    
    if args.code_type == 'wac':
        registry = generator.generate_wac_registry()
        if registry:
            print(f"WAC registry generated successfully with {len(registry.titles)} titles")
        else:
            print("Failed to generate WAC registry")
            sys.exit(1)
    elif args.code_type == 'rcw':
        registry = generator.generate_rcw_registry()
        if registry:
            print(f"RCW registry generated successfully with {len(registry.titles)} titles")
        else:
            print("Failed to generate RCW registry")
            sys.exit(1)
    elif args.code_type == 'both':
        wac_registry, rcw_registry = generator.generate_both_registries()
        if wac_registry and rcw_registry:
            print(f"Both registries generated successfully:")
            print(f"  WAC: {len(wac_registry.titles)} titles")
            print(f"  RCW: {len(rcw_registry.titles)} titles")
        else:
            print("Failed to generate one or both registries")
            if not wac_registry:
                print("  WAC registry failed")
            if not rcw_registry:
                print("  RCW registry failed")
            sys.exit(1)


def cmd_list(args):
    """List existing registries."""
    registry_manager = RegistryManager(args.data_dir)
    registries = registry_manager.list_registries(args.code_type)
    
    if not registries:
        filter_msg = f" for {args.code_type}" if args.code_type else ""
        print(f"No registries found{filter_msg}")
        return
    
    print(f"Found {len(registries)} registries:")
    for registry_file in registries:
        # Get file modification time
        mtime = registry_file.stat().st_mtime
        import datetime
        mtime_str = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        print(f"  {registry_file.name} (modified: {mtime_str})")


def cmd_info(args):
    """Show information about a specific registry."""
    registry_manager = RegistryManager(args.data_dir)
    
    if args.file:
        registry_file = Path(args.file)
        if not registry_file.exists():
            print(f"Registry file not found: {registry_file}")
            sys.exit(1)
    else:
        # Get latest registry for code type
        registries = registry_manager.list_registries(args.code_type)
        if not registries:
            print(f"No registries found for {args.code_type}")
            sys.exit(1)
        registry_file = registries[0]
    
    registry = registry_manager.load_registry(registry_file)
    if not registry:
        print(f"Failed to load registry from: {registry_file}")
        sys.exit(1)
    
    print(f"Registry Information:")
    print(f"  File: {registry_file}")
    print(f"  Code Type: {registry.code_type}")
    print(f"  Created: {registry.created_at}")
    print(f"  Base URL: {registry.base_url}")
    print(f"  Titles: {len(registry.titles)}")
    
    total_chapters = sum(len(title.chapters) for title in registry.titles)
    total_sections = sum(len(chapter.sections) for title in registry.titles for chapter in title.chapters)
    
    print(f"  Total Chapters: {total_chapters}")
    print(f"  Total Sections: {total_sections}")
    
    if args.verbose:
        print("\nTitles:")
        for title in registry.titles:
            print(f"  {title.title_number}: {title.name} ({len(title.chapters)} chapters)")


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="WA Law Scraper - Registry system for Washington State legal codes"
    )
    parser.add_argument(
        '--data-dir', 
        default='data',
        help='Data directory for storing registries (default: data)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate new registries')
    gen_parser.add_argument(
        'code_type',
        choices=['wac', 'rcw', 'both'],
        help='Type of legal code to scrape'
    )
    gen_parser.add_argument(
        '--rate-limit',
        action='store_true',
        help='Enable rate limiting for web requests'
    )
    gen_parser.set_defaults(func=cmd_generate)
    
    # List command
    list_parser = subparsers.add_parser('list', help='List existing registries')
    list_parser.add_argument(
        '--code-type',
        choices=['wac', 'rcw'],
        help='Filter by code type'
    )
    list_parser.set_defaults(func=cmd_list)
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show registry information')
    info_parser.add_argument(
        '--code-type',
        choices=['wac', 'rcw'],
        help='Show info for latest registry of this type'
    )
    info_parser.add_argument(
        '--file',
        help='Specific registry file to show info for'
    )
    info_parser.set_defaults(func=cmd_info)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Set up logging
    setup_logging(args.verbose)
    
    # Run the command
    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Command failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()