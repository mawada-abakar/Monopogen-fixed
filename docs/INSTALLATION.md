# Installation Guide for Monopogen-Fixed

This guide provides step-by-step instructions for installing and setting up Monopogen-Fixed, including options for users **without sudo privileges**.

## System Requirements

- **Operating System**: Linux or macOS
- **Memory**: At least 8GB RAM (16GB+ recommended)
- **Storage**: At least 10GB free space
- **CPU**: Multi-core processor recommended

---

## Part A: Install Required Software (Prerequisites)

Before installing Monopogen-Fixed, you need these three software packages:

### Software 1: Python 3.8+

**Check if already installed:**
```bash
python3 --version

If you have sudo privileges:

# Ubuntu/Debian:
sudo apt update
sudo apt install python3 python3-pip

# macOS (with Homebrew):
brew install python3

If you DON'T have sudo privileges:

# Download and install Miniconda (no sudo required)
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

# Follow the installer prompts, then restart your terminal
conda install python=3.8 pip

### Software 2: R 4.0+

Check if already installed:
R --version

If you have sudo privileges:
# Ubuntu/Debian:
sudo apt install r-base r-base-dev

# macOS (with Homebrew ):
brew install r

If you DON'T have sudo privileges:

# Install via conda
conda install -c conda-forge r-base

### Software 3: Bioinformatics Tools (samtools, bcftools, tabix)

Check if already installed:
samtools --version
bcftools --version
tabix --version

If you have sudo privileges:
# Ubuntu/Debian:
sudo apt install samtools bcftools tabix

# macOS (with Homebrew):
brew install samtools bcftools htslib

If you DON'T have sudo privileges:
# Install via conda (recommended)
conda install -c bioconda samtools bcftools htslib

# Verify installation
samtools --version
bcftools --version
tabix --version


## Part B: Install Monopogen-Fixed (Main Installation)

Now that you have the required software, follow these steps:

Step 1: Download Monopogen-Fixed

# Clone the repository
git clone https://github.com/mawada-abakar/Monopogen-fixed.git
cd Monopogen-fixed

Step 2: Install Python Packages

If you have sudo privileges:
# Install Python packages
pip3 install -r requirements.txt

If you DON'T have sudo privileges:
# Install with --user flag
pip3 install --user -r requirements.txt

# OR use conda
conda install -c conda-forge -c bioconda pysam pandas numpy scipy matplotlib seaborn

Verify Python packages:
python3 -c "import pysam, pandas, numpy; print('Python packages installed successfully')"

Step 3: Install R Packages

Option A: Use the provided script:
Rscript scripts/install_r_packages.R

Option B: Install manually in R:
# Open R console
R

# In R, install packages:
> install.packages(c("R.utils", "data.table", "reshape2", "ggplot2", "dplyr"), repos="https://cran.r-project.org/" )
> quit()

Option C: Use conda for R packages:
conda install -c conda-forge r-r.utils r-data.table r-reshape2 r-ggplot2 r-dplyr

Step 4: Set Up Environment and Scripts
```bash
# Set environment variable
export MONOPOGEN_PATH=$(pwd)

# Make scripts executable
chmod +x scripts/fix_vcf_headers.sh
chmod +x scripts/verify_setup.py

# Add to ~/.bashrc for persistence
echo "export MONOPOGEN_PATH=$(pwd)" >> ~/.bashrc
source ~/.bashrc

Step 5: Test Installation

# Test the main script
python3 src/Monopogen.py --help

# Test the VCF fix script
./scripts/fix_vcf_headers.sh --help

# Run setup verification
python3 scripts/verify_setup.py
# or
./scripts/verify_setup.py

# Verify Python environment
python3 -c "
import sys
print('Python version:', sys.version_info[:2])
if sys.version_info >= (3, 7):
    print('✅ Python version compatible')
else:
    print('❌ Python version too old, need 3.7+')
"

# If verification passes, you're ready to go!

# You should see the help message with available commands

Step 6: Download Reference Data

Your pipeline needs reference genome and population data to function properly.

Option A: Download Essential References (Recommended)
# Create reference directory
mkdir -p reference
cd reference

