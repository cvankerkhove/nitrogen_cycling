################################################################################
'''
RUFAS: Ruminant Farm Systems Model
File name: output_handler.py
Description: Contains the definition of the OutputHandler object
Author(s): Kass Chupongstimun, kass_c@hotmail.com
'''
##############################################################################

from Outputs import util1
from pathlib import Path
from Outputs.reporthandler import BaseReportHandler
#---------------------------------------------------------------------------
# Method: initialize_output_dir
#---------------------------------------------------------------------------
def initialize_output_dir(output_dir):
    '''
    If a directory of the same name exists, it and its contents is deleted,
    then creates the directory for all output report files as specified.
    Sets output file path for all reports through the class attribute of the
    BaseReportHandler class.

    Args:
        output_dir (Path): The path to the directory that will store all
            output report files.
    '''

    # Initialize path for reports
    output_dir = util1.get_base_dir() / output_dir

    # Delete directory if previously exists
    if output_dir.exists():
        for file in output_dir.iterdir():
            file.unlink()
        output_dir.rmdir()

    output_dir.mkdir(exist_ok = True, parents = False)
    BaseReportHandler.set_dir(output_dir)
