from mythic_payloadtype_container.MythicCommandBase import *
import json

class HostnameArguments(TaskArguments):
    def __init__(self, command_line):
        super().__init__(command_line)
        self.args = {}

    async def parse_arguments(self):
        pass

class HostnameCommand(CommandBase):
    cmd = "hostname"
    needs_admin = False
    help_cmd = "hostname"
    description = "This uses the `os` Node.js package to return the target's hostname."
    version = 1
    author = "@mattreduce"
    attackmapping = ["T1016"]
    argument_class = HostnameArguments

    async def create_tasking(self, task: MythicTask) -> MythicTask:
        return task

    async def process_response(self, response: AgentResponse):
        pass