from functions import merge_csvs, add_time_features, add_unique_customer_no, add_first_section_feature

df = merge_csvs()
df = add_time_features(df)
df = add_unique_customer_no(df)
df = add_first_section_feature(df)

df = df.set_index('index')

df.to_csv('../data/clean_test.csv')