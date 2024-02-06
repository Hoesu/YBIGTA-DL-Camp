import argparse
import logging
import os

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torch.optim import Adam
from torchvision import transforms as T
from tqdm import tqdm

from dataset import FoodDataset
from model import vanillaCNN, vanillaCNN2, VGG19

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', type=str, choices=['CNN1', 'CNN2', 'VGG'], required=True, help='model architecture to train')
    parser.add_argument('-e', '--epoch', type=int, default=50, help='the number of train epochs')
    parser.add_argument('-b', '--batch', type=int, default=32, help='batch size')
    parser.add_argument('-lr', '--learning_rate', type=float, default=1e-4, help='learning rate')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    
    os.makedirs('./save', exist_ok=True)
    os.makedirs(f'./save/{args.model}_{args.epoch}_{args.batch}_{args.learning_rate}', exist_ok=True)
    
    transforms = T.Compose([
        T.Resize((227,227), interpolation=T.InterpolationMode.BILINEAR),
        T.RandomVerticalFlip(0.5),
        T.RandomHorizontalFlip(0.5),
    ])

    train_dataset = FoodDataset("./data", "train", transforms=transforms)
    train_loader = DataLoader(train_dataset, batch_size=args.batch, shuffle=True)
    val_dataset = FoodDataset("./data", "val", transforms=transforms)
    val_loader = DataLoader(val_dataset, batch_size=args.batch, shuffle=True)

    if torch.cuda.is_available():
        device = torch.device('cuda')
    elif torch.backends.mps.is_available():
        device = torch.device('mps')
    else:
        device = torch.device('cpu')
    
    if args.model == 'CNN1':
        model = vanillaCNN()
    elif args.model == 'CNN2':
        model = vanillaCNN2()
    elif args.model == 'VGG': 
        model = VGG19()
    else:
        raise ValueError("model not supported")
    model.to(device)

    logging.basicConfig(filename=f'{args.model}.log',
                    filemode='w',
                    format='%(asctime)s %(levelname)s: %(message)s',
                    level=logging.INFO
                    )

    optimizer = torch.optim.Adam(params=model.parameters(), lr=args.learning_rate)
    criterion = torch.nn.CrossEntropyLoss()

    for epoch in range(args.epoch):
        
        model.train()
        step_index = 0
        train_loss = []

        for batch, tensor in enumerate(tqdm(train_loader)):
            images = tensor['input'].to(device)
            labels = tensor['target'].to(device)
            
            pred = model(images)
            loss = criterion(pred, labels)

            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

            train_loss.append(loss.item())
            logging.debug(f"Step {step_index} loss : {loss.item()}")

        logging.info(f"Epoch {epoch} loss : {sum(train_loss)/len(train_loss)}")

        model.eval()
        total = 0
        correct = 0
        val_score = 0

        with torch.no_grad():
            for batch, tensor in enumerate(tqdm(val_loader)):
                images = tensor['input'].to(device)
                labels = tensor['target'].to(device)
                total += len(images)

                outputs = model(images)
                _, pred = torch.max(outputs, axis=1)
                correct += (labels==pred).sum().item()
                val_score = correct/total

            logging.info(f"Epoch {epoch} accuracy : {val_score}")
        
        if not os.path.exists(f"./save/{args.model}_{args.epoch}_{args.batch}_{args.learning_rate}"):
            os.mkdir(f"./save/{args.model}_{args.epoch}_{args.batch}_{args.learning_rate}")

        torch.save(model.state_dict(),
                   f"./save/{args.model}_{args.epoch}_{args.batch}_{args.learning_rate}/{epoch}_score:{round(val_score,3)}.pth")