import os
import pprint

import xmltodict

"""
    Uncompressed .tar.gz courses are a flat representation of nested course
    structure, therefore each element type (chapter, sequential, vertical)
    is stored in a folder of its name on the filesystem, et and can be identified by
    its url_name. Ex. sequential/12ef45.xml, this file contains url_names of this element children
    which will be store in their element name folder.
"""


PATH = "/Users/richard/dev/fun/video-migration/moocs/selection/CNAM...01002S03...session03"

CLOUDFRONT_URL = "https://d381hmu4snvm3e.cloudfront.net/videos/{video_id}/HD.mp4"

def read_xmlfile(folder, url_name):
    """
    """
    with open(os.path.join(PATH, folder, url_name + ".xml"), "r") as f:
        return xmltodict.parse(f.read())


def prettyprint(data):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(data)


def ensure_list(maybe_list):
    """
    Convenientely returns a list if passed a single element, because
    if a node have a single child and xmltodict will return
    a OrderedDict when we expect a list of them
    """
    if type(maybe_list) == list:
        return maybe_list
    else:
        return [maybe_list]


def replace_video_xblock(url_name):
    """
    Regenerate a vertical to change its video xblock
    """
    print("            Libcast video xblock for video ID: {url}".format(
        url=CLOUDFRONT_URL.format(video_id=xblock["@video_id"])))

#replace_video_xblock(url_name=vertical_url["@url_name"])


def filter_children(node):
    """
    Filter node children names over properties
    """
    return [key for key in node.keys() if not key.startswith('@')]

def process_verticals(verticals_to_process):
    """
    Rewrite vertical xml file containin xblock we aim.
    """

    for url_name in verticals_to_process:
        vertical = read_xmlfile("vertical", url_name)

        import ipdb; ipdb.set_trace()
        #for xblock_name in filter_children(vertical):


        new_vertical = xmltodict.unparse(vertical, full_document=False, short_empty_elements=True)

def read_course_structure():

    base = read_xmlfile("", "course")
    print("Course key: {url_name}/{org}/{course}".format(
        url_name=base["course"]["@url_name"],
        org=base["course"]["@org"],
        course=base["course"]["@course"]))

    verticals_to_process = []

    # This node (chapters) contains "Advanced settings", course chapter and wiki url key
    chapters = read_xmlfile("course", base["course"]["@url_name"])
    print("Course name: {display_name}".format(display_name=chapters["course"]["@display_name"]))

    for chapter_url in ensure_list(chapters["course"]["chapter"]):
        chapter = read_xmlfile("chapter", chapter_url["@url_name"])
        print("    Chapter name: {display_name}".format(display_name=chapter["chapter"]["@display_name"]))

        for sequential_url in ensure_list(chapter["chapter"]["sequential"]):
            sequential = read_xmlfile("sequential", sequential_url["@url_name"])
            print("        Sequential name: {display_name}".format(display_name=sequential["sequential"]["@display_name"]))

            for vertical_url in ensure_list(sequential["sequential"]["vertical"]):
                vertical = read_xmlfile("vertical", vertical_url["@url_name"])
                print("            Vertical name: {display_name}".format(display_name=vertical["vertical"]["@display_name"]))

                xblocks = filter_children(vertical["vertical"])
                if "libcast_xblock" in xblocks:
                    verticals_to_process.append(vertical_url["@url_name"])

    process_verticals(verticals_to_process)

if __name__ == "__main__":
    read_course_structure()

