import pathlib
import itertools

from cldfbench import Dataset as BaseDataset, CLDFSpec
from pycldf import term_uri


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "steinertthrelkeldmodals"

    def cldf_specs(self):  # A dataset must declare all CLDF sets it creates.
        return CLDFSpec(module="StructureDataset", dir=self.cldf_dir)

    def cmd_makecldf(self, args):
        args.writer.cldf.add_component("ParameterTable")
        args.writer.cldf.add_component("LanguageTable")
        # new, non-standard tables
        # NOTE: should the column names use `term_uri` and, if so, how?
        args.writer.cldf.add_table(
            "unit-parameters.csv",
            {
                "name": "ID",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#id",
            },
            "Name",
            "Description",
            "force",
            "flavor",
        )
        args.writer.cldf.add_table(
            "unit-values.csv",
            {
                "name": "ID",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#id",
            },
            {
                "name": "Value",
                # FIXME: valueReference should be added to the ontology, in analogy to formReference.
                #"propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#valueReference",
            },
            "UnitParameter_ID",
            "UnitValue",
            "Comment",
            "Source",
        )
        args.writer.cldf.add_table(
            "flavors.csv",
            {
                "name": "ID",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#id",
            },
            "Name", "Description"
        )
        args.writer.cldf.add_table(
            "forces.csv",
            {
                "name": "ID",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#id",
            },
            "Name", "Description"
        )
        args.writer.cldf.add_foreign_key(
            "unit-values.csv", "Value", "ValueTable", "ID"
        )
        args.writer.cldf.add_foreign_key(
            "unit-values.csv", "UnitParameter_ID", "unit-parameters.csv", "ID"
        )
        args.writer.cldf.add_foreign_key(
            "unit-parameters.csv", "flavor", "flavors.csv", "Name" 
        )
        args.writer.cldf.add_foreign_key(
            "unit-parameters.csv", "force", "forces.csv", "Name"
        )

        # link forces

        modal_id = 0
        args.writer.objects["ParameterTable"].append(dict(ID="modal"))

        force_flavor_pairs = set()

        for lid, rows in itertools.groupby(
            sorted(
                self.raw_dir.read_csv("data.csv", dicts=True, delimiter="\t"),
                key=lambda r: (r["l"], r["m"], r["can"]),
            ),
            lambda r: r["l"],
        ):
            args.writer.objects["LanguageTable"].append(dict(ID=lid))
            for modal, rrows in itertools.groupby(rows, lambda r: r["m"]):
                args.writer.objects["ValueTable"].append(
                    dict(
                        ID=str(modal_id),
                        Language_ID=lid,
                        Parameter_ID="modal",
                        Value=modal,
                    )
                )
                unit_obs_id = 0
                for can, rrrows in itertools.groupby(rrows, lambda r: r["can"]):
                    for row in rrrows:
                        unit_obs_id += 1
                        test_dict = dict(
                            ID=f"{modal_id}-{unit_obs_id}",
                            Parameter_ID="modal",
                            Value=str(modal_id),
                            UnitParameter_ID=f"{row['force']}.{row['flavor']}",
                            UnitValue="can" if can == "1" else "cannot",
                        )
                        force_flavor_pairs.add((row["force"], row["flavor"]))
                        args.writer.objects["unit-values.csv"].append(test_dict)
                modal_id += 1

        for idx, pair in enumerate(force_flavor_pairs):
            # TODO: refactor naming of pairs
            args.writer.objects["unit-parameters.csv"].append(
                dict(ID=f"{pair[0]}.{pair[1]}", Name=f"{pair[0]}.{pair[1]}", force=pair[0], flavor=pair[1])
            )

        forces = sorted(set(pair[0] for pair in force_flavor_pairs))
        for idx, force in enumerate(forces):
            args.writer.objects["forces.csv"].append(dict(ID=idx, Name=force))

        flavors = sorted(set(pair[1] for pair in force_flavor_pairs))
        for idx, flavor in enumerate(flavors):
            args.writer.objects["flavors.csv"].append(dict(ID=idx, Name=flavor))