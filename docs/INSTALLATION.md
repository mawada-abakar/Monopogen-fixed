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


## Part A: Install Monopogen-Fixed (Main Installation)

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

Step 4: Set Up Environment

# Set environment variable
export MONOPOGEN_PATH=$(pwd)

# Make it permanent (add to ~/.bashrc)
echo "export MONOPOGEN_PATH=$(pwd)" >> ~/.bashrc
source ~/.bashrc

Step 5: Test Installation

# Test the main script
python3 src/Monopogen.py --help

# You should see the help message with available commands

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








