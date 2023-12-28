from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from peft import PeftModel

device = "auto"
tokenizer = AutoTokenizer.from_pretrained("w8ay/secgpt", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    "w8ay/secgpt", trust_remote_code=True, device_map=device, torch_dtype=torch.float16
)
print("模型加载成功")


def reformat_sft(instruction, input):
    if input:
        prefix = (
            "Below is an instruction that describes a task, paired with an input that provides further context. "
            "Write a response that appropriately completes the request.\n"
            f"### Instruction:\n{instruction}\n\n### Input:\n{input}\n\n### Response:"
        )
    else:
        prefix = (
            "Below is an instruction that describes a task. "
            "Write a response that appropriately completes the request.\n"
            f"### Instruction:\n{instruction}\n\n### Response:"
        )
    return prefix


query = """介绍sqlmap如何使用"""
query = reformat_sft(query, "")

generation_kwargs = {
    "top_p": 0.7,
    "temperature": 0.3,
    "max_new_tokens": 2000,
    "do_sample": True,
    "repetition_penalty": 1.1,
}

inputs = tokenizer.encode(query, return_tensors="pt", truncation=True)
inputs = inputs.cuda()
generate = model.generate(input_ids=inputs, **generation_kwargs)
output = tokenizer.decode(generate[0])
print(output)
