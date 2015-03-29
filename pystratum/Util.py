import os


# ----------------------------------------------------------------------------------------------------------------------
class Util:
    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_two_phases(the_filename, the_data):
        """
        Writes a file in two phase to the filesystem.

        First write the data to a temporary file (in the same directory) and than renames the temporary file. If the
        file already exists and its content is equal to the data that must be written no action is taken. This has the
        following advantages:
        * In case of some write error (e.g. disk full) the original file is kep in tact and no file with partially data
        is written.
        * Renaming a file is atomic. So, running processes will never read a partially written data.

        :param str the_filename: The name of the file were the data must be stored.
        :param str the_data: The data that must be written.
        """
        write_flag = True
        if os.path.exists(the_filename):
            with open(the_filename, 'r') as f:
                old_data = f.read()
                if the_data == old_data:
                    write_flag = False

        if write_flag:
            tmp_filename = the_filename + '.tmp'
            with open(tmp_filename, 'w+') as f:
                f.write(the_data)
            os.replace(tmp_filename, the_filename)
            print("Wrote: '%s'." % the_filename)

# ----------------------------------------------------------------------------------------------------------------------
