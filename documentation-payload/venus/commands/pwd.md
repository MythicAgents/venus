+++
title = "pwd"
chapter = false
weight = 100
hidden = false
+++

## Summary

Prints the current working directory for the agent.

- Needs Admin: False
- Version: 1
- Author: @mattreduce

## Usage

```
pwd
```

## MITRE ATT&CK Mapping

- T1083

## Detailed Summary

Uses the [process](https://nodejs.org/api/process.html) Node.js object to print
the current working directory:

```JavaScript
output = process.cwd()
```
