import argparse
import re
from llm.call_openrouter import ask_llm
from experiment_targets import get_target


parser = argparse.ArgumentParser()
parser.add_argument("--target", default="generate_manifest_template")
args = parser.parse_args()
target = get_target(args.target)

with open(target.file, "r") as f:
    code = f.read()


#=====stage1=====
with open("prompts/stage1_knowledge.txt", "r") as f:
    stage1_prompt = f.read()

stage1_prompt = stage1_prompt.replace("{function_code}", code)

knowledge = ask_llm(stage1_prompt)

print("====STAGE1 KNOWLEDGE====")
print(knowledge)


#=====stage2=====
with open("prompts/stage2_scenarios.txt", "r") as f:
    stage2_prompt = f.read()

stage2_prompt = stage2_prompt.replace("{function_code}", code)
stage2_prompt = stage2_prompt.replace("{knowledge}", knowledge)

scenarios = ask_llm(stage2_prompt)

print("====STAGE2 SCENARIOS====")
print(scenarios)


#=====stage3=====
with open("prompts/stage3_generate_test.txt", "r") as f:
    stage3_prompt = f.read()

stage3_prompt = stage3_prompt.replace("{function_code}", code)
stage3_prompt = stage3_prompt.replace("{knowledge}", knowledge)
stage3_prompt = stage3_prompt.replace("{scenarios}", scenarios)
stage3_prompt = stage3_prompt.replace("{target_module}", target.module)
stage3_prompt = stage3_prompt.replace("{target_function}", target.function)

result = ask_llm(stage3_prompt)

match = re.search(
    r"```(?:python)?\s*(.*?)```",
    result,
    re.DOTALL
)
if match:
    generated_test = match.group(1).strip()
else:
    generated_test = result.strip()

target.pilot_directory.mkdir(parents=True, exist_ok=True)
output_path = target.pilot_directory / "guided.py"
with open(output_path, "w") as f:
    f.write(generated_test)

with open(target.pilot_directory / "guided_stage1_knowledge.txt", "w") as f:
    f.write(knowledge)

with open(target.pilot_directory / "guided_stage2_scenarios.txt", "w") as f:
    f.write(scenarios)

print("\n====STAGE3 GENERATED TEST====")
print(generated_test)
print(f"Generated: {output_path}")
