import json, torch
from torch.utils.data import DataLoader
from torch.nn.utils.rnn import pad_sequence



class Dataset(torch.utils.data.Dataset):
    def __init__(self, task, split):
        super().__init__()
        self.task = task
        self.data = self.load_data(split)

    def load_data(self, split):
        with open(f"data/{self.task}/{split}.json", 'r') as f:
            data = json.load(f)
        return data

    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        src = self.data[idx]['src']
        trg = self.data[idx]['trg']

        if self.task == 'sum' and len(src) > 512:
            src = src[:512]
            
        return src, trg



class Collator(object):
    def __init__(self, pad_id):
        self.pad_id = pad_id

    def __call__(self, batch):
        src_batch, trg_batch = zip(*batch)
        
        return {'src': self.pad_batch(src_batch), 
                'trg': self.pad_batch(trg_batch)}

    def pad_batch(self, batch):
        return pad_sequence(
            batch, 
            batch_first=True, 
            padding_value=self.pad_id
        )



def load_dataloader(config, split):

    return DataLoader(
        Dataset(config.task, split), 
        batch_size=config.batch_size, 
        shuffle=True if config.mode == 'train' else False,
        collate_fn=Collator(config.pad_id),
        num_workers=2
    )