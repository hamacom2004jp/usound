.. -*- coding: utf-8 -*-

****************************************************
Command Reference ( speaker mode )
****************************************************

- List of speaker mode commands.

Capture speaker audio : `usound -m speaker -c capture <Option>`
==============================================================================

- Record audio output from the specified speaker.

.. csv-table::
    :widths: 20, 10, 70
    :header-rows: 1

    "Option","Required","Description"
    "--spid <speaker id>","","Specify the speaker to record by ID. If not specified, the first speaker found will be used."
    "--spname <speaker name>","","Specify the speaker to be recorded by name. If not specified, the first speaker found will be used."
    "--samplerate <rate>","","Specifies the sampling rate."
    "--duration <duration>","","Specifies the maximum number of seconds to buffer during recording. It will be chunked within this time."
    "--rectime <second>","","Specifies the recording time; if it is less than or equal to 0, it continues until the command is stopped."
    "--output_dir <dir>","","Specifies the directory where the recording files are stored."
    "--output_csv <file>","","Saves the recording file as a csv file. If specified, no standard output is performed."
    "--output_format <format>","","Specifies the format of the audio file."


List speaker : `usound -m speaker -c list <Option>`
==============================================================================

- Get a list of speakers.

.. csv-table::
    :widths: 20, 10, 70
    :header-rows: 1

    "Option","Required","Description"
    "--spid <speaker id>","","Filter by speaker name."
    "--spname <speaker name>","","Filter by speaker name."
