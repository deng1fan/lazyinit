import lazydl as l
from lazyinit.utils import echo
import torch
import datetime


class config:
    # model_name_or_path = "THUDM/chatglm2-6b-32k"
    model_name_or_path = "lmsys/vicuna-7b-v1.5"
    model_alias = "AI 心理咨询师"
    prompt_module = "modules.prompt_templates.psy_prompt.Prompt"
    # 生成超参配置
    max_new_tokens = 1024  # 每轮对话最多生成多少个token
    history_max_len = 1000  # 模型记忆的最大token长度
    top_p = 0.9
    temperature = 0.35
    repetition_penalty = 1.0
    # 是否使用4bit进行推理，能够节省很多显存，但效果可能会有一定的下降
    load_in_4bit = False
    use_qlora = True
    
def get_time():
    return datetime.datetime.now().strftime("%m月%d日 %H:%M")




def main():
    
    model, tokenizer = l.load_model_and_tokenizer(config.model_name_or_path, use_qlora=config.use_qlora, load_in_4bit=config.load_in_4bit)
    model = model.eval()
    # model = l.load_class(config.lit_model_file)(config, tokenizer, model=model)
    prompt = l.load_class("modules.prompt_templates.psy_prompt.Prompt")

    history = []

    # 开始对话
    echo("\n\n")
    l.hi()
    echo("🌈🌈🌈 当前对话模型为：{}，权重来自：{}\n\n".format(config.model_alias, config.model_name_or_path), color="#ff9900")
    utterance_id = 0    # 记录当前是第几轮对话，为了契合chatglm的数据组织格式
    
    last_time = get_time()
    echo("                                                    " + last_time, color="#808080")
    echo("\n")
    
    user_input = input('User ：')
    echo("\n")
    
    while True:
        utterance_id += 1
        input_prompt = prompt.build_prompt(
                        id=1,
                        history=history, 
                        query=user_input)
        model_input_ids = tokenizer.encode(input_prompt, return_tensors="pt", add_special_tokens=True).to(model.device)

        with torch.no_grad():
            outputs = model.generate(
                input_ids=model_input_ids, max_new_tokens=config.max_new_tokens, do_sample=True, top_p=config.top_p,
                temperature=config.temperature, repetition_penalty=config.repetition_penalty, eos_token_id=tokenizer.eos_token_id
            )
        model_input_ids_len = model_input_ids.size(1)
        response_ids = outputs[:, model_input_ids_len:]
        response = tokenizer.batch_decode(response_ids)[0]
        history = history + ["用户：" + user_input, "答：" + response]
        
        echo(f"{config.model_alias} ：" + response.strip().replace(tokenizer.eos_token, ""), color="#cd853f")
        echo("\n")
        if last_time != get_time():
            last_time = get_time()
            echo("                                                    " + get_time(), color="#808080")
            echo("\n")
        user_input = input('User ：')
        echo("\n")


if __name__ == '__main__':
    main()

