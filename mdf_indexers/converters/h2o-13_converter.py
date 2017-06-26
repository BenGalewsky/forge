import json
import sys
import os
from ..utils.file_utils import find_files
from ..parsers.ase_parser import parse_ase
from tqdm import tqdm
from ..validator.schema_validator import Validator

# VERSION 0.2.0

# This is the converter for the H2O-13 dataset: Machine-learning approach for one- and two-body corrections to density functional theory: Applications to molecular and condensed water
# Arguments:
#   input_path (string): The file or directory where the data resides.
#       NOTE: Do not hard-code the path to the data in the converter (the filename can be hard-coded, though). The converter should be portable.
#   metadata (string or dict): The path to the JSON dataset metadata file, a dict or json.dumps string containing the dataset metadata, or None to specify the metadata here. Default None.
#   verbose (bool): Should the script print status messages to standard output? Default False.
#       NOTE: The converter should have NO output if verbose is False, unless there is an error.
def convert(input_path, metadata=None, verbose=False):
    if verbose:
        print("Begin converting")

    # Collect the metadata
    if not metadata:
        dataset_metadata = {
            "mdf-title": "Machine-learning approach for one- and two-body corrections to density functional theory: Applications to molecular and condensed water",
            "mdf-acl": ['public'],
            "mdf-source_name": "h2o-13",
            "mdf-citation": ["Albert P. Bartók, Michael J. Gillan, Frederick R. Manby, Gábor Csányi: Machine-learning approach for one- and two-body corrections to density functional theory: Applications to molecular and condensed water, Physical Review B 88(5): 054104, 2013. http://dx.doi.org/10.1103/PhysRevB.88.054104"],
            "mdf-data_contact": {

                "given_name": "Albert P.",
                "family_name": "Bartók",
                
                "email": "ab686@eng.cam.ac.uk",
                "instituition": "University of Cambridge"

                },

            "mdf-author": [{
                
                "given_name": "Albert P.",
                "family_name": "Bartók",
                
                "email": "ab686@eng.cam.ac.uk",
                "instituition": "University of Cambridge"
                
                },
                {
                    
                "given_name": "Michael J.",
                "family_name": "Gillan",
                
                "institution": "University College London"
                
                },
                {
                
                "given_name": "Frederick R.",
                "family_name": "Manby",
                
                "instituition": "University of Bristol",
                
                },
                {
                
                "given_name": "Gábor",
                "family_name": "Csányi",
                
                "instituition": "University of Cambridge",
                
                }],

#            "mdf-license": "",

            "mdf-collection": "h2o-13",
            "mdf-data_format": ["xyz"],
            "mdf-data_type": ["DFT", "PBE"],
#            "mdf-tags": ,

            "mdf-description": "Water monomer and dimer geometries, with calculations at DFT, MP2 and CCSD(T) level of theory. 7k water monomer geometries corresponding to a grid, with energies and forces at DFT / BLYP, PBE, PBE0 with AV5Z basis set",
            "mdf-year": 2013,

            "mdf-links": {

                "mdf-landing_page": "http://qmml.org/datasets.html#h2o-13",

                "mdf-publication": ["https://doi.org/10.1103/PhysRevB.88.054104"],
                "mdf-dataset_doi": "http://qmml.org/Datasets/h2o-13.tar.bz2",

#                "mdf-related_id": ,

                # data links: {
                
                    #"globus_endpoint": ,
                    #"http_host": ,

                    #"path": ,
                    #}
                },

#            "mdf-mrr": ,

            "mdf-data_contributor": [{
                "given_name": "Evan",
                "family_name": "Pike",
                "email": "dep78@uchicago.edu",
                "institution": "The University of Chicago",
                "github": "dep78"
                }]
            }
        
    elif type(metadata) is str:
        try:
            dataset_metadata = json.loads(metadata)
        except Exception:
            try:
                with open(metadata, 'r') as metadata_file:
                    dataset_metadata = json.load(metadata_file)
            except Exception as e:
                sys.exit("Error: Unable to read metadata: " + repr(e))
    elif type(metadata) is dict:
        dataset_metadata = metadata
    else:
        sys.exit("Error: Invalid metadata parameter")



    # Make a Validator to help write the feedstock
    # You must pass the metadata to the constructor
    # Each Validator instance can only be used for a single dataset
    # If the metadata is incorrect, the constructor will throw an exception and the program will exit
    dataset_validator = Validator(dataset_metadata)


    # Get the data
    #    Each record should be exactly one dictionary
    #    You must write your records using the Validator one at a time
    #    It is recommended that you use a parser to help with this process if one is available for your datatype
    #    Each record also needs its own metadata
    for data_file in tqdm(find_files(input_path, "xyz"), desc="Processing files", disable=not verbose):
        record = parse_ase(os.path.join(data_file["path"], data_file["filename"]))
        uri = "https://data.materialsdatafacility.org/collections/" + "h2o-13/" + data_file["no_root_path"] + '/' + data_file["filename"]
        record_metadata = {
            "mdf-title": "H2O-13 - " + record["chemical_formula"],
            "mdf-acl": ['public'],

#            "mdf-tags": ,
#            "mdf-description": ,
            
            "mdf-composition": record["chemical_formula"],
#            "mdf-raw": ,

            "mdf-links": {
                "mdf-landing_page": uri,

#                "mdf-publication": ,
#                "mdf-dataset_doi": ,

#                "mdf-related_id": ,

                "data_links": {
                    "globus_endpoint": "82f1b5c6-6e9b-11e5-ba47-22000b92c6ec",
                    #"http_host": ,

                    "path": "/collections/h2o-13/" + data_file["no_root_path"] + "/" + data_file["filename"],
                    },
                },

#            "mdf-citation": ,
#            "mdf-data_contact": {

#                "given_name": ,
#                "family_name": ,

#                "email": ,
#                "institution":,

#                },

#            "mdf-author": ,

#            "mdf-license": ,
#            "mdf-collection": ,
#            "mdf-data_format": ,
#            "mdf-data_type": ,
#            "mdf-year": ,

#            "mdf-mrr":

#            "mdf-processing": ,
#            "mdf-structure":,
            }

        # Pass each individual record to the Validator
        result = dataset_validator.write_record(record_metadata)

        # Check if the Validator accepted the record, and print a message if it didn't
        # If the Validator returns "success" == True, the record was written successfully
        if result["success"] is not True:
            print("Error:", result["message"])

    # You're done!
    if verbose:
        print("Finished converting")
