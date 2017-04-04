import re
import subprocess
import shlex
import os

def development_envs():
    root_path = os.path.abspath(os.path.dirname(__file__))
    output_file = "/tmp/app.development.cfg.txt"

    subprocess.call(shlex.split('sh {root_path}/private/setup/common/security/local/decrypt.sh {root_path}/envs/app.development.cfg 2>&1 >/dev/null'.format(root_path=root_path)))

    try:
        with open(output_file) as f:
            content = f.read()

        for line in content.splitlines():
            ignored = re.match(r"(^\#)|(\n\s*\n)", line)
            if ignored:
                continue

            variable = re.match(r"\s*(.*)\s*=\s*(.*)\s*", line)
            if variable:
                os.environ.setdefault(variable.group(1).replace("\"","").replace("\'", "").strip(),
                                      variable.group(2).replace("\"","").replace("\'", "").strip())
    finally:
        os.remove(output_file)