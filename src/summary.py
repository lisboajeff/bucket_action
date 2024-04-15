from usecases.info import Information


class Action:

    def insert_uploaded(self, information: Information):
        pass

    def insert_removed(self, information: Information):
        pass


class Summary(Action):

    def __init__(self, description: str):
        self.actions: dict[str, list[Information]] = {"Uploaded": [], "Removed": []}
        self.description: str = description

    def _format_summary(self) -> list[str]:
        lines: list[str] = []
        if not self.actions["Uploaded"] and not self.actions["Removed"]:
            lines.append("No file was added or removed.")
        else:
            lines.append("| Action | Description  | File Name | Old Hash | New Hash |")
            lines.append("|---| ---  |---| --- | --- |")
            for info in self.actions["Uploaded"]:
                lines.append(
                    f"| Uploaded    | {self.description} |  {info.get_file_path()} | {info.get_old_hash()} "
                    f"| {info.get_hash()} |")
            for info in self.actions["Removed"]:
                lines.append(
                    f"| Removed     | {self.description} | {info.get_file_path()} | {info.get_old_hash()} "
                    f"| {info.get_hash()} |")
        return lines

    def write_text(self, filename: str):
        text = self._format_summary()
        print("\n".join(text))
        with open(filename, "w") as file:
            file.write("\n".join(text))

    def insert_uploaded(self, information: Information):
        self.actions["Uploaded"].append(information)

    def insert_removed(self, information: Information):
        self.actions["Removed"].append(information)
