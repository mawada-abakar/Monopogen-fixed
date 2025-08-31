#!/usr/bin/env python

import os
import sys
import logging
from multiprocessing import Pool

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(levelname)-8s\t%(filename)s\t%(message)s")

def BamFilter(para):
    """
    Filter BAM file for a specific chromosome and sample.
    This function was missing in the original script and has been added.
    """
    chr_region = para['chr']
    out_dir = para['out']
    sample_id = para['id']
    bam_file = para['bamFile']
    samtools_path = para['samtools']
    
    # Create output directory if it doesn't exist
    bam_out_dir = os.path.join(out_dir, "Bam")
    os.makedirs(bam_out_dir, exist_ok=True)
    
    # Define output filtered BAM file path
    output_bam = os.path.join(bam_out_dir, f"{sample_id}_{chr_region}.filter.bam")
    
    # Build the samtools command to filter by region and quality
    # Filters for mapping quality >= 20 and includes the header
    cmd = f"{samtools_path} view -b -q 20 -h {bam_file} {chr_region} > {output_bam}"
    
    logger.debug(f"Filtering BAM for sample {sample_id}, region {chr_region}")
    logger.debug(f"Executing command: {cmd}")
    
    # Execute the filtering command
    result = os.system(cmd)
    
    if result == 0:
        # Index the filtered BAM file for quick access
        index_cmd = f"{samtools_path} index {output_bam}"
        index_result = os.system(index_cmd)
        
        if index_result == 0:
            logger.debug(f"Successfully filtered and indexed BAM for {sample_id}_{chr_region}")
            return output_bam
        else:
            logger.error(f"Failed to index filtered BAM for {sample_id}_{chr_region}")
            return None
    else:
        logger.error(f"Failed to filter BAM for {sample_id}_{chr_region}")
        return None

def preProcess(args):
    """
    Preprocess BAM files by filtering and splitting by chromosome.
    """
    logger.info("Performing data preprocess before variant calling...")
    
    # Define paths and parameters from arguments
    bam_list_file = args.bamFile
    out_dir = args.out
    n_threads = args.nthreads
    max_mismatch = args.max_mismatch
    apps_path = args.apps
    
    # Define samtools path (this was missing)
    samtools_path = os.path.join(apps_path, "samtools")
    
    # Check if samtools executable exists
    if not os.path.isfile(samtools_path):
        logger.error(f"samtools not found at expected path: {samtools_path}")
        sys.exit(1)

    # Read BAM list file
    with open(bam_list_file, "r") as f:
        bam_records = [line.strip().split(',') for line in f]

    # Create a list of parameters for parallel processing
    para_lst = []
    # Assuming a single chromosome 'chr20' as per the user's context.
    # This can be expanded to read from a region file if needed.
    chromosomes = ["chr20"] 
    
    for record in bam_records:
        sample_id = record[0]
        bam_file = record[1]
        logger.debug(f"PreProcessing sample {sample_id}")
        
        for chrom in chromosomes:
            para_single = {
                "chr": chrom,
                "out": out_dir,
                "id": sample_id,
                "bamFile": bam_file,
                "max_mismatch": max_mismatch,
                "samtools": samtools_path
            }
            para_lst.append(para_single)

    # Use multiprocessing to run BamFilter in parallel
    with Pool(processes=n_threads) as pool:
        # The 'BamFilter' function is now defined, so this will work
        results = pool.map(BamFilter, para_lst)

    # Check for errors
    if None in results:
        logger.error("Some BAM filtering jobs failed. Please check the logs.")
    else:
        logger.info("BAM file preprocessing completed successfully.")

# Note: Other functions from the original bamProcess.py (like those for germline/somatic)
# are assumed to be in their respective files (germline.py, somatic.py)
