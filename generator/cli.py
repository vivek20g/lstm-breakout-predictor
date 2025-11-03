"""Simple CLI wrapper for data generation."""
import argparse
from . import generate_dataset


def main():
    p = argparse.ArgumentParser(description='Generator CLI')
    p.add_argument('--excel', default='data/ExecutionData_Sample.xlsx', help='Input excel with price data')
    p.add_argument('--out', default='generator/output/simulated_trades.csv', help='Output CSV path')
    p.add_argument('--sheet', default=None, help='Excel sheet name/index')
    args = p.parse_args()

    path = generate_dataset(args.excel, args.out, args.sheet)
    print(f'Generated dataset at: {path}')


if __name__ == '__main__':
    main()
