# Monopogen-Fixed Tutorial

This tutorial provides a complete walkthrough of the Monopogen-Fixed pipeline, from data preparation to somatic variant analysis.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Data Preparation](#data-preparation)
- [Pipeline Steps](#pipeline-steps)
  - [Step 1: Preprocess](#step-1-preprocess)
  - [Step 2: Germline SNV Calling](#step-2-germline-snv-calling)
  - [Step 3: Somatic SNV Calling](#step-3-somatic-snv-calling)
- [Output Files](#output-files)
- [Downstream Analysis](#downstream-analysis)
- [Troubleshooting](#troubleshooting)

## Overview

Monopogen-Fixed is a three-step pipeline for single-cell somatic variant analysis:

1. **Data preprocess**: Filter BAM files and prepare data
2. **Germline SNV calling**: Identify and phase germline variants
3. **Somatic SNV calling**: Detect somatic mutations using machine learning

## Quick Start

For users familiar with the pipeline, here's a minimal working example:

```bash
# Set environment
export MONOPOGEN_PATH=/path/to/Monopogen-fixed

# Step 1: Preprocess
python ${MONOPOGEN_PATH}/src/Monopogen.py preprocess \
  -b bam.lst \
  -o output \
  -a ${MONOPOGEN_PATH}/apps \
  -t 2 \
  -m 3

# Step 2: Germline calling
python ${MONOPOGEN_PATH}/src/Monopogen.py germline \
  -r region.lst \
  -s all \
  -o output \
  -g reference.fa \
  -p phasing_panel.vcf.gz \
  -a ${MONOPOGEN_PATH}/apps \
  -t 2

# Step 3: Somatic calling
python ${MONOPOGEN_PATH}/src/Monopogen.py somatic \
  -i output \
  -r region.lst \
  -l barcode.csv \
  -a ${MONOPOGEN_PATH}/apps \
  -t 2 \
  -s all \
  -g reference.fa

## Data Preparation

Required Input Files

1. BAM Files

    Format: Sorted and indexed BAM files
    Requirements:
        Single-cell RNA-seq or ATAC-seq data
        Aligned to the reference genome
        Must be indexed (.bai files present)

   # Index BAM files if needed
   samtools index sample.bam

2. BAM List File (bam.lst)

    Format: CSV format with sample names and BAM file paths
    Example:
    SampleA,/path/to/sampleA.bam
    SampleB,/path/to/sampleB.bam

3. Region List File (region.lst)

    Format: One chromosome per line
    Example:
    chr20

4. Reference Files

    Reference genome: FASTA format (.fa or .fasta)
    Phasing panel: Population VCF file (.vcf.gz)
    Cell barcodes: CSV file with cell identifiers

Directory Structure

project/
├── bam.lst
├── region.lst
├── reference.fa
├── phasing_panel.vcf.gz
├── barcode.csv
└── output/          # Will be created by pipeline


## Pipeline Steps

Step 1: Preprocess
Purpose: Filter BAM files and prepare data for variant calling.

Command:
python ${MONOPOGEN_PATH}/src/Monopogen.py preprocess \
  -b bam.lst \
  -o output \
  -a ${MONOPOGEN_PATH}/apps \
  -t 2 \
  -m 3

Parameters:

    -b: BAM list file
    -o: Output directory
    -a: Apps directory path
    -t: Number of threads
    -m: Maximum mismatch allowed

Expected Output:

output/
└── Bam/
    ├── SampleA_chr20.filter.bam
    ├── SampleA_chr20.filter.bam.bai
    ├── SampleB_chr20.filter.bam
    └── SampleB_chr20.filter.bam.bai

Runtime: 10-30 minutes depending on data size

Step 2: Germline SNV Calling
Purpose: Identify germline variants and perform population-based phasing.

Command:
python ${MONOPOGEN_PATH}/src/Monopogen.py germline \
  -r region.lst \
  -s all \
  -o output \
  -g ${MONOPOGEN_PATH}/example/chr20_2Mb.hg38.fa \
  -p ${MONOPOGEN_PATH}/example/phasing_panel.vcf.gz \
  -a ${MONOPOGEN_PATH}/apps \
  -t 2

Parameters:

    -r: Region list file
    -s: Sample list (use "all" for all samples)
    -o: Output directory
    -g: Reference genome
    -p: Phasing panel VCF
    -a: Apps directory
    -t: Number of threads

Expected Output:

output/
└── germline/
    ├── chr20.gl.vcf.gz      # Genotype likelihoods
    ├── chr20.gp.vcf.gz      # Genotype probabilities
    ├── chr20.phased.vcf.gz  # Phased variants
    ├── chr20.gp.log         # Beagle log (genotyping)
    └── chr20.phased.log     # Beagle log (phasing)

Runtime: 30 minutes to 2 hours

Important: If you encounter VCF header warnings, run the header fix script:

# Fix VCF headers
${MONOPOGEN_PATH}/scripts/fix_vcf_headers.sh output/germline/*.vcf.gz

Step 3: Somatic SNV Calling
Purpose: Detect somatic mutations using machine learning and LD refinement.

Command:
python ${MONOPOGEN_PATH}/src/Monopogen.py somatic \
  -i output \
  -r region.lst \
  -l ${MONOPOGEN_PATH}/test/test.csv \
  -a ${MONOPOGEN_PATH}/apps \
  -t 2 \
  -s all \
  -g ${MONOPOGEN_PATH}/example/chr20_2Mb.hg38.fa

Parameters:

    -i: Input directory (from germline step)
    -r: Region list file
    -l: Cell barcode file
    -a: Apps directory
    -t: Number of threads
    -s: Analysis steps (all, featureInfo, cellScan, LDrefinement)
    -g: Reference genome

Expected Output:

output/
└── somatic/
    ├── chr20.putativeSNVs.csv           # Final somatic variants
    ├── chr20.cell_snv.cellID.filter.csv # Cell-variant associations
    ├── chr20.SNV_mat.RDS                # SNV matrix for R analysis
    ├── LDrefinement_germline.chr20.pdf  # LD analysis plots
    ├── svm_feature.chr20.pdf            # SVM feature plots
    └── [other intermediate files]

Runtime: 1-3 hours depending on data complexity

## Output Files

Key Result Files

1-chr20.putativeSNVs.csv

    Content: Final filtered somatic variants
    Columns: chr, pos, Ref_allele, Alt_allele, Depth_total, Depth_ref, Depth_alt, SVM_pos_score, LD_scores, BAF_alt
    Use: Main result file for downstream analysis

2-chr20.cell_snv.cellID.filter.csv

    Content: Cell barcodes with detected somatic variants
    Use: Identify which cells carry specific mutations

3-chr20.SNV_mat.RDS

    Content: SNV-by-cell matrix in R format
    Use: Input for R-based downstream analysis

Quality Control Files

1-LDrefinement_germline.chr20.pdf

    Content: Linkage disequilibrium analysis plots
    Use: Assess LD patterns and refinement quality

2-svm_feature.chr20.pdf

    Content: SVM feature analysis and classification results
    Use: Evaluate variant classification quality

## Downstream Analysis

R-based Analysis

The somatic variants can be analyzed using R and Seurat:

# Load required libraries
library(Seurat)
library(ggpubr)

# Load Monopogen results
meta <- read.csv("output/somatic/chr20.putativeSNVs.csv")
mat <- readRDS("output/somatic/chr20.SNV_mat.RDS")

# Filter variants
meta_filter <- meta[meta$Depth_ref > 5 & meta$Depth_alt > 5, ]
meta_filter <- meta_filter[meta_filter$BAF_alt < 0.5, ]

# Further analysis...

Expected Results

For a typical 2Mb region:

    Germline variants: ~1,000-2,000 variants
    Somatic variants: ~10-100 variants (much fewer than germline)
    Processing time: 2-4 hours total

## Troubleshooting

Common Issues

1. BAM Index Missing
Error: AssertionError: Bam file ... has not been indexed!

Solution:
samtools index your_file.bam

2. VCF Header Issues
Error: [W::vcf_parse] Contig 'chr20' is not defined in the header

Solution:
${MONOPOGEN_PATH}/scripts/fix_vcf_headers.sh output/germline/*.vcf.gz

3. R Package Missing
Error: Error in fread(mat_gz) : ... 'R.utils' package which cannot be found

Solution:
Rscript -e "install.packages('R.utils', repos='https://cran.r-project.org')"

4. Invalid Header in Somatic Step
Error: ValueError: Invalid header

Solution: This indicates VCF header issues. Run the header fix script and ensure all VCF files have proper contig definitions

Getting Help

For additional support:

    Check the Troubleshooting Guide
    Review the Installation Guide
    Open an issue on GitHub with complete error messages

Citation

If you use Monopogen-Fixed in your research, please cite:

    Original Monopogen paper:
    Dou J, Tan Y, Kock KH, Wang J, Cheng X, Tan LM, Han KY, Hon CC, Park WY, Shin JW, Jin H, H Chen, L Ding, S Prabhakar, N Navin. K Chen. Single-nucleotide variant calling in single-cell sequencing data with Monopogen. Nature Biotechnology. 2023 Aug 17:1-0

This repository:
    https://github.com/mawada-abakar/Monopogen-fixed






