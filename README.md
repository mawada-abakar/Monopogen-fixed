# Monopogen-Fixed: Working Implementation of Single-Cell Somatic Variant Analysis

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg )](https://opensource.org/licenses/MIT )
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg )](https://www.python.org/downloads/ )
[![R 4.0+](https://img.shields.io/badge/R-4.0+-blue.svg )](https://www.r-project.org/ )

## 🔬 Overview

This repository contains a **fully functional, debugged implementation** of the Monopogen pipeline for single-cell somatic variant analysis. All critical bugs have been fixed, compatibility issues resolved, and comprehensive documentation provided.

### 🎯 What is Monopogen?

Monopogen is a computational pipeline designed to identify somatic mutations in single-cell RNA sequencing (scRNA-seq) data. It uniquely combines:

- **Germline variant calling** with population-based phasing
- **Machine learning-based somatic variant detection** 
- **Linkage disequilibrium refinement** for high-confidence calls
- **Single-cell resolution** mutation analysis

## 🚀 Key Improvements in This Version

✅ **Fixed all compatibility issues** with modern bcftools/samtools  
✅ **Resolved VCF header problems** that caused downstream failures  
✅ **Added robust error handling** for missing INFO fields  
✅ **Comprehensive documentation** with step-by-step guides  
✅ **Working example data** and test cases  
✅ **R package dependencies** properly documented  

## 📚 Original Work Citation

This implementation is based on the original Monopogen pipeline:

**Paper**: Dou J, Tan Y, Kock KH, Wang J, Cheng X, Tan LM, Han KY, Hon CC, Park WY, Shin JW, Jin H, H Chen, L Ding, S Prabhakar, N Navin. K Chen. Single-nucleotide variant calling in single-cell sequencing data with Monopogen. Nature Biotechnology. 2023 Aug 17:1-0

**Original Repository**: https://github.com/KChen-lab/Monopogen

**Please cite both the original paper and this repository if you use this code.**

## 🛠️ Quick Start

```bash
# Clone this repository
git clone https://github.com/mawada-abakar/Monopogen-fixed.git
cd Monopogen-fixed

# Install dependencies
pip install -r requirements.txt
Rscript scripts/install_r_packages.R

# Verify Your Setup

# Check if all dependencies are installed
./scripts/verify_setup.py

# Run the pipeline
python src/Monopogen.py --help

📋 Input Requirements

BAM Files Format
# BAM list file (bam_list.lst)
sample1,/path/to/sample1.bam
sample2,/path/to/sample2.bam
sample3,/path/to/sample3.bam

Configuration Setup
# Copy and edit configuration template
cp config/config_template.ini config/config.ini
nano config/config.ini

# Update paths in config.ini:
# - reference_genome = /path/to/your/reference.fa
# - reference_panel = /path/to/your/panel.vcf.gz
# - output_dir = /path/to/your/output

Reference Data Requirements

    Human reference genome (GRCh38 recommended)
    1000 Genomes reference panel for population phasing
    Target regions file (e.g target_chromosomes: chr20 to run this example)

## 📊 Example Data and Test Cases

### Using Original Monopogen Test Data
This repository uses the same example datasets as the original Monopogen pipeline. **All example data and test cases are available in the original repository** - simply use them with this fixed implementation to avoid the compatibility issues.

🛠️ Usage Examples
Step 1: Prepare BAM File List
Create a BAM list file (bam_list.lst ) with this format:
# Format: sample_name,/path/to/sample.bam
sample1,/path/to/sample1.bam
sample2,/path/to/sample2.bam
sample3,/path/to/sample3.bam

Step 2: Data Preprocessing
# Set environment variables
export MONOPOGEN_PATH=$(pwd)
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${MONOPOGEN_PATH}/apps

# Run preprocessing to filter BAM files
python src/Monopogen.py preProcess \
    -b bam_list.lst \
    -o output/ \
    -a ${MONOPOGEN_PATH}/apps \
    -m 3 \
    -t 2

Step 3: Germline Variant Calling
# Run germline variant calling with phasing
python src/Monopogen.py germline \
    -r region.lst \
    -s all \
    -o output/ \
    -g /path/to/reference/chr20_2Mb.hg38.fa \
    -p /path/to/reference/panel.vcf.gz \
    -a ${MONOPOGEN_PATH}/apps \
    -t 2

Step 4: Somatic Variant Calling
# Run somatic variant analysis
python src/Monopogen.py somatic \
    -i output/germline/ \
    -r region.lst \
    -o output/ \
    -l cell_barcode_file.csv \
    -s all \
    -a ${MONOPOGEN_PATH}/apps \
    -g GRCh38.chr20.fa \
    -t 2

📊 Pipeline Output

Germline Analysis Results

    chr*.gl.vcf.gz - Initial genotype variants
    chr*.gp.vcf.gz - Genotype probability variants
    chr*.phased.vcf.gz - Phased variants (main result)
    preprocessing.log - Processing logs

Somatic Analysis Results

    chr*.somatic.vcf.gz - Somatic variants per cell
    chr*.consensus.vcf.gz - High-confidence somatic calls
    quality_metrics.txt - Coverage and quality statistics

🔧 Troubleshooting

Common Issues
VCF header warnings:
./scripts/fix_vcf_headers.sh problematic_file.vcf.gz

Tool not found errors:
# Activate conda environment
conda activate monopogen
which samtools bcftools

Python import errors:
pip install -r requirements.txt --force-reinstall

Memory issues:

    Reduce num_threads in the configuration
    Process smaller chromosomal regions
    Ensure sufficient system memory (16GB+ recommended)


🔧 Key Fixes Applied

1. Samtools/Bcftools Compatibility

    Updated from deprecated samtools mpileup to bcftools mpileup
    Removed incompatible flags options (-t DP, -v , --incl-flags, --excl-flags)
    Adding (-Ou) to output uncompressed BCF format
    
2. VCF Header Issues

    Added missing contig definitions (##contig=<ID=chr20,length=64444167>)
    Fixed header format for downstream compatibility
    Automated header validation and fixing

    Fix VCF header issues

    # Fix a single file
    ./scripts/fix_vcf_headers.sh output/germline/chr20.gp.vcf.gz

    # Fix multiple files
    ./scripts/fix_vcf_headers.sh output/germline/*.vcf.gz

3. Error Handling

    Robust handling of missing INFO fields in VCF files
    Graceful degradation when expected fields are absent
    Comprehensive logging and error reporting

📊 Expected Results
For a typical 2Mb region of chr20:

    Germline variants: ~1,000-2,000 variants
    Somatic variants: ~10-100 variants (much fewer than germline)
    Processing time: 30 minutes to 2 hours

🤝 Contributing
Contributions are welcome! Please feel free to submit issues and pull requests.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments

    Original Monopogen developers: Chen Lab for the foundational pipeline
    Bioinformatics community: For the excellent tools that make this possible

⭐ If this repository helped your research, please give it a star and cite both the original Monopogen paper and this repository!
