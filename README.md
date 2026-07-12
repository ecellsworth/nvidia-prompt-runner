# NVIDIA Prompt Runner - User Guide

A simple command-line tool to generate **text** and **images** using NVIDIA-hosted AI models.

---

## Requirments

- Python 3.10 or higher
- NVIDIA API keys for the models you want to use
- Sign up for free at https://build.nvidia.com/models?modal=signin
    - Generate APIs for:
        - [Link](https://build.nvidia.com/black-forest-labs/flux_2-klein-4b)
        - [Link](https://build.nvidia.com/deepseek-ai/deepseek-v4-pro)
        - [Link](https://build.nvidia.com/google/gemma-4-31b-it)
        - [Link](https://build.nvidia.com/z-ai/glm-5.2)

---

## Overview

This tool allows you to:
- Generate high-quality text responses (reasoning, coding, explanations, etc.)
- Generate images from text prompts
- Automatically save all outputs into organized folders

You interact with the tool by running a Python script and providing a prompt file + model name.

---

## Directory Structure

```
nvidia-project/
├── run_prompt.py                 # Main Python script
├── NVIDIA_Prompt_Runner_Guide.md # This documentation
├── text-prompt.md                # Example text prompt
├── image-prompt.md               # Example image prompt
├── generated_output/             # All generated content is saved here
│   ├── glm-5.2_20260712_xxxx.md
│   └── flux.2-klein-4b_20260712_xxxx.png
└── edit_output/                  # (Optional) Folder for images you may want to edit later
```

---

## Available Models

| Model                        | Type     | Use Case                                                                 | NVIDIA Build Link |
|-----------------------------|----------|--------------------------------------------------------------------------|-------------------|
| `paligemma`                 | Vision   | Image-to-Text, video, language generation, vision assistant, computer vision, visual question answering | [Link](https://build.nvidia.com/google/google-paligemma) |
| `flux.2-klein-4b`           | Image    | Image editing, Image Generation, Text-to-Image                           | [Link](https://build.nvidia.com/black-forest-labs/flux_2-klein-4b) |
| `deepseek-v4-pro`           | Text     | Reasoning, MoE, coding, agentic                                          | [Link](https://build.nvidia.com/deepseek-ai/deepseek-v4-pro) |
| `gemma-4-31b-it`            | Text     | Agentic, text-to-text, coding, reasoning                                 | [Link](https://build.nvidia.com/google/gemma-4-31b-it) |
| `glm-5.2`                   | Text     | Agentic AI, coding, reasoning, tool use                                  | [Link](https://build.nvidia.com/z-ai/glm-5.2) |

---

## How to Use

### Basic Command

```bash
python3 run_prompt.py <prompt-file> --model <model-name>
```

### Examples

**Generate Text**
```bash
python3 run_prompt.py text-prompt.md --model glm-5.2
```

**Generate an Image**
```bash
python3 run_prompt.py image-prompt.md --model flux.2-klein-4b
```

---

## Recommended Models by Task

| Task                              | Recommended Model          | Command                                           |
|-----------------------------------|----------------------------|---------------------------------------------------|
| General reasoning / explanations  | `glm-5.2`                  | `--model glm-5.2`                                 |
| Coding and technical tasks        | `deepseek-v4-pro`          | `--model deepseek-v4-pro`                         |
| Agentic workflows & tool use      | `glm-5.2`                  | `--model glm-5.2`                                 |
| Image Generation                  | `flux.2-klein-4b`          | `--model flux.2-klein-4b`                         |
| Image Editing                     | `flux.2-klein-4b`          | `--model flux.2-klein-4b --input-image <file>`    |

---

## Prompt Files

Create `.md` files containing your prompts. The entire content of the file is sent to the model.

**Example `text-prompt.md`:**
```markdown
Explain how a modern server rack works in simple terms.
```

**Example `image-prompt.md`:**
```markdown
A modern server rack in a clean data center, cinematic lighting, highly detailed
```

---

## Output

All generated content is automatically saved in the `generated_output/` folder:

- **Text responses** → Saved as `.md` files
- **Images** → Saved as `.png` files

Example output files:
- `glm-5.2_20260712_152439.md`
- `flux.2-klein-4b_20260712_152512.png`

---

## Important: Add Your API Keys

**Before using the script**, you must add your own NVIDIA API keys.

1. Open the file `run_prompt.py`
2. Replace the following placeholder values with your actual keys:

```python
"api_key": "YOUR_FLUX_API_KEY"
"api_key": "YOUR_GLM_API_KEY"
"api_key": "YOUR_DEEPSEEK_API_KEY"
"api_key": "YOUR_GEMMA_API_KEY"
```

You can generate your API keys at [NVIDIA Build](https://build.nvidia.com/models?modal=signin).

---

## Notes

- The script uses your individual NVIDIA API keys for each model.
- Only `flux.2-klein-4b` is currently configured for reliable image generation.
- All output is saved automatically to the `generated_output/` folder.
- Image editing is currently **not supported** in this version of the script.

---

## Full Command Reference

| Action                    | Command                                                      |
|---------------------------|--------------------------------------------------------------|
| Generate text             | `python3 run_prompt.py text-prompt.md --model glm-5.2`       |
| Generate image            | `python3 run_prompt.py image-prompt.md --model flux.2-klein-4b` |
| Check available models    | See the `MODELS` dictionary inside `run_prompt.py`           |

---

## License

This project is open source. Feel free to use and modify it.
