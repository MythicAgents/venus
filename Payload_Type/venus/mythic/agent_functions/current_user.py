from mythic_payloadtype_container.MythicCommandBase import *
import json

class CurrentUserArguments(TaskArguments):
    def __init__(self, command_line):
        super().__init__(command_line)
        self.args = {}

    async def parse_arguments(self):
        pass

class CurrentUserCommand(CommandBase):
    cmd = "current_user"
    needs_admin = False
    help_cmd = "current_user"
    description = "This uses the `os` Node.js package to get information about the current user."
    version = 1
    author = "@mattreduce"
    attackmapping = ["T1033"]
    argument_class = CurrentUserArguments

    async def create_tasking(self, task: MythicTask) -> MythicTask:
        return task

    async def process_response(self, response: AgentResponse):
        pass