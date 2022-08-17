#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the results in Weights & Biases

Author: 'Seun Ajayi
Date: August 2022
"""
import argparse
import logging
import wandb
import pandas as pd
from wandb_utils.log_artifact import log_artifact

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    logger.info("Downloading Artifact")
    local_path = wandb.use_artifact(args.input_artifact).file()
    df = pd.read_csv(local_path)

    logger.info("Dropping outliers")
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()

    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()
    
    logger.info("Converting last_review to datetime")
    df['last_review'] = pd.to_datetime(df['last_review'])

    filename='clean_sample.csv'
    df.to_csv(filename, index=False)

    logger.info("Logging Artifact")
    log_artifact(
        artifact_name=args.output_artifact,
        artifact_type=args.output_type,
        artifact_description=args.output_description,
        filename=filename,
        wandb_run=run
    )



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This step cleans the data")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Fully-qualified name for the input artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Name for the Output Artifact",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help='Type of the Output Artifact',
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help='Description of the Output Artifact',
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help='Minimum price',
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="Maximum price",
        required=True
    )


    args = parser.parse_args()

    go(args)
