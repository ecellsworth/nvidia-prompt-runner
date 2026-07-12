from openai import OpenAI
import requests
from datetime import datetime
from pathlib import Path
import argparse
import sys
import base64

# ====================== MODEL CONFIG ======================
MODELS = {
    # Image Generation
    "flux.2-klein-4b": {
        "type": "image",
        "model": "black-forest-labs/flux.2-klein-4b",
        "api_key": "YOUR_FLUX_API_KEY",
        "endpoint": "https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.2-klein-4b"
    },

    # Text Models
    "glm-5.2": {
        "type": "text",
        "model": "z-ai/glm-5.2",
        "api_key": "YOUR_GLM_API_KEY"
    },
    "deepseek-v4-pro": {
        "type": "text",
        "model": "deepseek-ai/deepseek-v4-pro",
        "api_key": "YOUR_DEEPSEEK_API_KEY"
    },
    "gemma-4-31b-it": {
        "type": "text",
        "model": "google/gemma-4-31b-it",
        "api_key": "YOUR_GEMMA_API_KEY"
    },

}

DEFAULT_TEXT_MODEL = "glm-5.2"
OUTPUT_DIR = Path("generated_output")
OUTPUT_DIR.mkdir(exist_ok=True)
# ========================================================


def get_client(model_key: str) -> OpenAI:
    config = MODELS[model_key]
    return OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=config["api_key"]
    )


def generate_text(prompt: str, model_key: str) -> str:
    config = MODELS[model_key]
    client = get_client(model_key)
    response = client.chat.completions.create(
        model=config["model"],
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4000,
        temperature=0.7
    )
    return response.choices[0].message.content


def generate_image(prompt: str, model_key: str) -> str:
    config = MODELS[model_key]
    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "prompt": prompt,
        "width": 1024,
        "height": 1024,
        "seed": 0,
        "steps": 4
    }
    response = requests.post(config["endpoint"], headers=headers, json=payload)
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        sys.exit(1)
    result = response.json()
    image_data = result.get("image") or result.get("b64_json")
    if not image_data and "artifacts" in result:
        image_data = result["artifacts"][0].get("base64")
    if not image_data:
        print("Error: Could not extract image data")
        sys.exit(1)
    img_data = base64.b64decode(image_data)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = OUTPUT_DIR / f"{model_key}_{timestamp}.png"
    with open(filename, "wb") as f:
        f.write(img_data)
    return str(filename)


def save_text_output(content: str, model_key: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = OUTPUT_DIR / f"{model_key}_{timestamp}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return str(filename)


def main():
    parser = argparse.ArgumentParser(description="Generate text or images using NVIDIA models.")
    parser.add_argument("prompt_file")
    parser.add_argument("--model", required=True, help="Model to use")
    args = parser.parse_args()

    prompt_path = Path(args.prompt_file)
    if not prompt_path.exists():
        print(f"Error: File '{prompt_path}' not found.")
        sys.exit(1)

    prompt = prompt_path.read_text(encoding="utf-8").strip()
    if not prompt:
        print("Error: Prompt file is empty.")
        sys.exit(1)

    model_key = args.model
    if model_key not in MODELS:
        print(f"Error: Unknown model '{model_key}'")
        print("Available models:", ", ".join(MODELS.keys()))
        sys.exit(1)

    model_type = MODELS[model_key]["type"]

    if model_type.startswith("image"):
        print(f"🖼️  Generating image using model: {model_key}")
        saved_path = generate_image(prompt, model_key)
        print(f"✅ Image saved to: {saved_path}")
    else:
        print(f"✍️  Generating text using model: {model_key}")
        result = generate_text(prompt, model_key)
        saved_path = save_text_output(result, model_key)
        print(f"✅ Response saved to: {saved_path}")
        print("\n" + "=" * 60)
        print(result)
        print("=" * 60)


if __name__ == "__main__":
    main()