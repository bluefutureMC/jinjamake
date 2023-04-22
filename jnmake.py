import os
import sys
from optparse import OptionParser
import json


def collect_files_by_extension(file_extension, root_path):
    last_working_dir = os.getcwd()
    try:
        os.chdir(root_path)
        src_dir_contents = os.listdir('.')
        collected_files = [os.path.abspath(f) for f in src_dir_contents if os.path.isfile(f) and f.endswith(file_extension)] \
                        + sum([collect_files_by_extension(file_extension, subdir) for subdir in src_dir_contents if os.path.isdir(subdir)], start=[])

        return collected_files
    finally:
        os.chdir(last_working_dir)


def render(data, src_path, out_path, temp_ext):
    from jinja2 import (
        Environment,
        FileSystemLoader,
    )

    env = Environment(
        loader=FileSystemLoader(src_path),
        keep_trailing_newline=True,
    )
    
    def raise_msg(msg):
        raise Exception(msg)

    env.globals['raise'] = raise_msg

    # Add environ global
    env.globals["get_context"] = lambda: data

    for template in collect_files_by_extension(temp_ext, src_path):
        relative_template_path = os.path.relpath(template, start=src_path)
        rendered_content = env.get_template(relative_template_path).render(data)
        relative_out_path = os.path.join(out_path, relative_template_path[:-len(temp_ext)])

        os.makedirs(os.path.dirname(relative_out_path), exist_ok=True)

        with open(relative_out_path, "w") as rendered_file:
            rendered_file.write(rendered_content)
            rendered_file.flush()
            rendered_file.close()


def cli(opts, args):
    input_file, = args
    input_file_path = os.path.join(os.getcwd(), os.path.expanduser(input_file))

    with open(input_file_path, "r") as input_file_object:
        data = json.load(input_file_object)
        render(data, src_path=opts.src_path, out_path=opts.out_path, temp_ext=opts.temp_ext)
        input_file_object.close()


def main():
    parser = OptionParser(
        usage="usage: %prog [options] <datapack globals>"
    )
    parser.add_option(
        "-s",
        "--src",
        help="Path to .j2 source files.",
        dest="src_path",
        metavar="PATH",
        action="store",
        default="src"
    )
    parser.add_option(
        "-o",
        "--out",
        help="Path to output rendered files to.",
        dest="out_path",
        metavar="PATH",
        action="store",
        default="out"
    )
    parser.add_option(
        "-e",
        "--extension",
        help="The file extension of the template files.",
        dest="temp_ext",
        metavar=".EXTENSION",
        action="store",
        default=".j2"
    )
    opts, args = parser.parse_args()

    if len(args) < 1:
        parser.print_help()
        sys.exit(1)

    sys.exit(cli(opts, args))


if __name__ == "__main__":
    main()