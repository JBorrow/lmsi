"""
The plot container!
"""

from pydantic import BaseModel
import json
import re


class PlotConfig(BaseModel):
    source: str
    title: str
    caption: str
    regex: bool = True

    def match(self, filename: str) -> bool:
        if self.regex:
            return bool(re.match(self.source, filename))
        else:
            return self.source == filename


class SectionConfig(BaseModel):
    name: str
    plots: list[PlotConfig]


class Config(BaseModel):
    list[SectionConfig]

    @classmethod
    def from_file(cls, filename: str):
        with open(filename, "r'") as handle:
            base = json.load(handle)

        return cls(
            [SectionConfig(name=key, plots=value) for key, value in base.items()]
        )


class Plot(BaseModel):
    filename: str
    title: str | None = None
    caption: str | None = None


class Section(BaseModel):
    name: str
    plots: list[Plot]


class PlotContainer(BaseModel):
    sections: list[Section]

    @classmethod
    def from_config(cls, config: Config, files: set[str]):
        sections = []
        matched_files = set()
        for section in config.sections:
            section = Section(name=section.name, plots=[])
            for plot in section.plots:
                for filename in files:
                    if plot.match(filename):
                        section.plots.append(
                            Plot(
                                filename=filename,
                                title=plot.title,
                                caption=plot.caption,
                            )
                        )
                        matched_files.add(filename)
            if len(section.plots) > 0:
                sections.append(section)

        # If there are leftover files, add them to the uncategorised section
        left_over_files = matched_files | files

        if len(left_over_files) > 0:
            sections.append(
                Section(
                    name="Uncategorised",
                    plots=[
                        Plot(
                            filename=filename,
                        )
                        for filename in left_over_files
                    ],
                )
            )
        
        return PlotContainer(sections=sections)
