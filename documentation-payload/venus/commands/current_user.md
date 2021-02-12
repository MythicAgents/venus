+++
title = "current_user"
chapter = false
weight = 100
hidden = false
+++

## Summary

Prints the current user for the agent.

- Needs Admin: False  
- Version: 1  
- Author: @mattreduce  

## Usage

```
current_user
```

## MITRE ATT&CK Mapping

- T1033  

## Detailed Summary

Uses the [os](https://nodejs.org/api/os.html) Node.js module to print the
current user:

```JavaScript
output = os.userInfo().username
```
