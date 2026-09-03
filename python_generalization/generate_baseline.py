import argparse
import re
from llm.call_openrouter import ask_llm
from experiment_targets import get_target


parser = argparse.ArgumentParser()
parser.add_argument("--target", default="generate_manifest_template")
args = parser.parse_args()
target = get_target(args.target)

with open(
    target.file,
    "r"
) as f:
    code = f.read()


with open(
    "prompts/baseline.txt",
    "r"
) as f:
    prompt = f.read()


prompt = prompt.replace(
    "{function_code}",
    code
)
prompt = prompt.replace("{target_module}", target.module)
prompt = prompt.replace("{target_function}", target.function)

print("====PROMPT====")
print(prompt)

result = ask_llm(prompt)

print("\n====RESPONSE====")
print(result)

match = re.search(
    r"```(?:python)?\s*(.*?)```",
    result,
    re.DOTALL
)
if match:
    generated_code = match.group(1).strip()
else:
    generated_code = result.strip()

target.pilot_directory.mkdir(parents=True, exist_ok=True)
output_path = target.pilot_directory / "baseline.py"
with open(output_path, "w") as f:
    f.write(generated_code)


print(f"Generated: {output_path}")
