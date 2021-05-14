Campaign information files
==========================

Programs and schemas for Marine Seismology "campaign" files

Also handles "experiment" files, which are a more efficient way to store
multiple campaigns.

They have a similar base structure to obsinfo information files, to simplify work for
anyone dealing with both.

Command-line programs

The InfoDict system used is probably too complicated, as we don't need advanced
element substitution
----------------------

experiment_to_campaign: make campaign files from an experiment file
campaign_validate: validates campaign or experiment files against schema