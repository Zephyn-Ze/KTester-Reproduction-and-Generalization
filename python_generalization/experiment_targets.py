from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TargetSpec:
    name: str
    file: Path
    module: str
    function: str

    @property
    def pilot_directory(self):
        return Path("generated_tests/pilots") / self.name

    @property
    def repetitions_directory(self):
        return Path("generated_tests/repetitions") / self.name


TARGETS = {
    "parse_bindings": TargetSpec(
        name="parse_bindings",
        file=Path("target_functions/parse_bindings_target.py"),
        module="target_functions.parse_bindings_target",
        function="parse_bindings",
    ),
    "is_main_conference": TargetSpec(
        name="is_main_conference",
        file=Path("target_functions/is_main_conference_target.py"),
        module="target_functions.is_main_conference_target",
        function="is_main_conference",
    ),
    "generate_manifest_template": TargetSpec(
        name="generate_manifest_template",
        file=Path("target_functions/generate_manifest_template_target.py"),
        module="target_functions.generate_manifest_template_target",
        function="generate_manifest_template",
    ),
    "parse_size": TargetSpec(
        name="parse_size",
        file=Path("target_functions/parse_size_target.py"),
        module="target_functions.parse_size_target",
        function="parse_size",
    ),
    "normalize_string_quotes": TargetSpec(
        name="normalize_string_quotes",
        file=Path("target_functions/normalize_string_quotes_target.py"),
        module="target_functions.normalize_string_quotes_target",
        function="normalize_string_quotes",
    ),
}


def get_target(name):
    try:
        return TARGETS[name]
    except KeyError as error:
        choices = ", ".join(sorted(TARGETS))
        raise ValueError(f"Unknown target {name!r}. Choose one of: {choices}") from error
