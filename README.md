<p align="center" style="margin-bottom: 0px !important;">
  <img width="200" src="agent_icons/venus.svg"
    alt="Venus, Greek goddess" align="center">
</p>
<h1 align="center" style="margin-top: 0px;">Venus<br/></h1>

Venus is a [VS Code](https://code.visualstudio.com/) extension that acts as an
agent for Mythic C2. It produces a `.vsix` extension file that can be delivered
to target/test machines manually or via social engineering. The extension must
then be manually installed in Visual Studio Code. This can be done from the CLI
like so:

```shell
$ code --install-extension my-extension-0.0.1.vsix
```

:warning: Doesn't support encrypted payloads yet, always use TLS  
:warning: Not yet dependable enough for operations  
:warning: Only tested against macOS and Linux, should run anywhere in Visual Studio Code

## Mythic Payload Type installation

From the top-level directory of Mythic on your C2 server, run the command:

```shell
$ sudo ./install_agent_from_github.sh https://github.com/mattreduce/venus
```

Once installed, restart Mythic to build a new Venus agent.

## Thank you

Venus icon made by [Freepik](https://www.flaticon.com/authors/freepik)

## Disclaimer

This is an open source project meant to be used with authorization to assess
security posture, and for research purposes. The authors of this project are
not liable for any damage caused by its misuse.
