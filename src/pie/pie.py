#!/bin/env python3
"""
This program is free software: you can redistribute it and/or modify it 
under the terms of the GNU Lesser General Public License as published 
by the Free Software Foundation, either version 3 of the License, or 
(at your option) any later version.

This program is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
See the GNU Lesser General Public License for more details.

You should have received a copy of the Lesser GNU General Public License along with this program. 
If not, see <https://www.gnu.org/licenses/>.
""" 
import click
import os.path
# hardcoded piecrusts
import notdate.play.playdate_pie


@click.group()
def cli():
    pass

@cli.group()
def playdate():
    pass

@playdate.command()
@click.argument("projectname")
@click.option("--language", show_default=True, default="lua", help="Which language to use")
@click.option("--projectfile", show_default=True, default="project.pdproject", help="Where to store project metadata")
def new(projectname, language, projectfile):
    projectfile = os.path.join(projectname, projectfile)
    if os.path.exists(projectfile):
        click.echo(f"ERROR: There's already a project using the metadata file {projectfile}")
        click.echo("Please use the --projectfile argument, or work with the existing project")
        exit(1)
    click.echo("Creating a project using the following options (hardcoded for playdate):")
    click.echo("Platform: notdate.play.playdate_pie.playdate (hardcoded)")
    project = notdate.play.playdate_pie.playdate.Project(projectname, projectname, language=language)
    project.copy_skeleton()
    project.save_project(projectfile)

@playdate.command()
@click.option("--projectfile", show_default=True, default="project.pdproject", help="Where the project metadata was stored")
def compile(projectfile):
    project = notdate.play.playdate_pie.playdate.Project.load_project(projectfile)
    click.echo("Attempting to compile project...")
    project.compile()
    click.echo("Done")


if __name__ == '__main__':
    cli()