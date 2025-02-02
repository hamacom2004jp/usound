.. -*- coding: utf-8 -*-

****************************************************
Command Reference ( whisper mode )
****************************************************

- List of whisper mode commands.

Whisper model deploy : `usound -m whisper -c deploy <Option>`
==============================================================================

- Deploy a model to extract text from audio.

.. csv-table::
    :widths: 20, 10, 70
    :header-rows: 1

    "Option","Required","Description"
    "--host <IP address or host name>","","Specify the service host of the Redis server."
    "--port <port number>","","Specify the service port of the Redis server."
    "--password <password>","","Specify the access password of the Redis server (optional). If omitted, `password` is used."
    "--svname <Service Name>","","Specify the service name of the inference server. If omitted, `server` is used."
    "--name <Name>","","Specify the registration name of the AI model."
    "--model_size <Size Name>","","Specifies the size of the model."
    "--device <device>","","Specifies the calculation device."
    "--device_index <index>","","Specifies the GPUID when the GPU is used in `device`."
    "--compute_type <type>","","Specifies the weight type of the model."
    "--cpu_threads <count>","","Specifies the number of threads to be used when executing on the CPU."
    "--num_workers <count>","","Specify the number of workers to perform text extraction."
    "--overwrite","","Specify to overwrite even if it is already deployed."
    "--retry_count <Number of retries>","","Specifies the number of reconnections to the Redis server.If less than 0 is specified, reconnection is forever."
    "--retry_interval <Retry Interval>","","Specifies the number of seconds before reconnecting to the Redis server."
    "--timeout <time-out>","","Specify the maximum waiting time until the server responds."


Whisper model start : `usound -m whisper -c start <Option>`
==============================================================================

- Start deployed model.

.. csv-table::
    :widths: 20, 10, 70
    :header-rows: 1

    "Option","Required","Description"
    "--host <IP address or host name>","","Specify the service host of the Redis server."
    "--port <port number>","","Specify the service port of the Redis server."
    "--password <password>","","Specify the access password of the Redis server (optional). If omitted, `password` is used."
    "--svname <Service Name>","","Specify the service name of the inference server. If omitted, `server` is used."
    "--name <Name>","","Specify the registration name of the AI model."
    "--retry_count <Number of retries>","","Specifies the number of reconnections to the Redis server.If less than 0 is specified, reconnection is forever."
    "--retry_interval <Retry Interval>","","Specifies the number of seconds before reconnecting to the Redis server."
    "--timeout <time-out>","","Specify the maximum waiting time until the server responds."


Whisper model stop : `usound -m whisper -c stop <Option>`
==============================================================================

- Stop deployed model.

.. csv-table::
    :widths: 20, 10, 70
    :header-rows: 1

    "Option","Required","Description"
    "--host <IP address or host name>","","Specify the service host of the Redis server."
    "--port <port number>","","Specify the service port of the Redis server."
    "--password <password>","","Specify the access password of the Redis server (optional). If omitted, `password` is used."
    "--svname <Service Name>","","Specify the service name of the inference server. If omitted, `server` is used."
    "--name <Name>","","Specify the registration name of the AI model."
    "--retry_count <Number of retries>","","Specifies the number of reconnections to the Redis server.If less than 0 is specified, reconnection is forever."
    "--retry_interval <Retry Interval>","","Specifies the number of seconds before reconnecting to the Redis server."
    "--timeout <time-out>","","Specify the maximum waiting time until the server responds."


Whisper model transcribe : `usound -m whisper -c transcribe <Option>`
==============================================================================

- Perform text extraction using the deployed model.

.. csv-table::
    :widths: 20, 10, 70
    :header-rows: 1

    "Option","Required","Description"
    "--host <IP address or host name>","","Specify the service host of the Redis server."
    "--port <port number>","","Specify the service port of the Redis server."
    "--password <password>","","Specify the access password of the Redis server (optional). If omitted, `password` is used."
    "--svname <Service Name>","","Specify the service name of the inference server. If omitted, `server` is used."
    "--input_file <file>","","Specify the audio file from which to extract text."
    "--input_format <format>","","Specifies the format of the input file."
    "--stdin","","Read the audio to be text extracted from the standard input."
    "--best_of <number>","","Number of candidates to sample when temperature is non-zero."
    "--beam_size <number>","","Parameters of the beam search. This number of searches is used to select the best word connection."
    "--patience <number>","","Parameters for beam search. A patience factor of 1.0 terminates the search when the best result is found; a patience factor of 0.5 terminates the search at 50%."
    "--length_penalty <number>","","Parameters for beam search. Penalty on the length of the generated series; if less than 1, longer series are more likely to be preferred."
    "--temperature <number>","","Confidence. the closer to 0, the more certain the choice, and the further away from 0, the more diverse the choices."
    "--compression_ratio_threshold <number>","","If the gzip compression ratio is higher than this value, the decoded string is treated as a failure because it is redundant."
    "--log_prob_threshold <number>","","If the average log probability is lower than this value, the decoding is treated as a failure."
    "--no_speech_threshold <number>","","If the token probability is higher than this value and decoding fails due to 'logprob_threshold', the segment is considered silent."
    "--condition_on_previous_text","","If specified, the previous output of the model is specified as the prompt for the next window for consistent output."
    "--initial_prompt <prompt>","","The model's initial window prompts."
    "--prefix <prefix>","","Text to be used as the initial window prefix for the audio."
    "--suppress_blank <True/False>","","Suppress blank output at the beginning of sampling."
    "--without_timestamps","","Do not output text containing timestamps."
    "--max_initial_timestamp <number>","","Specifies that the initial timestamp of the audio will not be later than this value."
    "--word_timestamps","","Generate a timestamp for each word."
    "--vad_filter","","Enable Voice Activity Detection (VAD) to filter out unvoiced portions of audio."
    "--output_lang <lang>","","Specify the audio file from which to extract text."
    "--retry_count <Number of retries>","","Specifies the number of reconnections to the Redis server.If less than 0 is specified, reconnection is forever."
    "--retry_interval <Retry Interval>","","Specifies the number of seconds before reconnecting to the Redis server."
    "--timeout <time-out>","","Specify the maximum waiting time until the server responds."
