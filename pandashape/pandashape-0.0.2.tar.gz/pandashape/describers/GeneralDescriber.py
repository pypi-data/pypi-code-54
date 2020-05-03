from .GenericDescriber import GenericDescriber


class GeneralDescriber(GenericDescriber):
    def __init__(self, df):
        super().__init__(df)

    def describe(self, df):
        messages = [f"Shape: {df.shape}"]

        columns_with_nulls = df.columns[df.isna().any()].array
        if len(columns_with_nulls) > 0:
            messages.append(
                f"Columns with one or more null values: {columns_with_nulls}"
            )

        object_typed_columns = df.select_dtypes(include='object').columns.array
        if len(object_typed_columns) > 0:
            messages.append(
                f"Columns of type \"object\" (may need label encoding): ${object_typed_columns}"
            )

        return messages
