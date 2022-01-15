"""
Checks the IFF condition for the modals in the dataset
"""
import itertools

from cldfbench_steinertthrelkeldmodals import Dataset


def run(args):
    ds = Dataset().cldf_reader()
    for modal in ds['ValueTable']:
        can = set((fo, fl) for fo, fl in modal['expressivity']['can'])
        cannot = set((fo, fl) for fo, fl in modal['expressivity']['cannot'])

        for fo, fl in itertools.product([e[0] for e in can], [e[1] for e in can]):
            assert (fo, fl) in can and ((fo, fl) not in cannot)
 
