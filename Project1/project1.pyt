import arcpy
import os
import runpy

class Toolbox(object):
    def __init__(self):
        self.label = "Project 1 Toolbox"
        self.alias = "project1"
        self.tools = [RunProject1Script]

class RunProject1Script(object):
    def __init__(self):
        self.label = "Run Project 1 (JSON → Shapefile)"
        self.description = "Runs the professor's original project1.py script."

    def getParameterInfo(self):
        p_folder = arcpy.Parameter(
            displayName="Project Folder (contains project1.py and no_tax.json)",
            name="project_folder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )
        return [p_folder]

    def execute(self, parameters, messages):
        project_folder = parameters[0].valueAsText

        py_path = os.path.join(project_folder, "project1.py")
        json_path = os.path.join(project_folder, "no_tax.json")

        if not os.path.exists(py_path):
            raise FileNotFoundError(f"project1.py not found in: {project_folder}")

        if not os.path.exists(json_path):
            raise FileNotFoundError(f"no_tax.json not found in: {project_folder}")

        messages.addMessage(f"Running: {py_path}")
        messages.addMessage(f"Using JSON: {json_path}")

        # Make relative paths work by changing cwd
        old_cwd = os.getcwd()
        os.chdir(project_folder)

        try:
            runpy.run_path(py_path, run_name="__main__")
        finally:
            os.chdir(old_cwd)

        messages.addMessage("✅ Done. The shapefile should be created where 'workspace' points inside project1.py.")
