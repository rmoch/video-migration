import os
import pprint

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


PATH = "selection/CNAM...01002S03...session03"

CLOUDFRONT_URL = "https://d381hmu4snvm3e.cloudfront.net/videos/{video_id}/HD.mp4"


def read_xmlfile(folder, url_name):
    """
    """
    base_path = os.getcwd()
    return ET.parse(os.path.join(base_path, PATH, folder, url_name + ".xml")).getroot()


def prettyprint(data):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(data)


def replace_video_xblock(url_name):
    """
    Regenerate a vertical to change its video xblock
    """
    print("            Libcast video xblock for video ID: {url}".format(
        url=CLOUDFRONT_URL.format(video_id=xblock["@video_id"])))

#replace_video_xblock(url_name=vertical_url["@url_name"])



def process_verticals(verticals_to_process):
    """
    Rewrite vertical xml file containin xblock we aim.
    """

    #for url_name in verticals_to_process:
    #    vertical = read_xmlfile("vertical", url_name)
#
    #    #import ipdb; ipdb.set_trace()
    #    #for xblock_name in filter_children(vertical):
#
    #    new_vertical = xmltodict.unparse(vertical, full_document=False, short_empty_elements=True)


def read_course_structure():

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
            print("    Chapter name: {display_name}".format(display_name=chapter.attrib["display_name"]))
            for sequential_url in chapter:
                sequential = read_xmlfile("sequential", sequential_url.attrib["url_name"])
                print("        Sequential name: {display_name}".format(display_name=sequential.attrib["display_name"]))

                for vertical_url in sequential:
                    vertical = read_xmlfile("vertical", vertical_url.attrib["url_name"])
                    print("            Vertical name: {display_name}".format(display_name=vertical.attrib["display_name"]))

                    for xblock in vertical:
                        if xblock.tag == "libcast_xblock":
                            verticals_to_process.append(
                                vertical_url.attrib["url_name"])
                        if xblock.tag == "video":
                            print("Suspect video xblock")
    print(verticals_to_process)

    process_verticals(verticals_to_process)

if __name__ == "__main__":
    read_course_structure()
