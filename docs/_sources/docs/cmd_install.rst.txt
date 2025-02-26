.. -*- coding: utf-8 -*-

****************************************************
Command Reference ( install mode )
****************************************************

- List of install mode commands.

Installation (server) : `usound -m install -c server <Option>`
==============================================================================

- Build a docker image `build` of the `inference server`. The options are as follows.
- If the `build` is successful, a `docker-compose.yml` file will be generated in the runtime directory.
- To start the server, run `docker-compose up -d` at the location where the `docker-compose.yml` file is located.
- To stop the server, run `docker-compose down` at the location where the `docker-compose.yml` file is located.
- This command is not yet supported in the windows environment.
- In a windows environment, run `usound -m whisper -c deploy` and `usound -m whisper -c start` directly.


.. csv-table::
    :widths: 20, 10, 70
    :header-rows: 1

    "Option","Required","Description"
    "--data <data folder>","","If omitted, use `$HONE/.usound`."
    "--install_cmdbox <cmdbox module name>","","If omitted, `cmdbox` is used. You can also specify `cmdbox==0.4.5`."
    "--install_usound <usound module name>","","If omitted, `usound` is used. You can also specify `usound==0.1.1`."
    "--install_from <Image Name>","","Specify the FROM image that will be the source of the docker image to be created."
    "--install_no_python","","Do not install `python` in the docker image."
    "--install_tag <Additional tag names>","","If specified, it can be appended to the tag name of the docker image to be created."
    "--install_use_gpu","","Install in a modular configuration that uses GPUs."
