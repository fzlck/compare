import pandas as pd


def main():
    orig_df = pd.read_excel("EXP_PB_DYNPAR_DELTA_STR_CLIENT.xlsx")

    orig_grouped = orig_df.groupby("OSS_NODE_ID")

    result_df = pd.read_excel("Parameter.xlsx")
    result_grouped = result_df.groupby("OSS_NODE_ID")

    orig_final_df = pd.DataFrame()
    result_final_df = pd.DataFrame()

    for orig_oss_node_id, orig_group_data in orig_grouped:
        print(orig_oss_node_id)
        if orig_oss_node_id in result_grouped.groups:
            result_group_data = result_grouped.get_group(orig_oss_node_id)
            result_group_data.loc[:, "VALUE"] = result_group_data["VALUE"].str.replace("_u_", "_&_")

            merged_df = pd.merge(orig_group_data, result_group_data, how="outer", indicator=True)

            orig_only = merged_df[merged_df["_merge"] == "left_only"].drop(columns=["_merge"])
            result_only = merged_df[merged_df["_merge"] == "right_only"].drop(columns=["_merge"])
            
            orig_final_df = pd.concat([orig_final_df, pd.concat([orig_only], axis=1)],ignore_index=True)
            result_final_df = pd.concat([result_final_df, pd.concat([result_only], axis=1)],ignore_index=True)

    orig_file_path = "OG_DIFF.xlsx"
    orig_final_df.to_excel(orig_file_path, index=False, engine="openpyxl")
    result_file_path = "RESULT_DIFF.xlsx"
    result_final_df.to_excel(result_file_path, index=False, engine="openpyxl")        


if __name__ == "__main__":
    main()
