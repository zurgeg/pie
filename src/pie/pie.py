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

def get_contents(object_):
    for object_name in dir(object_):
        if not object_name.startswith("_"):
            yield getattr(object_, object_name)

platforms = []
crust_platforms = {}
crust_langs = {}

try:
    from . import crusts
    from . import clog
    from .clog import DEBUG, INFO, WARNING, ERROR
except ImportError:
    # we are in a developer env and not working as a package
    import crusts
    import clog
    from clog import DEBUG, INFO, WARNING, ERROR

logger = clog.Logger(
    message_format="[{level}]{module_info}{message}",
    module_info="pie"
)

logger.log("Loading crusts...", INFO)
for tld in get_contents(crusts):
    logger.log(f"Loading tld {'.'.join(tld.__name__.split('.')[2:])}", DEBUG)
    for domain in get_contents(tld):
        logger.log(f"Loading domain {'.'.join(domain.__name__.split('.')[2:])}", DEBUG)
        for crust_module in get_contents(domain):
            if type(crust_module) not in [str, list]:
                logger.log(f"Loading module {'.'.join(crust_module.__name__.split('.')[2:])}", INFO)
                for platform in crust_module.PIE_PROVIDES:
                    crust_platforms[platform] = crust_module.PIE_PROVIDES[platform]
                    crust_langs[platform] = crust_module.PIE_LANGUAGES[platform]
                    platforms.append(platform)
            else:
                logger.log(f"Invalid module (type is wrong, {type(crust_module)} {crust_module}", WARNING)

def create_group_for(platform):
    crust_platform = crust_platforms[platform]
    @click.group(name=platform)
    def platform_group():
        pass

    @platform_group.command()
    @click.argument("projectname")
    @click.option("--language", show_default=True, default=crust_langs[platform], help="Which language to use")
    @click.option("--projectfile", show_default=True, default=f"project.{crust_platform.PIE_PROJECT_EXTENSION}", help="Where to store project metadata")
    def new(projectname, language, projectfile):
        projectfile = os.path.join(projectname, projectfile)
        if os.path.exists(projectfile):
            click.echo(f"ERROR: There's already a project using the metadata file {projectfile}")
            click.echo("Please use the --projectfile argument, or work with the existing project")
            exit(1)
        click.echo("Creating a project using the following options:")
        click.echo(f"Platform: {platform.__name__}")
        project = crust_platform.Project(projectname, projectname, language=language)
        project.copy_skeleton()
        project.save_project(projectfile)

    @platform_group.command()
    @click.option("--projectfile", show_default=True, default=f"project.{crust_platform.PIE_PROJECT_EXTENSION}", help="Where the project metadata was stored")
    def compile(projectfile):
        project = crust_platform.load_project(projectfile)
        click.echo("Attempting to compile project...")
        project.compile()
        click.echo("Done")
    return platform_group

@click.group()
@click.option('--log-level',
              type=click.Choice(["debug", "info", 
              "warning", "error"], case_sensitive=False),
              show_choices=True,
              default="info"
              )
def cli(log_level):
    logger.set_level(log_level)


for platform in platforms:
    cli.add_command(create_group_for(platform))




if __name__ == '__main__':
    cli()