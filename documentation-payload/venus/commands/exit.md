+++
title = "exit"
chapter = false
weight = 100
hidden = false
+++

## Summary

This ends the current Venus agent's main loop by using the `clearInterval()`
function.

- Needs Admin: False
- Version: 1
- Author: @mattreduce

## Usage

```
exit
```

## Detailed Summary

The command instructs the agent to exit on the next iteration of its main loop 
with this call:

```JavaScript
context.globalState.update('mustExit', 1);
```

The `mainLoop()` function then checks this value and exits if it is anything but 
`null`. Having handled the instruction to exit, it also clears out the value of 
`mustExit` in VS Code's global state storage:

```JavaScript
function mainLoop(context) {
	const mustExit = context.globalState.get('mustExit')

	if (mustExit != null) {
		// Find ID for main loop and stop it
		const intervalID = context.globalState.get('intervalID')
		clearInterval(intervalID)

		// Clear out the exit instruction
		context.globalState.update('mustExit', null)
	}
	getTasking(context)
}
```
