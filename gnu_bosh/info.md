# GNU BOSH

This folder contains a modified version of gnu_bash which sends all commands run to an endpoint.

## Setup and Install

Can be setup by changing the IP or url in the curl command found at the bottom of the execute_command_internal function in the execute_cmd.c file. Set it to an endpoint which you control, and have a system similar to test_endpoint (a simple flask server) running on it, which can recive the requests.
