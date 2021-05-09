from mythic_payloadtype_container.MythicCommandBase import *
import json

class PwdArguments(TaskArguments):
    def __init__(self, command_line):
        super().__init__(command_line)
        self.args = {}

    async def parse_arguments(self):
        pass

class PwdCommand(CommandBase):
    cmd = "pwd"
    needs_admin = False
    help_cmd = "pwd"
    description = "Prints the current working directory for the agent"
    version = 1
    author = "@mattreduce"
    attackmapping = ["T1083"]
    argument_class = PwdArguments

    async def create_tasking(self, task: MythicTask) -> MythicTask:
        return task

    async def process_response(self, response: AgentResponse):
        pass