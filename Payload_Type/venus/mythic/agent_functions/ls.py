from mythic_payloadtype_container.MythicCommandBase import *
import json

class LsArguments(TaskArguments):
    def __init__(self, command_line):
        super().__init__(command_line)
        self.args = {
            "path": CommandParameter(
                name="path",
                type=ParameterType.String,
                default_value=".",
                description="Path of file or folder on the current system to list",
            )
        }

    async def parse_arguments(self):
        if len(self.command_line) > 0:
            if self.command_line[0] == "{":
                temp_json = json.loads(self.command_line)
                if "host" in temp_json:
                    # this means we have tasking from the file browser rather than the popup UI
                    # the Venus agent doesn't currently have the ability to do _remote_ listings, so we ignore it
                    self.add_arg("path", temp_json["path"] + "/" + temp_json["file"])
                    self.add_arg("file_browser", True, type=ParameterType.Boolean)
                else:
                    self.add_arg("path", temp_json["path"])
            else:
                self.add_arg("path", self.command_line)

class LsCommand(CommandBase):
    cmd = "ls"
    needs_admin = False
    help_cmd = "ls /path/to/file"
    description = "List a given directory"
    version = 1
    author = "@mattreduce"
    attackmapping = ["T1083"]
    argument_class = LsArguments
    attributes = CommandAttributes(
        spawn_and_injectable=True,
        supported_os = [
            SupportedOS.Linux,
            SupportedOS.MacOS,
            SupportedOS.Windows
        ],
    )

    async def create_tasking(self, task: MythicTask) -> MythicTask:
        task.display_params = task.args.get_arg("path")
        return task

    async def process_response(self, response: AgentResponse):
        pass
