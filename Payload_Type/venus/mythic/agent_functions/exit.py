from mythic_payloadtype_container.MythicCommandBase import *
import json

class ExitArguments(TaskArguments):
    def __init__(self, command_line):
        super().__init__(command_line)
        self.args = {}

    async def parse_arguments(self):
        pass

class ExitCommand(CommandBase):
    cmd = "exit"
    needs_admin = False
    help_cmd = "exit"
    description = "Exit the extension on next interval (does not uninstall)"
    version = 1
    supported_ui_features = ["callback_table:exit"]
    author = "@mattreduce"
    attackmapping = []
    argument_class = ExitArguments

    async def create_tasking(self, task: MythicTask) -> MythicTask:
        return task

    async def process_response(self, response: AgentResponse):
        pass