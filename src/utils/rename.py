# import re
# from typing import List
#
# from lib.rename import DefaultValues, Rename

# class RenameArgsValidator:
#     def __init__(self, *args, **kwargs):
#         self.passed_args = args
#
#     @property
#     def rename_class_keys(self) -> List[str]:
#         return Rename.__dataclass_fields__.keys()
#
#     @staticmethod
#     def validate_new_name():
#         ext_pattern = re.compile(DefaultValues.ANY_EXTENSION_PATTERN.value)
#         if ext_pattern.search(self.new_name):
#             raise ValueError(f'--new_name option "{self.new_name}" contains extension characters.')
#
#         if type(self.replacement_with_separator_pattern) is str:
#             self.replacement_with_separator_pattern: Pattern = re.compile(self.replacement_with_separator_pattern)
