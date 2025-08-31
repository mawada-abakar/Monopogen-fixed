#!/bin/bash

# VCF Header Fix Script for Monopogen-Fixed
# Fixes the "Contig 'chr20' is not defined in the header" warning
# Usage: ./fix_vcf_headers.sh file1.vcf.gz file2.vcf.gz ...

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command -v bcftools &> /dev/null; then
        print_error "bcftools is not installed or not in PATH"
        exit 1
    fi
    
    if ! command -v tabix &> /dev/null; then
        print_error "tabix is not installed or not in PATH"
        exit 1
    fi
    
    print_status "Prerequisites check passed"
}

# Function to fix a single VCF file
fix_vcf_header() {
    local input_vcf="$1"
    local output_vcf="${input_vcf%.vcf.gz}.fixed.vcf.gz"
    
    print_status "Processing: $input_vcf"
    
    # Check if input file exists
    if [[ ! -f "$input_vcf" ]]; then
        print_error "File not found: $input_vcf"
        return 1
    fi
    
    # Check if file already has contig header
    if bcftools view -h "$input_vcf" 2>/dev/null | grep -q "##contig=<ID=chr20"; then
        print_warning "File $input_vcf already has chr20 contig header, skipping..."
        return 0
    fi
    
    # Create temporary files
    local temp_dir=$(mktemp -d)
    local old_header="$temp_dir/old_header.txt"
    local new_header="$temp_dir/new_header.txt"
    local header_part1="$temp_dir/header_part1.txt"
    local contig_line="$temp_dir/contig_line.txt"
    local header_part2="$temp_dir/header_part2.txt"
    
    # Extract header
    if ! bcftools view -h "$input_vcf" > "$old_header" 2>/dev/null; then
        print_error "Failed to extract header from $input_vcf"
        rm -rf "$temp_dir"
        return 1
    fi
    
    # Create header parts
    grep '^##' "$old_header" | grep -v '^##contig' > "$header_part1"
    echo '##contig=<ID=chr20,length=64444167>' > "$contig_line"
    grep '^#CHROM' "$old_header" > "$header_part2"
    
    # Combine parts
    cat "$header_part1" "$contig_line" "$header_part2" > "$new_header"
    
    # Apply new header
    if bcftools reheader -h "$new_header" "$input_vcf" > "$output_vcf" 2>/dev/null; then
        # Index the fixed file
        if tabix -p vcf "$output_vcf" 2>/dev/null; then
            print_status "Successfully created: $output_vcf"
        else
            print_error "Failed to index $output_vcf"
            rm -f "$output_vcf"
            rm -rf "$temp_dir"
            return 1
        fi
    else
        print_error "Failed to apply new header to $input_vcf"
        rm -rf "$temp_dir"
        return 1
    fi
    
    # Clean up
    rm -rf "$temp_dir"
    return 0
}

# Main function
main() {
    echo "=================================================="
    echo "    VCF Header Fix Script for Monopogen-Fixed"
    echo "=================================================="
    echo
    
    # Check if any arguments provided
    if [[ $# -eq 0 ]]; then
        print_error "No input files provided"
        echo "Usage: $0 file1.vcf.gz file2.vcf.gz ..."
        echo "Example: $0 output/germline/*.vcf.gz"
        exit 1
    fi
    
    # Check prerequisites
    check_prerequisites
    echo
    
    # Process each file
    local success_count=0
    local total_count=$#
    
    for vcf_file in "$@"; do
        if fix_vcf_header "$vcf_file"; then
            ((success_count++))
        fi
        echo
    done
    
    # Summary
    echo "=================================================="
    print_status "Processing complete!"
    print_status "Successfully processed: $success_count/$total_count files"
    
    if [[ $success_count -eq $total_count ]]; then
        print_status "All files processed successfully!"
        echo
        print_status "You can now use the .fixed.vcf.gz files in your pipeline"
        print_status "Remember to update your pipeline to use the fixed files"
    else
        print_warning "Some files failed to process. Check the error messages above."
    fi
    echo "=================================================="
}

# Run main function with all arguments
main "$@"
