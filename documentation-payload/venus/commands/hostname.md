+++
title = "hostname"
chapter = false
weight = 100
hidden = false
+++

## Summary

Get the target machine's hostname.

- Needs Admin: False
- Version: 1
- Author: @mattreduce

## Usage

```
hostname
```

## MITRE ATT&CK Mapping

- T1082

## Detailed Summary

Uses the [os](https://nodejs.org/api/os.html) Node.js module to print the
hostname:

```JavaScript
output = os.hostname()
```
