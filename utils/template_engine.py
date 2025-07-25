import os

def load_templates():
    templates = {}
    template_dir = "templates"
    for filename in os.listdir(template_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(template_dir, filename), "r") as f:
                templates[filename] = f.read()
    return templates

def fill_template(template_content, data, service_to_sell):
    # This is a basic fill_template. It can be expanded based on specific template needs.
    # For now, it replaces placeholders like {channel_name}, {latest_video_title}, {service}
    filled_template = template_content
    for key, value in data.items():
        filled_template = filled_template.replace(f"{{{key}}}", str(value))
    filled_template = filled_template.replace("{service}", service_to_sell)
    return filled_template