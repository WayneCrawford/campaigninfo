Campaign information files
==========================

Programs and schemas for Marine Seismology "**campaign**" files.  A campaign is a single data collection unit (deployment and recovery during one cruise, or deployment on one cruise and recovery on another)

These are YAML or JSON files that describe an experiment from the point of view of the chief scientist, including information on what they want to see when validating the data (make sure that amplitudes and clock drifts are correct.

The are divided into five main sections:
  - ``operators``: A list of equipment operators and the stations they deployed
  - ``data_distribution``: restrictions to data distribution
  - ``fdsn_network``: information about the FDSN network corresponding to this campaign
  - ``validation_methods``: information of parameters used to validate (currently a list of waveform time windows)
  - ``expeditions``: An optional list of seagoing expeditions used for data collection.

For multiple-campaign experiments, you can also create "**experiment**" files, which avoid repeating some information that should be the same in each campaign file, (data distribution; fdsd_network; expedition names, ships and dates).

Example files are found in the ``_examples`` directory

Command-line programs
----------------------

- ``experiment_to_campaign``: make campaign files from an experiment file
- ``campaign_validate``: validates campaign or experiment files against schema
