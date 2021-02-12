+++
title = "shell"
chapter = false
weight = 100
hidden = false
+++

## Summary

Executes arbitrary shell commands.

- Needs Admin: False
- Version: 1
- Author: @mattreduce

### Arguments

#### command

- Description: Command to run  
- Required Value: True  
- Default Value: None  

## Usage

### Without Popup

```
shell {command}
```

## MITRE ATT&CK Mapping

- T1059

## Detailed Summary

This uses the `execSync()` Node.js function to execute arbitrary shell
commands:

```JavaScript
const cmd = JSON.parse(parameters)['command']
output = execSync(cmd).toString()
```
