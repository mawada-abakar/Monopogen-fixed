#!/usr/bin/env python3

import os
import sys
import argparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)-8s\t%(filename)s %(message)s")

# Import sub-modules
from bamProcess import preProcess
from germline import germline
from somatic import somatic

def main():
    parser = argparse.ArgumentParser(description="Monopogen: A pipeline for single-cell variant analysis.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for 'germline' command
    germline_parser = subparsers.add_parser("germline", help="Perform germline variant calling and phasing.")
    germline_parser.add_argument("-r", "--region", required=True, help="Region file (e.g., region.lst)")
    germline_parser.add_argument("-s", "--sample", required=True, help="Sample file (e.g., all)")
    germline_parser.add_argument("-o", "--output_dir", default="output", help="Output directory")
    germline_parser.add_argument("-g", "--reference", required=True, help="Reference genome (e.g., example/chr20_2Mb.hg38.fa)")
    germline_parser.add_argument("-p", "--phasing_panel", help="Phasing panel VCF (e.g., example/CCDG_14151_B01_GRM_WGS_2020-08-05_chr20.filtered.shapeit2-duohmm-phased.vcf.gz)")
    germline_parser.add_argument("-a", "--apps", default="apps", help="Path to apps directory")
    germline_parser.add_argument("-t", "--nthreads", type=int, default=1, help="Number of threads")
    germline_parser.set_defaults(func=germline)

    # Subparser for 'somatic' command
    somatic_parser = subparsers.add_parser("somatic", help="Perform somatic variant analysis.")
    somatic_parser.add_argument("-i", "--input_folder", required=True, help="Input folder containing germline results")
    somatic_parser.add_argument("-r", "--region", required=True, help="Region file (e.g., region.lst)")
    somatic_parser.add_argument("-l", "--barcode", required=True, help="Cell barcode file")
    somatic_parser.add_argument("-k", "--keep", help="Keep intermediate files")
    somatic_parser.add_argument("-a", "--app_path", required=True, help="Path to apps directory")
    somatic_parser.add_argument("-t", "--nthreads", type=int, default=1, help="Number of threads")
    somatic_parser.add_argument("-s", "--step", required=True, choices=['featureInfo', 'cellScan', 'LDrefinement', 'monovar', 'all'], help="Analysis step to perform")
    somatic_parser.add_argument("-g", "--reference", required=True, help="Reference genome file")
    somatic_parser.add_argument("--skip_feature_extraction", action='store_true', help='Skip feature extraction step if already done')
    somatic_parser.add_argument("--skip_cell_scanning", action='store_true', help='Skip cell scanning step if already done')
    somatic_parser.add_argument("--skip_ld_refinement", action='store_true', help='Skip LD refinement step if already done')
    somatic_parser.add_argument("--convert_to_vcf", action='store_true', help='Convert LD refined variants to VCF format')
    somatic_parser.set_defaults(func=somatic)

    # Subparser for 'preprocess' command
    preprocess_parser = subparsers.add_parser("preprocess", help="Preprocess BAM files.")
    preprocess_parser.add_argument("-b", "--bamFile", required=True, help="BAM list file (format: sample_name,bam_path)")
    preprocess_parser.add_argument("-o", "--out", required=True, help="Output directory")
    preprocess_parser.add_argument("-a", "--apps", required=True, help="Path to apps directory")
    preprocess_parser.add_argument("-m", "--max_mismatch", type=int, default=3, help="Maximum mismatch allowed")
    preprocess_parser.add_argument("-t", "--nthreads", type=int, default=1, help="Number of threads")
    preprocess_parser.set_defaults(func=preProcess)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
