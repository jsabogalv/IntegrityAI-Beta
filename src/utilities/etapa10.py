import os
import subprocess

def execute(project_name, is_secopii_checked):
    project_dir = os.path.join(os.path.dirname(__file__), '../../projects', project_name)
    dashsecop_path = os.path.join(project_dir, 'DashSecop.py')

    if is_secopii_checked:
        # Ejecutar DashSecop.py
        if os.path.exists(dashsecop_path):
            subprocess.run(['python', dashsecop_path], check=True)
        else:
            print(f"Archivo {dashsecop_path} no encontrado.")
    else:
        # Eliminar DashSecop.py si existe
        if os.path.exists(dashsecop_path):
            os.remove(dashsecop_path)
            print(f"Archivo {dashsecop_path} eliminado.")
        else:
            print(f"Archivo {dashsecop_path} no existe.")
# -*- coding: utf-8 -*-

