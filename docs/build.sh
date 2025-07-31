#!/bin/bash

# Documentation Build Script for D3 Project Template
# This script helps build documentation with both MkDocs and JupyterBook

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if pixi is available
if ! command -v pixi &> /dev/null; then
    print_error "Pixi is not installed. Please install pixi first: https://pixi.sh/"
    exit 1
fi

# Function to install dependencies
install_deps() {
    print_status "Installing documentation dependencies..."
    pixi install --feature docs
    print_success "Dependencies installed successfully!"
}

# Function to build MkDocs
build_mkdocs() {
    print_status "Building MkDocs documentation..."
    pixi run docs-mkdocs-build
    print_success "MkDocs documentation built in docs/site/"
}

# Function to serve MkDocs
serve_mkdocs() {
    print_status "Starting MkDocs development server..."
    print_warning "Press Ctrl+C to stop the server"
    pixi run docs-mkdocs-serve
}

# Function to build JupyterBook
build_jupyter_book() {
    print_status "Building JupyterBook documentation..."
    pixi run docs-jupyter-book-build
    print_success "JupyterBook documentation built in docs/jupyter-book/_build/"
}

# Function to serve JupyterBook
serve_jupyter_book() {
    print_status "Building and opening JupyterBook documentation..."
    pixi run docs-jupyter-book-serve
    print_success "JupyterBook documentation opened in browser"
}

# Function to clean documentation
clean_docs() {
    print_status "Cleaning documentation build artifacts..."
    pixi run docs-clean
    print_success "Documentation cleaned successfully!"
}

# Function to build both
build_all() {
    print_status "Building documentation with both MkDocs and JupyterBook..."
    build_mkdocs
    build_jupyter_book
    print_success "All documentation built successfully!"
}

# Help function
show_help() {
    echo "Documentation Build Script for D3 Project Template"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  install          Install documentation dependencies"
    echo "  mkdocs-build     Build MkDocs documentation"
    echo "  mkdocs-serve     Serve MkDocs documentation locally"
    echo "  jupyter-build    Build JupyterBook documentation"
    echo "  jupyter-serve    Build and open JupyterBook documentation"
    echo "  build-all        Build both MkDocs and JupyterBook documentation"
    echo "  clean            Clean documentation build artifacts"
    echo "  help             Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 install              # Install dependencies"
    echo "  $0 mkdocs-serve          # Start MkDocs development server"
    echo "  $0 build-all            # Build both documentation systems"
}

# Main script logic
case "${1:-help}" in
    install)
        install_deps
        ;;
    mkdocs-build)
        build_mkdocs
        ;;
    mkdocs-serve)
        serve_mkdocs
        ;;
    jupyter-build)
        build_jupyter_book
        ;;
    jupyter-serve)
        serve_jupyter_book
        ;;
    build-all)
        build_all
        ;;
    clean)
        clean_docs
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