# Download human reference genome (GRCh38) - chromosome 20 only for testing
echo "Downloading reference genome (this may take a while)..."
wget -c http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/GRCh38_reference_genome/GRCh38_full_analysis_set_plus_decoy_hla.fa
wget -c http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/GRCh38_reference_genome/GRCh38_full_analysis_set_plus_decoy_hla.fa.fai

# Download 1000 Genomes reference panel (chr20 for testing )
echo "Downloading 1000 Genomes reference panel..."
wget -c http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1000_genomes_project/release/20190312_biallelic_SNV_and_INDEL/ALL.chr20.shapeit2_integrated_snvindels_v2a_27022019.GRCh38.phased.vcf.gz
wget -c http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1000_genomes_project/release/20190312_biallelic_SNV_and_INDEL/ALL.chr20.shapeit2_integrated_snvindels_v2a_27022019.GRCh38.phased.vcf.gz.tbi

# Verify downloads
echo "Verifying downloaded files..."
ls -lh *.fa *.fa.fai *.vcf.gz *.vcf.gz.tbi

cd ..

Option B: Use Your Own Reference Data
If you already have reference data, note the paths - you'll need them for configuration.

Step 7: Configure the Pipeline
# Copy the configuration template
cp config/config_template.ini config/config.ini

# Edit the configuration file
nano config/config.ini

Important: Update these paths in config/config.ini:
[PATHS]
# Update these paths to match your system
monopogen_path = /path/to/Monopogen-Fixed
reference_genome = /path/to/reference/GRCh38_full_analysis_set_plus_decoy_hla.fa
reference_panel = /path/to/reference/ALL.chr20.shapeit2_integrated_snvindels_v2a_27022019.GRCh38.phased.vcf.gz
bam_list_file = /path/to/your/bam_list.txt
output_dir = /path/to/your/output

[TOOLS]
# If using conda, these should work as-is
samtools = samtools
bcftools = bcftools
tabix = tabix
bgzip = bgzip

[PARAMETERS]
# Processing parameters
num_threads = 8
target_chromosomes = chr20

Step 8: Final Verification
# Test with your configuration
python3 src/main.py --help

# Run the comprehensive setup verification
./scripts/verify_setup.py

# Test configuration file parsing
python3 -c "
import configparser
config = configparser.ConfigParser( )
config.read('config/config.ini')
print('Configuration file loaded successfully')
print('Reference genome:', config.get('PATHS', 'reference_genome'))
"

## Quick Installation for Non-Sudo Users (All-in-One)

If you don't have sudo privileges, here's the complete process using conda:
# 1. Install Miniconda (if not already installed)
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
# Restart terminal after installation

# 2. Create a dedicated environment
conda create -n monopogen python=3.8
conda activate monopogen

# 3. Install all required software
conda install -c conda-forge -c bioconda samtools bcftools htslib pysam pandas numpy scipy
conda install -c conda-forge r-base r-r.utils r-data.table r-reshape2 r-ggplot2

# 4. Download and test Monopogen-Fixed
git clone https://github.com/mawada-abakar/Monopogen-fixed.git
cd Monopogen-fixed
export MONOPOGEN_PATH=$(pwd )
python3 src/Monopogen.py --help

# 5. Install Python dependencies
pip install -r requirements.txt

# 6. Test installation
python3 src/main.py --help
./scripts/verify_setup.py

##  Troubleshooting

Problem: "Permission denied" when installing packages

Solution:
# Use --user flag for pip
pip3 install --user package_name

# Or use conda instead
conda install package_name

Problem: "Command not found" for samtools/bcftools

Solution:
# Check if tools are in your PATH
which samtools
echo $PATH

# If using conda, activate your environment
conda activate monopogen

Problem: R packages fail to install

Solution:
# In R, set a local library path
R
> dir.create("~/R/library", recursive=TRUE)
> .libPaths(c("~/R/library", .libPaths()))
> install.packages("R.utils", lib="~/R/library")

Problem: Reference data download fails

Solution:
# Use wget with resume capability
wget -c [URL]

# Or use curl instead
curl -C - -O [URL]

# Check available disk space
df -h

Problem: Configuration file errors

Solution:
# Verify configuration syntax
python3 -c "
import configparser
config = configparser.ConfigParser()
try:
    config.read('config/config.ini')
    print('Configuration file is valid')
except Exception as e:
    print('Configuration error:', e)
"








