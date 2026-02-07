import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    working_directory_abs_path = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_directory_abs_path, file_path))
    valid_target_dir = os.path.commonpath([working_directory_abs_path, target_file]) == working_directory_abs_path

    if not valid_target_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if not target_file.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file'
    
    command = ["python", target_file]
    if args:
        command.extend(args)
    
    try:
        completed_process = subprocess.run(
            command,
            cwd=working_directory_abs_path, 
            capture_output=True,
            text=True,
            timeout=30)
        output_parts = []

        if completed_process.returncode != 0:
            output_parts.append(f'Process exited with code {completed_process.returncode}')
        if not completed_process.stdout and not completed_process.stderr:
            output_parts.append("No output produced")
        if completed_process.stdout:
            output_parts.append(f'STDOUT:\n{completed_process.stdout}')
        if completed_process.stderr:
            output_parts.append(f'STDERR:\n{completed_process.stderr}')
        return '\n'.join(output_parts)
        

    except Exception as e:
        return f'Error: executing python file: {e}'
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a given python file",
    parameters=types.Schema(
        required=["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file to run"
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional arguments",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Individual command line argument string"
                ),
            ),
        },
    ),
)