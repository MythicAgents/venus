from CommandBase import *
from MythicResponseRPC import *
import json

class ShellArguments(TaskArguments):
    def __init__(self, command_line):
        super().__init__(command_line)
        self.args = {
            "command": CommandParameter(
                name="command", type=ParameterType.String, description="Command to run"
            )
        }

    async def parse_arguments(self):
        if len(self.command_line) > 0:
            if self.command_line[0] == "{":
                self.load_args_from_json_string(self.command_line)
            else:
                self.add_arg("command", self.command_line)
        else:
            raise ValueError("Missing arguments")

class ShellCommand(CommandBase):
    cmd = "shell"
    needs_admin = False
    help_cmd = "shell {command}"
    description = "This uses the execSync() Node.js function to execute arbitrary shell commands."
    version = 1
    is_exit = False
    is_file_browse = False
    is_process_list = False
    is_download_file = False
    is_remove_file = False
    is_upload_file = False
    author = "@mattreduce"
    attackmapping = ["T1059"]
    argument_class = ShellArguments

    async def create_tasking(self, task: MythicTask) -> MythicTask:
        resp = await MythicResponseRPC(task).register_artifact(
            artifact_instance="{}".format(task.args.get_arg("command")),
            artifact_type="Process Create",
        )
        return task

    async def process_response(self, response: AgentResponse):
        pass
