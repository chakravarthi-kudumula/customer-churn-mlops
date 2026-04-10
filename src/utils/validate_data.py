import pandas as pd
import great_expectations as gx
from typing import Tuple, List


def validate_telco_data(df) -> Tuple[bool, List[str]]:
    """
    Comprehensive data validation for Telco Customer Churn dataset using Great Expectations.

    Input:
        df : pandas DataFrame

    Output:
        (is_valid, failed_expectations)
        is_valid -> bool
        failed_expectations -> List[str]
    """
    print("🔍 Starting data validation with Great Expectations...")

    failed_expectations = []

    try:
        # ------------------------------------------------------------------
        # STEP 0: Work on a copy so original dataframe is untouched
        # ------------------------------------------------------------------
        df = df.copy()

        # Clean TotalCharges BEFORE validation because raw telco data often
        # contains blank strings for new customers
        if "TotalCharges" in df.columns:
            df["TotalCharges"] = df["TotalCharges"].replace(r"^\s*$", pd.NA, regex=True)
            df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

        # ------------------------------------------------------------------
        # STEP 1: Create GX context / datasource / asset / batch
        # ------------------------------------------------------------------
        context = gx.get_context()

        datasource_name = "telco_pandas_source"
        asset_name = "telco_dataframe_asset"
        batch_definition_name = "telco_whole_dataframe"

        try:
            data_source = context.data_sources.get(datasource_name)
        except Exception:
            data_source = context.data_sources.add_pandas(name=datasource_name)

        try:
            data_asset = data_source.get_asset(asset_name)
        except Exception:
            data_asset = data_source.add_dataframe_asset(name=asset_name)

        try:
            batch_definition = data_asset.get_batch_definition(batch_definition_name)
        except Exception:
            batch_definition = data_asset.add_batch_definition_whole_dataframe(
                batch_definition_name
            )

        batch = batch_definition.get_batch(batch_parameters={"dataframe": df})

        validations = []

        # ------------------------------------------------------------------
        # STEP 2: Schema validation
        # ------------------------------------------------------------------
        print("   📋 Validating schema and required columns...")

        required_columns = [
            "customerID",
            "gender",
            "SeniorCitizen",
            "Partner",
            "Dependents",
            "tenure",
            "PhoneService",
            "MultipleLines",
            "InternetService",
            "OnlineSecurity",
            "OnlineBackup",
            "DeviceProtection",
            "TechSupport",
            "StreamingTV",
            "StreamingMovies",
            "Contract",
            "PaperlessBilling",
            "PaymentMethod",
            "MonthlyCharges",
            "TotalCharges",
            "Churn",
        ]

        for col in required_columns:
            validations.append(
                batch.validate(gx.expectations.ExpectColumnToExist(column=col))
            )

        validations.append(
            batch.validate(
                gx.expectations.ExpectColumnValuesToNotBeNull(column="customerID")
            )
        )

        # ------------------------------------------------------------------
        # STEP 3: Business logic validation
        # ------------------------------------------------------------------
        print("   💼 Validating business logic constraints...")

        validations.append(
            batch.validate(
                gx.expectations.ExpectColumnValuesToBeInSet(
                    column="gender",
                    value_set=["Male", "Female"],
                )
            )
        )

        validations.append(
            batch.validate(
                gx.expectations.ExpectColumnValuesToBeInSet(
                    column="Partner",
                    value_set=["Yes", "No"],
                )
            )
        )

        validations.append(
            batch.validate(
                gx.expectations.ExpectColumnValuesToBeInSet(
                    column="Dependents",
                    value_set=["Yes", "No"],
                )
            )
        )

        validations.append(
            batch.validate(
                gx.expectations.ExpectColumnValuesToBeInSet(
                    column="PhoneService",
                    value_set=["Yes", "No"],
                )
            )
        )

        validations.append(
            batch.validate(
                gx.expectations.ExpectColumnValuesToBeInSet(
                    column="Contract",
                    value_set=["Month-to-month", "One year", "Two year"],
                )
            )
        )

        validations.append(
            batch.validate(
                gx.expectations.ExpectColumnValuesToBeInSet(
                    column="InternetService",
                    value_set=["DSL", "Fiber optic", "No"],
                )
            )
        )

        validations.append(
            batch.validate(
                gx.expectations.ExpectColumnValuesToBeInSet(
                    column="Churn",
                    value_set=["Yes", "No"],
                )
            )
        )

        # ------------------------------------------------------------------
        # STEP 4: Numeric validation
        # ------------------------------------------------------------------
        print("   📊 Validating numeric ranges and business constraints...")

        validations.append(
            batch.validate(
                gx.expectations.ExpectColumnValuesToNotBeNull(column="tenure")
            )
        )

        validations.append(
            batch.validate(
                gx.expectations.ExpectColumnValuesToNotBeNull(column="MonthlyCharges")
            )
        )

        validations.append(
            batch.validate(
                gx.expectations.ExpectColumnValuesToBeBetween(
                    column="tenure",
                    min_value=0,
                    max_value=120,
                )
            )
        )

        validations.append(
            batch.validate(
                gx.expectations.ExpectColumnValuesToBeBetween(
                    column="MonthlyCharges",
                    min_value=0,
                    max_value=200,
                )
            )
        )

        # TotalCharges in raw telco data may be null for some brand-new customers,
        # so use mostly instead of forcing every row to pass.
        validations.append(
            batch.validate(
                gx.expectations.ExpectColumnValuesToBeBetween(
                    column="TotalCharges",
                    min_value=0,
                    mostly=0.99,
                )
            )
        )

        # ------------------------------------------------------------------
        # STEP 5: Optional consistency rule
        # ------------------------------------------------------------------
        print("   🔗 Validating data consistency...")

        # Raw data can contain edge cases for very new customers, so keep this
        # rule relaxed. If it becomes noisy later, you can remove it completely.
        validations.append(
            batch.validate(
                gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
                    column_A="TotalCharges",
                    column_B="MonthlyCharges",
                    or_equal=True,
                    mostly=0.90,
                )
            )
        )

        # ------------------------------------------------------------------
        # STEP 6: Process results
        # ------------------------------------------------------------------
        total_checks = len(validations)
        passed_checks = sum(1 for r in validations if r.success)
        failed_checks = total_checks - passed_checks

        for r in validations:
            if not r.success:
                try:
                    failed_expectations.append(r.expectation_config.type)
                except Exception:
                    failed_expectations.append("unknown_expectation")

        is_valid = failed_checks == 0

        if is_valid:
            print(f"✅ Data validation PASSED: {passed_checks}/{total_checks} checks successful")
        else:
            print(f"❌ Data validation FAILED: {failed_checks}/{total_checks} checks failed")
            print(f"   Failed expectations: {failed_expectations}")

        return is_valid, failed_expectations

    except Exception as e:
        print(f"❌ Validation execution error: {e}")
        return False, [str(e)]