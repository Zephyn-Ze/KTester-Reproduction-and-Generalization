import argparse
from llm.call_openrouter import ask_llm
import re
from experiment_targets import get_target


parser = argparse.ArgumentParser()
parser.add_argument("--target", default="generate_manifest_template")
parser.add_argument("--repetitions", type=int, default=5)
args = parser.parse_args()
target = get_target(args.target)

with open(target.file, "r") as f:
    code = f.read()


def clean_code(result):
    match = re.search(r"```(?:python)?\s*(.*?)```",
                      result,
                      re.DOTALL)
    if match:
        return match.group(1).strip()
    return result.strip()

#=====baseline repetitions=====
with open("prompts/baseline.txt", "r") as f:
    baseline_template = f.read()

baseline_directory = target.repetitions_directory / "baseline"
baseline_directory.mkdir(parents=True, exist_ok=True)

for i in range(1, args.repetitions + 1):
    print(f"\n=====BASELINE RUN {i}=====")
    prompt = baseline_template.replace("{function_code}", code)
    prompt = prompt.replace("{target_module}", target.module)
    prompt = prompt.replace("{target_function}", target.function)

    result = ask_llm(prompt)
    generated_code = clean_code(result)

    out_path = baseline_directory / f"run_{i}.py"
    with open(out_path, "w") as f:
        f.write(generated_code)
    print(f"saved to {out_path}")


#=====guided repetitions=====
with open("prompts/stage1_knowledge.txt", "r") as f:
    stage1_knowledge_template = f.read()
with open("prompts/stage2_scenarios.txt", "r") as f:
    stage2_scenarios_template = f.read()
with open("prompts/stage3_generate_test.txt", "r") as f:
    stage3_generate_test_template = f.read()

guided_directory = target.repetitions_directory / "guided"
guided_directory.mkdir(parents=True, exist_ok=True)

for i in range(1, args.repetitions + 1):
    print(f"\n=====GUIDED RUN {i}=====")
    stage1_prompt = stage1_knowledge_template.replace("{function_code}", code)
    knowledge = ask_llm(stage1_prompt)

    stage2_prompt = stage2_scenarios_template.replace("{function_code}", code)
    stage2_prompt = stage2_prompt.replace("{knowledge}", knowledge)

    scenarios = ask_llm(stage2_prompt)

    stage3_prompt = stage3_generate_test_template.replace("{function_code}", code)
    stage3_prompt = stage3_prompt.replace("{knowledge}", knowledge)
    stage3_prompt = stage3_prompt.replace("{scenarios}", scenarios)
    stage3_prompt = stage3_prompt.replace("{target_module}", target.module)
    stage3_prompt = stage3_prompt.replace("{target_function}", target.function)

    result = ask_llm(stage3_prompt)
    generated_code = clean_code(result)

    out_path = guided_directory / f"run_{i}.py"

    with open(out_path, "w") as f:
        f.write(generated_code)

    with open(guided_directory / f"run_{i}_stage1_knowledge.txt", "w") as f:
        f.write(knowledge)

    with open(guided_directory / f"run_{i}_stage2_scenarios.txt", "w") as f:
        f.write(scenarios)

    print(f"saved to {out_path}")
