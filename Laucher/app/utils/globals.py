import os

class Globals:
    """
    Class containing all the globally accessible propertins and functions
    """

    @staticmethod
    def tools():
        """
        Return a list of available tools.

        This method retrieves the names of folders located within the 'tools'
        directory in the current working directory.

        Returns:
            list: A list containing the names of available tools (folders).
        """
        complete_path = os.path.join(os.getcwd(), 'tools')
        path_content = os.listdir(complete_path)

        folders = []
        for elem in path_content:
            if os.path.isdir(os.path.join(complete_path, elem)):
                folders.append(elem)

        return folders