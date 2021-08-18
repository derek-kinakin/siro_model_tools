"""Combine Block Stats exported from SiroModel into a single database.

Block Stats files are exported from SiroModel via the 
"File - Save - Block Statistics" menu option for all file currently loaded in
the Block Model Analysis tool.
"""

__author__ = "Derek Kinakin"
__email__ = "dkinakin@gmail.com"
__copyright__ = "Copyright 2021, Derek Kinakin"
__license__ = "GPL3"
__status__ = "Development"


import os
import ntpath
import pandas as pd
from tqdm import tqdm


# Globals
SIMULATION_NAME = "case_1"

STATS_FILES_PATH = r"C:\Users\dkinakin\Desktop\Model_runs\case_1\block_stats"

csv_results_file = os.path.join(
    STATS_FILES_PATH,
    "combined_blockstats_{0}.csv".format(SIMULATION_NAME)
    )

BLK_FILE_HEADER = ["Blk_num","Num_Faces","Num_Vrts","NRFlag","CentE","CentN",
                    "CentEl","SArea","Vol","RVE","RVN","RVEl","RVDip","RVDD",
                    "FOS","ExpArea","TopFlg","Num_Fracs","Frac Area",
                    "Blk Radius","Pore Pressure"]

DB_HEADER = ["CentE","CentN","CentEl","FOS","Blk_num","Num_Faces","Num_Vrts",
             "NRFlag","SArea","Vol","RVE","RVN","RVEl","RVDip","RVDD","ExpArea",
             "TopFlg","Num_Fracs","Frac Area","Blk Radius","Pore Pressure",
             "run"]

# Functions
def create_blockstat_file_list(pth, file_ext="txt"):
    fd_cnts = os.listdir(pth)
    blk_fl_lst = [os.path.join(pth, f) for f in fd_cnts if f.endswith(file_ext)]
    return blk_fl_lst


def read_block_stats_file(bf, header=BLK_FILE_HEADER):
    bf_header = BLK_FILE_HEADER
    bfd = pd.read_csv(bf, sep="\t", skiprows=13, header=None, names=bf_header)
    return bfd


def run_number_from_path(pth):
    fn = ntpath.basename(i)
    rnm = fn.split(".")[0]
    rn = rnm.split("Stats")[1]
    return rn

# Main
if __name__ == "__main__":
    block_file_list = create_blockstat_file_list(STATS_FILES_PATH)
    results_df = pd.DataFrame(columns=DB_HEADER)
    with tqdm(total=len(block_file_list), desc="COMBINING BLOCKSTATS") as pbar:
        for i in block_file_list:
            df = read_block_stats_file(i)
            df["run"] = run_number_from_path(i)
            results_df = results_df.append(df, ignore_index=True)
            pbar.update()

    results_df.to_csv(csv_results_file, index=False)
