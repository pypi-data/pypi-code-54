import sys
from os import path
from robot.api import TestData
from .testDataDependencyBuilder import TestDataDependencyBuilder
from .testDataVisitor import TestDataVisitor, FindVisitor
from .usageFinder import KeywordUsageFinder, VariableUsageFinder
from .refactorHelper import KeywordRefactorHelper, VariableRefactorHelper
from robot.parsing.model import ResourceFile
from .referencesMethods import get_keyword_object_replace_method, get_variable_object_replace_method

class RefactoringFacade:
    def get_instance_from_testData(self, instanceName, table):
        return next((instance for instance in table if instance.name.upper() == instanceName.upper()),None)

    def build(self, path):
        suite = TestData(source=path)
        builder = TestDataDependencyBuilder()
        root = builder.build(suite)
        return root

    def get_testData_node(self, root, source):
        find_visitor = FindVisitor(root, source)
        return find_visitor.get_result()[0] if find_visitor.has_result() else None

    def get_keyword_obj_from_file(self, root, kwName, source):
        testData = self.get_testData_node(root, source).get_data()
        return self.get_instance_from_testData(kwName, testData.keyword_table)

    def get_variable_obj_from_file(self, root, varName, source):
        testData = self.get_testData_node(root, source).get_data()
        return self.get_instance_from_testData(varName, testData.variable_table)

    def get_keyword_references(self, root, keyword):
        source = keyword.source
        finder = KeywordUsageFinder()
        node = self.get_testData_node(root, source)
        references = {}
        def visit(node):
            node_source = node.get_data().source
            if node_source not in references.keys():
                references[node_source] = finder.find_usage_from_testdataFile(keyword.name, node.get_data())
            return True
        node.accept(TestDataVisitor(visit))
        return [reference for reference in references.values() if len(reference['references']) > 0 ]

    def get_variable_references(self, root, variable):
        source = variable.parent.parent.source
        finder = VariableUsageFinder()
        node = self.get_testData_node(root, source)
        references = {}
        def visit(node):
            node_source = node.get_data().source
            if node_source not in references.keys():
                references[node_source] = finder.find_global_variable_from_testdata_file(variable, node.get_data())
            return True
        node.accept(TestDataVisitor(visit))
        return [reference for reference in references.values() if len(reference['references']) > 0 ]

    def rename_variable_references(self, references, oldVariableName, newVariableName):
        VariableRefactorHelper().rename_variable(references, oldVariableName, newVariableName)

    def rename_keyword_references(self, references, oldKeywordName, newKeywordName):
        KeywordRefactorHelper().rename_keyword(references, oldKeywordName, newKeywordName)

    def rename_keyword_def(self, keyword, newName):
        replace_method = get_keyword_object_replace_method()
        replace_method(keyword, keyword.name, newName)

    def rename_variable_def(self, variable, newName):
        replace_method = get_variable_object_replace_method()
        replace_method(variable, variable.name, newName)

    def save_test_data_files(self, testDataFiles):
        for testData in testDataFiles:
            self.save(testData)

    def save(self, testData):
        testData.save()

    def print_dependency(self, root):
        def visit(node):
            print(node.get_data().source)
            return True
        root.accept(TestDataVisitor(visit))