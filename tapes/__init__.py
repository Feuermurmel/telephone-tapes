import argparse
import sys
import warnings
from pathlib import Path

from podgen.warnings import NotSupportedByItunesWarning

from tapes.feed import extract_podcasts
from tapes.util import log, UserError


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('--output-dir', '-o', type=Path, default=Path())

    return parser.parse_args()


def main(url, output_dir):
    warnings.simplefilter('ignore', NotSupportedByItunesWarning)
    warnings.simplefilter('ignore', UserWarning)

    for i, p in enumerate(extract_podcasts(url), 1):
        output_path = output_dir / f'{i:02}_{p.name.replace(" ", "_")}.xml'
        output_path.write_text(p.rss_str())

        log(f'Wrote {output_path}')


def entry_point():
    try:
        main(**vars(parse_args()))
    except KeyboardInterrupt:
        log('Operation interrupted.')
        sys.exit(1)
    except UserError as e:
        log(f'error: {e}')
        sys.exit(2)
