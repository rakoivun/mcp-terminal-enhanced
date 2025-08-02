# New approach: Use Git Bash directly instead of shell=True with executable

# CURRENT (not working):
# process = await asyncio.create_subprocess_shell(
#     cmd, shell=True, executable="C:/Program Files/Git/bin/bash.exe")

# NEW APPROACH (should work):
# git_bash_cmd = ["C:/Program Files/Git/bin/bash.exe", "-c", cmd]
# process = await asyncio.create_subprocess_exec(*git_bash_cmd, ...)

print("Creating fixed version...")