# LSST:UK DAC Data Upload Tool

This is a Python tool that was created to facilitate the upload of large amounts of data from remote sites which are not part of GridPP (namely CSD3) to object storage on Echo, in SCD at RAL.

> [!WARNING]
> This is a largely untested tool and likely contains errors which could, possibly, cause irreparable damage to your data. You are *strongly* advised to not rely on this tool for data transfer if you have other options. In particular, _you should consider how you're going to long-term store your data *before* you create it on any particular HPC system._

## How does it work?

This tool is based on a number of components:

* A containerised version of the Rucio client (in Apptainer).
* A python script (`cataloguer.py`) which uses glob to create a catalogue (stack) of every file in a provided directory which matches a given search term.
* The main python script (`main.py`) designed to break the catalogue into batches, and upload a number of batches in parallel to a given Rucio RSE.

Once a client container has been created, the tool creates a working directory with multiple copies of that container, each uploading a batch of files. This is a crude and hacky way of running multiple containers - and therefore upload streams - in parallel. It does speed up the uploading of large amounts of data, but the relationship is not liner and 'your mileage may vary'.

Again - there are much better options for doing data upload than this tool; in particular, creating your data in the right (or close to the right) storage location in the first place.

## To use this tool you need to:

1. Clone the repo to the same system from where you are uploading data.

2. Copy your certificate and key (as `usercert.pem` and `userkey.pem`) into the same directory as this tool (for x509 authentication with your chosen Rucio instance).

3. Edit `rucio.cfg` with details of the Rucio instance you will be using, and your Rucio account (username). 

4. Build the Rucio client container from the `dac-upload-tool-v2.def` definition. You MUST name the resulting container `dac-upload-tool-v2.sif`.

The command for this is `apptainer build dac-upload-tool-v2.sif dac-upload-tool-v2.def`

> [!WARNING]
> Currently, the definition file requires grid certificates to be imported manually (from the grid-security directory in this repo) and installs the EGI trust anchors repo from a random GitHub repo (because it was easy). Both these are probably massive security risks, but unfortunately because the EGI trust anchors repo moved / got broken right at the end of my graduate project working on LSST, this was the only option available in the timeframe. _I will try to, but make no guarantee that I will be able to, fix this in the future._

5. Edit `main.py` to set:
* the batch size (number of files to upload in a single 'thread')
* the Rucio scope to which you want to upload
* the Rucio RSE to which you want to upload
* the maximum number of containers to run in parallel (in theory - more will speed up your upload process)

> [!INFO]
> The upload command includes the attribute `--lifetime 3600`. On a properly running Rucio server, this will result in any file you upload being delated after 1 hour (3600 seconds). If you're using this tool in production (and, again, you really should attempt any alternative you can before you do) you will want to remove this!

6. Authenticate with your chosen VO using vomses.

7. Run the tool using `python3 main.py`.

The tool should output a file, `summary.json`, containing details of every file which was uploaded. I am told this information will be sufficient for ingesting the data into the LSST Butler data curation system (though have not attempted to do so). 

## Isn't this a really bad way of solving the problem?

You bet it is. It's slow, cumbersome, and prone to known (and unknown) errors. Unfortunately, as long as user-generated data is being produced at non-GridPP HPC sites, which needs transferring to storage on Echo, this is the least terrible way I could think of.

## Help, it doesn't work!

You can email [mathew.sims@stfc.ac.uk](mailto:mathew.sims@stfc.ac.uk) and I will attempt to help you; however, this code was written on a graduate project and is not something I can promise I'll actively maintain.