import os
import pprint

import click

import xmltodict
import xml.etree.ElementTree as ET

"""
    Uncompressed .tar.gz course is a flat representation of nested course
    structure, therefore each element type (chapter, sequential, vertical)
    is stored in a folder of its name on the filesystem, and and can be
    identified by its url_name. Ex. sequential/12ef45.xml, this file contains
    url_names of its children elements which will be store in their element
    type name folder.
"""


CLOUDFRONT_URL = "https://d381hmu4snvm3e.cloudfront.net/videos/{video_id}/HD.mp4"


def read_course_structure(path, convert_video):

    def read_xmlfile(folder, url_name, getroot=True):
        """
        Read xml file, returns
        """
        base_path = os.getcwd()
        result = ET.parse(os.path.join(
            base_path, path, folder, url_name + ".xml"))
        if getroot:
            result = result.getroot()
        return result

    def prettyprint(data):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(data)

    def replace_video_xblock(url_name):
        """
        Regenerate a vertical to change its video xblock
        """
        print("            Libcast video xblock for video ID: {url}".format(
            url=CLOUDFRONT_URL.format(video_id=xblock["@video_id"])))

    def process_verticals(verticals_to_process, convert_video):
        """
        Rewrite vertical xml file containing xblock we aim.
        """

        for url_name in verticals_to_process:
            vertical = read_xmlfile("vertical", url_name, getroot=True)
            for idx, xblock in enumerate(vertical):
                if xblock.tag == "libcast_xblock" and convert_video:
                    if convert_video == "youtube":
                        import ipdb; ipdb.set_trace()
                        video = ET.Element("video")
                        video.attrib = {"display_name": vertical.attrib["display_name"]}
                        del vertical[idx]
                        vertical.insert(idx, video)
                        print(ET.tostring(vertical))

    root = read_xmlfile("", "course")
    print("Course key: {url_name}/{org}/{course}".format(
        url_name=root.attrib["url_name"],
        org=root.attrib["org"],
        course=root.attrib["course"]))

    verticals_to_process = []

    # This node (chapters) contains "Advanced settings", course chapters and wiki url key
    chapters = read_xmlfile("course", root.attrib["url_name"])
    print("Course name: {display_name}".format(display_name=chapters.attrib["display_name"]))

    for chapter_url in chapters:
        if "url_name" in chapter_url.attrib:  # wiki is a chapter with no url
            chapter = read_xmlfile("chapter", chapter_url.attrib["url_name"])
            print("{p}Chapter name: {display_name}".format(
                display_name=chapter.attrib["display_name"], p=" " * 4))
            for sequential_url in chapter:
                sequential = read_xmlfile("sequential", sequential_url.attrib["url_name"])
                print("{p}Sequential name: {display_name}".format(display_name=sequential.attrib["display_name"], p=" " * 8))

                for vertical_url in sequential:
                    vertical = read_xmlfile("vertical", vertical_url.attrib["url_name"])
                    print("{p}Vertical name: {display_name}".format(display_name=vertical.attrib["display_name"], p=" " * 12))

                    for xblock in vertical:
                        if xblock.tag == "libcast_xblock":
                            verticals_to_process.append(
                                vertical_url.attrib["url_name"])
                        if xblock.tag == "video":
                            print("Suspect video xblock")

    process_verticals(verticals_to_process, convert_video)


@click.command()
@click.option("--path", type=click.Path(exists=True, file_okay=False, dir_okay=True,
    writable=True, readable=True))
@click.option("--convert-video", type=click.Choice(choices=["youtube", "marsha"]))
def cli(path, convert_video):
    read_course_structure(path, convert_video)


if __name__ == '__main__':
    cli()
