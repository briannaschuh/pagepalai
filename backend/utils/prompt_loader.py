from jinja2 import Environment, FileSystemLoader

PROMPT_DIR = "backend/prompt_templates"  

def load_prompt_template(prompt_name: str = "explanation", version: str = "v1"):
    env = Environment(loader=FileSystemLoader(PROMPT_DIR))
    return env.get_template(f"{prompt_name}_{version}.j2")
