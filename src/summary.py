from usecases.action import Action
from usecases.info import Information


class SummaryVisitor:

    def report_without_actions(self) -> str:
        pass

    def title(self) -> str:
        pass


class Summary(Action):

    def __init__(self, description: str, filename: str, visitor: SummaryVisitor):
        self.actions: dict[str, list[Information]] = {"Uploaded": [], "Removed": []}
        self.description: str = description
        self.filename: str = filename
        self.visitor = visitor

    def _format_summary(self) -> list[str]:
        lines: list[str] = [self.visitor.title()]
        if not self.actions["Uploaded"] and not self.actions["Removed"]:
            lines.append(self.visitor.report_without_actions())
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

    def export(self):
        text = self._format_summary()
        print("\n".join(text))
        with open(self.filename, "w") as file:
            file.write("\n".join(text))

    def insert_uploaded(self, information: Information):
        self.actions["Uploaded"].append(information)

    def insert_removed(self, information: Information):
        self.actions["Removed"].append(information)
