+++
title = "OPSEC"
chapter = false
weight = 10
pre = "<b>1. </b>"
+++

## Considerations

The Venus agent does not yet utilize AES encryption for C2 communications. Be 
sure to always use TLS/HTTPS in the meantime.

### Indicators

* Records in globalState (SQLite3 database)
* Payload is present in VS Code extensions folder (OS-dependent)