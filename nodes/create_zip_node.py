import shutil
import os

def zip_project_folder(project_folder_path, output_zip_path):
    zip_file_path = shutil.make_archive(output_zip_path, 'zip', project_folder_path)
    return zip_file_path

# Node
def create_zip(state):
    project_path = "project_root"
    zip_output_path = "final_project/"
    zip_path = zip_project_folder(project_path, zip_output_path)
    return state