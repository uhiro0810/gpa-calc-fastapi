import pandas as pd
import math

# 設定：名称が異なる場合は適宜書き換えてください
EXCLUDED_CATEGORY = "GPA計算対象外科目"           # 科目区分でGPA計算対象外を示すラベル
PF_VALUES = {"P", "F", "合格", "不合格"}          # P/F評価の値

def compute_gpa_and_ratio(csv_path: str,
                          gp_map: dict[str, float] | None = None) -> tuple[float, float]:
    """
    ① 累計GPA（GPA計算対象外＋P/Fを除外）
    ② A以上の単位割合（P/Fのみ除外）
    """
    # 既定のGPA換算（4.3制）
    if gp_map is None:
        gp_map = {"A+": 4.3, "A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0}

    df = pd.read_csv(csv_path)
    df.columns = [c.strip() for c in df.columns]  # 列名の余分な空白を除去
    df["単位数"] = pd.to_numeric(df["単位数"], errors="coerce")

    # P/F 判定
    is_pf = df["総合評価"].isin(PF_VALUES)

    # ---- ① 累計GPA：GPA計算対象外を除き、かつ P/F を除外した文字評価のみ ----
    is_letter = df["総合評価"].isin(gp_map.keys())
    is_gpa_eligible = (~is_pf) & is_letter & (df["科目区分"] != EXCLUDED_CATEGORY)

    gpa_df = df.loc[is_gpa_eligible].copy()
    gpa_df["gp"] = gpa_df["総合評価"].map(gp_map)

    total_cred = gpa_df["単位数"].sum(skipna=True)
    total_gp   = (gpa_df["gp"] * gpa_df["単位数"]).sum(skipna=True)
    gpa = (total_gp / total_cred) if total_cred > 0 else math.nan

    # ---- ② A以上の単位割合：P/Fのみ除外（GPA計算対象外は含める）----
    non_pf_letter = df.loc[(~is_pf) & is_letter].copy()
    a_or_above_cred = non_pf_letter.loc[
        non_pf_letter["総合評価"].isin(["A+", "A"]), "単位数"
    ].sum(skipna=True)
    non_pf_total_cred = non_pf_letter["単位数"].sum(skipna=True)
    ratio = (a_or_above_cred / non_pf_total_cred) if non_pf_total_cred > 0 else math.nan

    return gpa, ratio


def main():
    gpa, ratio = compute_gpa_and_ratio("SIRS202312944.csv")
    print(f"累計 GPA: {gpa:.3f}")
    print(f"A 以上(非P/F)の単位割合: {ratio*100:.2f}%")


if __name__ == "__main__":
    main()
