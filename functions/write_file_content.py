import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        working_directory_abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_abs_path, file_path))
        valid_target_dir = os.path.commonpath([working_directory_abs_path, target_file]) == working_directory_abs_path
        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as e:
        return f'Error: writing to file failed: {e}'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes given content to a given file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content given to write into the file"
            ),
        },
    ),
)
