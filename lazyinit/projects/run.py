import lazydl as l
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from omegaconf import DictConfig
import hydra
from lazyinit.utils import run_cmd, echo
from projects.modules.loss_custom import HFLoss_custom
from projects.modules.zy_dataset import SFTDataset, SFTDataset_ChatGLM2, SFTDataCollator
from projects.modules.lit_model import LightningModel
import lightning as L
from torch.utils.data import DataLoader

log = l.Logger(__name__)
current_dir = os.path.dirname(os.path.abspath (__file__))


@hydra.main(version_base="1.2", config_path="configs/", config_name="default_config.yaml")
def main(config: DictConfig) -> float:
    l.hi()
    config, experiment = l.init_env(config, current_dir)
    
    
    # ---------------------------------------------------------------------------- #
    #                         加载模型                                     
    # ---------------------------------------------------------------------------- #
    model, tokenizer = l.load_model_and_tokenizer(config.model_name_or_path, use_qlora=True)
    
    
    # ---------------------------------------------------------------------------- #
    #                         加载数据集                                     
    # ---------------------------------------------------------------------------- #
    # if model.config.model_type == 'chatglm':
    #     train_dataset = SFTDataset_ChatGLM2(config.train_file, tokenizer, config.max_seq_length)
    # else:
    #     train_dataset = SFTDataset(config.train_file, tokenizer, config.max_seq_length)
        

    # ---------------------------------------------------------------------------- #
    #                            初始化Trainer                                  
    # ---------------------------------------------------------------------------- #
    # trainer = l.LoRATrainer_HF(
    #     model=model,
    #     args=hf_args,
    #     train_dataset=train_dataset,
    #     data_collator=l.SFTDataCollator(tokenizer, config.max_seq_length),
    #     compute_loss=loss_func
    # )
    trainer = L.Trainer(**config.lit_args)
    
    # ---------------------------------------------------------------------------- #
    #                         模型训练                                     
    # ---------------------------------------------------------------------------- #
    # train_result = trainer.train()
    trainer.fit(model=LightningModel(config, tokenizer, model=model), 
                train_dataloaders=l.load_data(config, tokenizer, stage="train"),
                val_dataloaders=l.load_data(config, tokenizer, stage="val"))
    
    # ---------------------------------------------------------------------------- #
    #                         结果保存                                     
    # ---------------------------------------------------------------------------- #
    # final_save_path = os.path.join(config.output_dir, 'final')
    # trainer.save_model(final_save_path)  # Saves the tokenizer too
    # metrics = train_result.metrics
    # trainer.log_metrics("train", metrics)
    # trainer.save_metrics("train", metrics)
    # trainer.save_state()

    # l.merge_lora_to_base_model(model_name_or_path, "", "results/")

    
    
    
if __name__ == "__main__":
    main()