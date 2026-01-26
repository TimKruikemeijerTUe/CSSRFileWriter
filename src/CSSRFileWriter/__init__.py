#!/usr/bin/env python3
from pathlib import Path

import numpy as np
from ovito.io import FileWriterInterface
from ovito.pipeline import Pipeline
from traits.api import String


class CSSRFileWriter(FileWriterInterface):
    title = String("Titel", label="Title in the header")

    def _get_label_map(self, frame: int, pipeline: Pipeline) -> dict[int, str]:
        return {
            t.id: t.name for t in pipeline.compute(frame).particles.particle_types.types
        }

    def write(self, *, filename: str, frame: int, pipeline: Pipeline, **kwargs) -> None:
        label_map = self._get_label_map(frame, pipeline)

        with Path(filename).open("w", newline="\n") as file:
            data = pipeline.compute(frame)

            file.write(
                f"{' '.join([f'{t:.6g}' for t in np.diagonal(data.cell)])}\n",
            )
            file.write(
                "90 90 90 SPGR = 1 P 1 OPT = 1\n",  # TODO
            )
            file.write(f"{data.particles.count} 0 \n")
            file.write(f"0  {self.title} \n")

            file.writelines(
                f"{p_id} {label_map[p_type]} {xyz[0]:.6g} {xyz[1]:.6g} {xyz[2]:.6g} 0  0  0  0  0  0  0  0  0.00\n"  # TODO
                for (p_id, p_type, xyz) in zip(
                    data.particles.identifiers,
                    data.particles.particle_types,
                    data.particles.positions,
                    strict=True,
                )
            )
