import os
import traceback
try:
    import md5
except:
    from hashlib import md5

ROOT_DIRECTORY = os.getcwd()
KODI_VERSIONS = [
    {
        "release": "Matrix",
        "target_dir": "matrix",
        "python_version": "3.0.0"
        },
    {
        "release": "Leia",
        "target_dir": "leia",
        "python_version": "2.26.0"
        }
    ]


def is_addon_dir(addon):
    """
    Confirms addon directory exists
    :param addon: addon directory path
    :type addon: str
    :return: True if path exists, else False
    :rtype: bool
    """
    if not os.path.isdir(addon) or addon == ".svn":
        return False
    else:
        return True


def print_traceback():
    traceback.print_exc()


class Generator:
    """
        Generates a new addons.xml file from each addons addon.xml file
        and a new addons.xml.md5 hash file. Must be run from the root of
        the checked-out repo. Only handles single depth folder structure.
    """

    def __init__(self, release_target):
        self.release = release_target
        self.target_path = os.path.join(ROOT_DIRECTORY, release_target["target_dir"])
        self.addons_xml = os.path.join(self.target_path, "addons.xml")
        self.addons_xml_md5 = os.path.join(self.target_path, "addons.xml.md5")
        self._generate_addons_files()

    def _generate_addons_files(self):
        addons = os.listdir(self.target_path)
        addons_xml = u"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<addons>\n"
        found_an_addon = False

        for addon in addons:
            _path = None
            try:
                target_addon = os.path.join(self.target_path, addon)
                if is_addon_dir(target_addon):
                    _path = os.path.join(target_addon, "addon.xml")

                    if _path and os.path.exists(_path):
                        found_an_addon = True

                    xml_lines = open(_path, "r").read().splitlines()
                    addon_xml = ""

                    for line in xml_lines:
                        if line.find("<?xml") >= 0: continue
                        addon_xml += str(line.rstrip() + "\n")

                    addons_xml += addon_xml.rstrip() + "\n\n"

            except Exception as e:
                print_traceback()
                print("Excluding %s for %s" % (_path, e,))

        # clean and add closing tag
        addons_xml = addons_xml.strip() + u"\n</addons>\n"

        if found_an_addon:
            self._save_file(addons_xml, self.addons_xml)
            self._generate_md5_file()
            print("Updated addons xml and addons.xml.md5 files")
        else:
            print("Could not find any addons, so script has done nothing.")

    def _generate_md5_file(self):
        try:
            try:
                m = md5.new(open(self.addons_xml).read()).hexdigest()
            except AttributeError:
                m = md5(open(self.addons_xml).read().encode('utf-8')).hexdigest()

            self._save_file(m, self.addons_xml_md5)

        except Exception as e:
            print("An error occurred creating addons.xml.md5 file!\n%s" % (e,))

    def _save_file(self, data, the_path):
        try:
            open(the_path, "w").write(str(data))
        except Exception as e:
            print_traceback()
            print("An error occurred saving %s file!\n%s" % (the_path, e,))


def execute(release):
    print("Running generator for release: {}".format(release["release"]))
    Generator(release)


if __name__ == "__main__":
    for release in KODI_VERSIONS:
        execute(release)


