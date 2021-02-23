import argparse

from environment.display import GridRender


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', required=True,
                        help='Input File Path')
    parser.add_argument('--moves-file', required=True,
                        help='Moves File Path containing predicted moves for this input')
    args = parser.parse_args()

    GridRender.load(args.input_file, args.moves_file)
