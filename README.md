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

# Run the pipeline
python src/Monopogen.py --help

📖 Documentation

    Installation Guide - Detailed setup instructions
    Tutorial - Complete walkthrough
    Troubleshooting - Common issues and solutions

🔧 Key Fixes Applied
1. Samtools/Bcftools Compatibility

    Updated from deprecated samtools mpileup to modern bcftools mpileup
    Removed incompatible flags (-t DP, --incl-flags, --excl-flags)
    Added proper BCF output formatting (-Ou)

2. VCF Header Issues

    Added missing contig definitions (##contig=<ID=chr20,length=64444167>)
    Fixed header format for downstream compatibility
    Automated header validation and fixing

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
