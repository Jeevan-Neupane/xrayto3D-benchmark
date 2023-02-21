import wandb
import torch
from torch.utils.data.dataloader import DataLoader
from torch.optim import Adam
import pytorch_lightning as pl
from XrayTo3DShape import (
    get_dataset,
    get_nonkasten_transforms,
    get_kasten_transforms,
    VolumeAsInputExperiment,
    ParallelHeadsExperiment,
    SingleHeadExperiment,
    BaseExperiment,
    NiftiPredictionWriter,
    MetricsLogger,
    parse_training_arguments,
    get_model,
    get_model_config,
    get_loss
)
import XrayTo3DShape
from monai.utils.misc import set_determinism
from pytorch_lightning.loggers.wandb import WandbLogger
from pytorch_lightning import seed_everything
from pytorch_lightning.callbacks import ModelCheckpoint

if __name__ == "__main__":

    args = parse_training_arguments()
    SEED = 12345
    lr = args.lr
    NUM_EPOCHS = args.epochs
    IMG_SIZE = args.size
    ANATOMY = args.anatomy
    LOSS_NAME = args.loss
    IMG_RESOLUTION = args.res
    BATCH_SIZE = args.batch_size
    WANDB_PROJECT = args.wandb_project
    model_name = args.model_name
    experiment_name = args.experiment_name
    WANDB_EXPERIMENT_GROUP = args.model_name
    WANDB_TAGS = [WANDB_EXPERIMENT_GROUP,ANATOMY,LOSS_NAME,*args.tags]

    set_determinism(seed=SEED)
    seed_everything(seed=SEED)

    if experiment_name == ParallelHeadsExperiment.__name__ or experiment_name == SingleHeadExperiment.__name__:
        callable_transform = get_nonkasten_transforms
    elif experiment_name == VolumeAsInputExperiment.__name__:
        callable_transform = get_kasten_transforms
    else:
        raise ValueError(f'Invalid experiment name {experiment_name}')
    train_transforms = callable_transform(size=IMG_SIZE,resolution=IMG_RESOLUTION)

    
    train_loader = DataLoader(
        get_dataset(args.trainpaths, transforms=train_transforms),
        batch_size=BATCH_SIZE,
        num_workers=20,
        shuffle=True,
    )
    val_loader = DataLoader(
        get_dataset(args.valpaths, transforms=train_transforms),
        batch_size=BATCH_SIZE,
        num_workers=20,
        shuffle=False,
    )

    model = get_model(model_name=args.model_name,image_size=IMG_SIZE)
    MODEL_CONFIG = get_model_config(model_name,IMG_SIZE)
    # save hyperparameters
    HYPERPARAMS = {'IMG_SIZE':IMG_SIZE,'RESOLUTION':IMG_RESOLUTION,'BATCH_SIZE':BATCH_SIZE,'LR':lr,'SEED':SEED,'ANATOMY':ANATOMY,'MODEL_NAME':model_name,'LOSS':LOSS_NAME}
    HYPERPARAMS.update(MODEL_CONFIG)

    loss_function = get_loss(loss_name=LOSS_NAME,anatomy=ANATOMY,image_size=IMG_SIZE,lambda_bce=args.lambda_bce,lambda_dice=args.lambda_dice,device=f'cuda:{args.gpu}') 
    optimizer = Adam(model.parameters(), lr)
    # load pytorch lightning module
    experiment:BaseExperiment = getattr(XrayTo3DShape.experiments,experiment_name)(model,optimizer,loss_function,BATCH_SIZE)

    # batch = next(iter(train_loader))
    # input,output = experiment.get_input_output_from_batch(batch)
    # pred_logits = experiment.model(*input)
    # bs = pred_logits.shape[0]
    # print('pred shape',pred_logits.shape)
    # loss = experiment.loss_function(pred_logits,output)
    # # loss = experiment.loss_function(pred_logits.reshape(bs,-1),output.reshape(bs,-1))
    # print(loss)
    evaluation_callbacks = []
    if args.evaluate:
        if args.save_predictions:
            nifti_saver = NiftiPredictionWriter(output_dir=args.output_dir,write_interval='batch')
            evaluation_callbacks.append(nifti_saver)
        
        metric_saver = MetricsLogger(output_dir=args.output_dir,voxel_spacing=  IMG_RESOLUTION,nsd_tolerance=1)
        evaluation_callbacks.append(metric_saver)

        trainer = pl.Trainer(callbacks=evaluation_callbacks)
        trainer.predict(model=experiment,ckpt_path=args.checkpoint_path,dataloaders=val_loader,return_predictions=False)
        
    else:
        # loggers
        wandb_logger = WandbLogger(save_dir='runs/',project=WANDB_PROJECT,group=WANDB_EXPERIMENT_GROUP,tags=WANDB_TAGS)
        wandb_logger.watch(model,log_graph=False)
        wandb_logger.log_hyperparams(HYPERPARAMS)

        checkpoint_callback = ModelCheckpoint(monitor='val/loss',mode='min',save_last=True,save_top_k=5,filename='epoch={epoch}-step={step}-val_loss={val/loss:.2f}-val_acc={val/dice:.2f}',auto_insert_metric_name=False)
        trainer = pl.Trainer(accelerator=args.accelerator,precision=args.precision,max_epochs=NUM_EPOCHS,devices=[args.gpu],deterministic=False,log_every_n_steps=1,auto_select_gpus=True,logger=[wandb_logger],callbacks=[checkpoint_callback],enable_progress_bar=True,enable_checkpointing=True,max_steps=args.steps)

        trainer.fit(experiment,train_loader,val_loader)


        wandb.finish()