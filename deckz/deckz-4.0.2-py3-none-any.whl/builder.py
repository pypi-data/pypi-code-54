from enum import Enum
from filecmp import cmp
from logging import getLogger
from multiprocessing import Pool
from os import unlink
from os.path import join as path_join
from pathlib import Path
from shutil import copyfile, move
from subprocess import CompletedProcess, run
from tempfile import NamedTemporaryFile
from typing import Any, Dict, Optional

from jinja2 import Environment, FileSystemLoader

from deckz.exceptions import DeckzException
from deckz.paths import Paths
from deckz.targets import Target, Targets


class CompileType(Enum):
    Handout = "handout"
    Presentation = "presentation"
    Print = "print"
    PrintHandout = "print-handout"


class Builder:
    def __init__(
        self,
        config: Dict[str, Any],
        paths: Paths,
        targets: Targets,
        build_presentation: bool,
        build_handout: bool,
        build_print: bool,
    ):
        self._config = config
        self._paths = paths
        self._targets = targets
        self._presentation = build_presentation
        self._handout = build_handout
        self._print = build_print
        self._logger = getLogger(__name__)
        self._build_all()

    def _build_all(self) -> None:
        to_compile = []
        for target in self._targets:
            if self._presentation:
                to_compile.append((target, CompileType.Presentation, True))
            if self._handout:
                to_compile.append((target, CompileType.Handout, True))
            if self._print:
                to_compile.append((target, CompileType.PrintHandout, False))
        to_compile.sort(key=lambda x: (x[0].name, x[1].value))
        n_outputs = (int(self._handout) + int(self._presentation)) * len(
            self._targets
        ) + int(self._print)
        self._logger.info(
            f"Building {len(to_compile)} PDFs used in {n_outputs} outputs"
        )
        with Pool() as pool:
            completed_processes = pool.starmap(self._build, to_compile)
        print_handout_ok = (
            sum(
                c.returncode
                for c, (_, t, _) in zip(completed_processes, to_compile)
                if t is CompileType.PrintHandout
            )
            == 0
        )
        if self._print:
            if print_handout_ok:
                self._logger.info(
                    f"Formatting {len(self._targets)} PDFs into a printable output"
                )
                completed_processes.append(self._build(None, CompileType.Print, True))
            else:
                self._logger.warning(
                    "Preparatory compilations failed. Skipping print output"
                )
        for completed_process, (target, compile_type, _) in zip(
            completed_processes, to_compile
        ):
            if target is not None:
                compilation = f"{target.name}/{compile_type.value}"
            else:
                compilation = compile_type.value
            if completed_process.returncode != 0:
                self._logger.warning("Compilation %s errored", compilation)
                self._logger.warning(
                    "Captured %s stderr\n%s", compilation, completed_process.stderr
                )
                self._logger.warning(
                    "Captured %s stdout\n%s", compilation, completed_process.stdout
                )

    def _get_filename(self, target: Optional[Target], compile_type: CompileType) -> str:
        name = self._config["deck_acronym"]
        if target is not None:
            name += f"-{target.name}"
        name += f"-{compile_type.value}"
        return name.lower()

    def _build(
        self,
        target: Optional[Target],
        compile_type: CompileType,
        copy_result: bool = True,
    ) -> CompletedProcess:
        build_dir = self._setup_build_dir(target, compile_type)
        filename = self._get_filename(target, compile_type)
        latex_path = build_dir / f"{filename}.tex"
        build_pdf_path = latex_path.with_suffix(".pdf")
        output_pdf_path = self._paths.pdf_dir / f"{filename}.pdf"
        if compile_type is CompileType.Print:
            self._write_print_latex(self._targets, latex_path)
        else:
            self._write_main_latex(target, compile_type, latex_path)
            self._link_dependencies(target, build_dir)

        completed_process = self._compile(
            latex_path=latex_path.relative_to(build_dir), build_dir=build_dir,
        )
        if copy_result and completed_process.returncode == 0:
            self._paths.pdf_dir.mkdir(parents=True, exist_ok=True)
            copyfile(build_pdf_path, output_pdf_path)
        return completed_process

    def _setup_build_dir(
        self, target: Optional[Target], compile_type: CompileType
    ) -> Path:
        target_build_dir = self._paths.build_dir
        if target is not None:
            target_build_dir /= target.name
        target_build_dir /= compile_type.value
        target_build_dir.mkdir(parents=True, exist_ok=True)
        for item in self._paths.shared_dir.iterdir():
            self._setup_link(target_build_dir / item.name, item)
        return target_build_dir

    def _write_main_latex(
        self, target: Target, compile_type: CompileType, output_path: Path
    ) -> None:
        self._write_latex(
            template_path=self._paths.jinja2_main_template,
            output_path=output_path,
            config=self._config,
            target=target,
            handout=compile_type in [CompileType.Handout, CompileType.PrintHandout],
            print=compile_type is CompileType.PrintHandout,
        )

    def _write_print_latex(self, targets: Targets, output_path: Path) -> None:
        self._write_latex(
            template_path=self._paths.jinja2_print_template,
            output_path=output_path,
            pdf_paths=[
                "../%s/%s/%s"
                % (
                    target.name,
                    CompileType.PrintHandout.value,
                    self._get_filename(target, CompileType.PrintHandout),
                )
                for target in targets
            ],
            format="1x2",
        )

    def _write_latex(
        self, *, template_path: Path, output_path: Path, **template_kwargs: Any
    ) -> None:
        template = self._env.get_template(str(template_path.name))
        try:
            with NamedTemporaryFile("w", encoding="utf8", delete=False) as fh:
                fh.write(template.render(**template_kwargs))
                fh.write("\n")
            if not output_path.exists() or not cmp(fh.name, str(output_path)):
                move(fh.name, output_path)
        finally:
            try:
                unlink(fh.name)
            except FileNotFoundError:
                pass

    @property
    def _env(self) -> Environment:
        if not hasattr(self, "__env"):
            self.__env = Environment(
                loader=FileSystemLoader(searchpath=self._paths.jinja2_dir),
                block_start_string=r"\BLOCK{",
                block_end_string="}",
                variable_start_string=r"\VAR{",
                variable_end_string="}",
                comment_start_string=r"\#{",
                comment_end_string="}",
                line_statement_prefix="%%",
                line_comment_prefix="%#",
                trim_blocks=True,
                autoescape=False,
            )
            self.__env.filters["camelcase"] = self._to_camel_case
            self.__env.filters["path_join"] = lambda paths: path_join(*paths)
        return self.__env

    def _link_dependencies(self, target: Target, target_build_dir: Path) -> None:
        for dependency in target.dependencies.used:
            try:
                link_dir = (
                    target_build_dir
                    / dependency.relative_to(self._paths.shared_latex_dir).parent
                )
            except ValueError:
                link_dir = (
                    target_build_dir
                    / dependency.relative_to(
                        self._paths.working_dir / target.name
                    ).parent
                )
            link_dir.mkdir(parents=True, exist_ok=True)
            self._setup_link(link_dir / dependency.name, dependency)

    def _compile(self, latex_path: Path, build_dir: Path) -> CompletedProcess:
        command = [
            "latexmk",
            "-pdflatex=xelatex -shell-escape -interaction=nonstopmode %O %S",
            "-dvi-",
            "-ps-",
            "-pdf",
        ]
        command.append(str(latex_path))
        return run(command, cwd=build_dir, capture_output=True, encoding="utf8")

    def _setup_link(self, source: Path, target: Path) -> None:
        if not target.exists():
            raise DeckzException(
                f"{target} could not be found. Please make sure it exists before "
                "proceeding."
            )
        target = target.resolve()
        if source.is_symlink():
            if source.resolve().samefile(target):
                return
            raise DeckzException(
                f"{source} already exists in the build directory and does not point to "
                f"{target}. Please clean the build directory."
            )
        elif source.exists():
            raise DeckzException(
                f"{source} already exists in the build directory. Please clean the "
                "build directory."
            )
        source.parent.mkdir(parents=True, exist_ok=True)
        source.symlink_to(target)

    def _to_camel_case(self, string: str) -> str:
        return "".join(substring.capitalize() or "_" for substring in string.split("_"))
