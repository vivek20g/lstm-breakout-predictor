"""main.py — top-level orchestrator that composes simulator and trainer packages."""

import argparse
import pandas as pd
from simulator import generate_dataset
from trainer import Trainer
from features.engineer import FeatureEngineer

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--generate', action='store_true')
    p.add_argument('--train', action='store_true')
    p.add_argument('--excel', default='simulator/data/NiftyPrice.xlsx')
    p.add_argument('--sheet', default='HDFCBANK')
    p.add_argument('--out', default='simulator/output/simulated_trades.csv')
    args = p.parse_args()

    data_path = args.out

    if args.generate:
        print('Generating simulated dataset...')
        generate_dataset(args.excel, data_path, args.sheet)

    if args.train:
        print('Loading dataset for training...')
        df = pd.read_csv(data_path)
        df = df.sort_values(by='ExecutionDate')

        #fe = __import__('features.engineer', fromlist=['FeatureEngineer']).FeatureEngineer()
        fe = FeatureEngineer()
        df = fe.run(df)

        price_features = ['Entry_vs_PrevClose', 'EntryPriceChange', 'volatility']
        indicator_features = ['EMA_10', 'EMA_20', 'MA50', 'BB_Width', 'RSI', 'Momentum', 'ATR']
        time_features = ['HourOfDay', 'OrderMonth', 'GoldenCrossover']

        sequence_length = 9
        trainer = Trainer(sequence_length=sequence_length)

        Xp, Xi, Xt, y = trainer.preprocess(df, price_features, indicator_features, time_features)

        trainer.build_model(price_dim=len(price_features), indicator_dim=len(indicator_features), time_dim=len(time_features))
        trainer.compile()

        trainer.fit(Xp, Xi, Xt, y)

        val_size = int(len(y) * 0.3)
        trainer.evaluate(Xp[-val_size:], Xi[-val_size:], Xt[-val_size:], y[-val_size:])

        trainer.save()

if __name__ == '__main__':
    main()


