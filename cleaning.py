#import libraries
import pandas as pd

#LOAD DATASET
df = pd.read_csv("banking_dataset.csv")
print("Original Shape:", df.shape)

#b4 cleaning
print("First 5 Rows:")
print(df.head())
print("/n Dataset information")
print(df.info())
print("\n Duplicate rows:",df.duplicated().sum())
print("\n Missing values:",df.isnull().sum())

#Remove exact duplicate rows
df = df.drop_duplicates()
print("Duplicate rows removed.")
print("Shape after removing duplicates:", df.shape)

#CHECK DUPLICATE TRANSACTION IDs
print("\nDuplicate Transaction IDs:")
print(df["TransactionID"].duplicated().sum())

# Remove duplicate TransactionIDs
# Keep the first occurrence
df = df.drop_duplicates(
    subset="TransactionID",
    keep="first"
)

print("Duplicate TransactionIDs removed.")

#CHECK MISSING VALUES
print("\nMissing Values Before Cleaning:")
print(df.isnull().sum())

#FILL MISSING NUMERICAL VALUES
numeric_columns = df.select_dtypes(
    include="number"
).columns

for column in numeric_columns:

    df[column] = df[column].fillna(
        df[column].median()
    )

#FILL MISSING TEXT VALUES
text_columns = df.select_dtypes(
    include="object"
).columns

for column in text_columns:

    df[column] = df[column].fillna(
        df[column].mode()[0]
    )

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

#REMOVE EXTRA SPACES FROM TEXT
for column in text_columns:

    df[column] = df[column].str.strip()

#CONVERT TRANSACTION DATE
df["TransactionDate"] = pd.to_datetime(
    df["TransactionDate"],
    errors="coerce"
)

#FIND OUTLIERS USING IQR

print("\n================ OUTLIER ANALYSIS ================")

for column in numeric_columns:

    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)

    IQR = Q3 - Q1

    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR

    outliers = df[
        (df[column] < lower_limit) |
        (df[column] > upper_limit)
    ]

    print("\nColumn:", column)
    print("Lower Limit:", lower_limit)
    print("Upper Limit:", upper_limit)
    print("Number of Outliers:", len(outliers))

#CREATE OUTLIER FLAG
df["Outlier"] = False

for column in numeric_columns:

    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)

    IQR = Q3 - Q1

    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR

    df.loc[
        (df[column] < lower_limit) |
        (df[column] > upper_limit),
        "Outlier"
    ] = True

#COUNT TOTAL OUTLIER RECORDS
print("\nTotal records containing outliers:")
print(df["Outlier"].sum())



#CHECK NEGATIVE ACCOUNT BALANCE
negative_balance = (
    df["AccountBalance"] < 0
).sum()

print("\nNegative Account Balances:")
print(negative_balance)



#FINAL CHECK
print("\n================ FINAL CHECK ================")

print("\nFinal Shape:")
print(df.shape)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nDuplicate TransactionIDs:")
print(
    df["TransactionID"].duplicated().sum()
)

#SAVE CLEANED DATASET
df.to_csv(
    "cleaned_banking_dataset.csv",
    index=False
)

print("\n========================================")
print("DATA CLEANING COMPLETED SUCCESSFULLY!")
print("========================================")

print(
    "\nCleaned file saved as: "
    "cleaned_banking_dataset.csv"
)
