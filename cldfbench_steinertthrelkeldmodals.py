import pathlib
import itertools

from cldfbench import Dataset as BaseDataset, CLDFSpec


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "steinertthrelkeldmodals"

    def cldf_specs(self):  # A dataset must declare all CLDF sets it creates.
        return CLDFSpec(module='StructureDataset', dir=self.cldf_dir)

    def cmd_makecldf(self, args):
        args.writer.cldf.add_component('ParameterTable')
        args.writer.cldf.add_component('LanguageTable')
        args.writer.cldf.add_columns(
            'ValueTable',
            {
                "name": "expressivity",
                "datatype": "json",
            }
        )
        vid = 0
        args.writer.objects['ParameterTable'].append(dict(ID='modal'))
        for lid, rows in itertools.groupby(
            sorted(
                self.raw_dir.read_csv('data.csv', dicts=True, delimiter='\t'),
                key=lambda r: (r['l'], r['m'], r['can'])),
            lambda r: r['l'],
        ):
            args.writer.objects['LanguageTable'].append(dict(ID=lid))
            for modal, rrows in itertools.groupby(rows, lambda r: r['m']):
                expr = {}
                for can, rrrows in itertools.groupby(rrows, lambda r: r['can']):
                    expr['can' if can == '1' else 'cannot'] = [[r['force'], r['flavor']] for r in rrrows]
                vid += 1
                args.writer.objects['ValueTable'].append(dict(
                    ID=str(vid),
                    Language_ID=lid,
                    Parameter_ID='modal',
                    Value=modal,
                    expressivity=expr,
                ))

