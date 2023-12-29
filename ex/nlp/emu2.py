from PIL import Image
import requests
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


tokenizer = AutoTokenizer.from_pretrained("BAAI/Emu2")

model = (
    AutoModelForCausalLM.from_pretrained(
        "BAAI/Emu2",
        torch_dtype=torch.bfloat16,
        low_cpu_mem_usage=True,
        trust_remote_code=True,
    )
    .to("cuda")
    .eval()
)


# `[<IMG_PLH>]` is the image placeholder which will be replaced by image embeddings.
# the number of `[<IMG_PLH>]` should be equal to the number of input images

query = "[<IMG_PLH>]Describe the image in details:"
image = Image.open(
    requests.get(
        "https://github.com/baaivision/Emu/Emu2/examples/blue_black_1_top_left.jpg?raw=true",
        stream=True,
    ).raw
).convert("RGB")


inputs = model.build_input_ids(text=[query], tokenizer=tokenizer, image=[image])

with torch.no_grad():
    outputs = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        image=inputs["image"].to(torch.bfloat16),
        max_new_tokens=64,
        length_penalty=-1,
    )

output_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)
