<p align="center" style="margin-bottom: 0px !important;">
  <img width="200" src="agent_icons/venus.svg"
    alt="Venus, Greek goddess" align="center">
</p>
<h1 align="center" style="margin-top: 0px;">Venus<br/></h1>

Venus is a [VS Code](https://code.visualstudio.com/) extension that acts as an
agent for Mythic C2. It produces a zipped folder of VS Code extension source
code, which currently must be packaged by the operator before delivering to
target/test machines manually or via social engineering.

:white_check_mark: Cross-platform (tested on macOS, Linux, Windows)  
:warning: Doesn't support encrypted payloads yet, always use TLS  
:warning: Not yet dependable enough for operations  

## Installation

From the top-level directory of Mythic on your C2 server, run the command:

```shell
$ sudo ./mythic-cli install github https://github.com/MythicAgents/venus
```

or to install a specific Git branch of Venus:

```shell
$ sudo ./mythic-cli install github https://github.com/MythicAgents/venus branchname
```

## Usage

First, create a Venus Payload in Mythic and download it to your local machine. Make sure 
you have Node.js installed then get the `vsce` package and compile your extension like so:

```shell
$ npm install -g vsce
$ unzip venus.zip
$ cd venus
$ vsce package
```

The extension must then be manually installed on target in Visual Studio Code.
This can be done from the editor UI or from the CLI with:

```shell
$ code --install-extension venus-0.0.1.vsix
```

### Commands

Command | Syntax | Description
------- | ------ | -----------
current_user | `current_user` | Uses the `os` Node.js package to get information about the current user.
exit | `exit` | Exit a callback.
hostname | `hostname` | Uses the `os` Node.js package to return the target's hostname.
pwd | `pwd` | Prints the current working directory for the agent.
shell | `shell [command]` | Uses the `execSync()` Node.js function to execute arbitrary shell commands.

## Thank you

Venus icon made by [Freepik](https://www.flaticon.com/authors/freepik)

## Disclaimer

This is an open source project meant to be used with authorization to assess
security posture, and for research purposes. The authors of this project are
not liable for any damage caused by its misuse.
