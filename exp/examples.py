import pandas as pd

store = pd.HDFStore("table_store.d5")


# Example of how to access only the asr scores of the original table
their_table : pd.DataFrame = store["their_original_table_1"]
print(their_table.loc[:, [(attack, "asr") for attack in their_table.columns.levels[0]]])
# attacks                 AdvBench AutoDAN DeepInception    GCG HEx-PHI  PAIR SAP30 Template
# values                       asr     asr           asr    asr     asr   asr   asr      asr
# models defenses                                                                           
# Vicuna No-Defense            8.0    88.0         100.0  100.0    17.0  88.0  83.0     40.0
#        PPL                   8.0    88.0         100.0    0.0    15.0  88.0  83.0     40.0
#        Self-Examination      0.0     4.0          88.0   12.0     8.0  12.0  16.0     12.0
#        Paraphrase           14.0    70.0         100.0   20.0    23.0  26.0  58.0     32.0
#        Retokenization       30.0    76.0         100.0   42.0    33.0  76.0  72.0     53.0
#        Self-Reminder         0.0    70.0         100.0   42.0     8.0  48.0  45.0     35.0
#        ICD                   0.0    80.0         100.0   70.0     6.0  54.0  47.0     38.0
#        SafeDecoding          0.0     0.0           0.0    4.0     1.0   4.0   9.0      5.0
# Llama2 No-Defense            0.0     2.0          10.0   32.0     2.0  18.0   0.0      0.0
#        PPL                   0.0     2.0          10.0    0.0     2.0  18.0   0.0      0.0
#        Self-Examination      0.0     0.0           2.0   12.0     0.0   0.0   0.0      0.0
#        Paraphrase            2.0     0.0           8.0    4.0     3.0  12.0   0.0     11.0
#        Retokenization        0.0    10.0          40.0    2.0    15.0  20.0   5.0      3.0
#        Self-Reminder         0.0     0.0           4.0    0.0     0.0  14.0   0.0      0.0
#        ICD                   0.0     0.0           0.0    0.0     0.0   0.0   0.0      0.0
#        SafeDecoding          0.0     0.0           0.0    0.0     1.0   4.0   0.0      0.0


# Example of how to access our table's contents so far
our_table : pd.DataFrame = store["our_table"]
print(our_table)
# attacks                                   AdvBench    GCG  AutoDAN   PAIR  DeepInception
# models                  defenses                                                        
# vicuna_1x               No-Defense             4.0   98.0     88.0   88.0          100.0
#                         PPL                    4.0    0.0     88.0   88.0          100.0
#                         Self-Examination       0.0   12.0      4.0   12.0           92.0
#                         Retokenization        30.0   52.0     78.0   64.0          100.0
#                         Self-Reminder          2.0   48.0     68.0   46.0          100.0
#                         ICD                    0.0   72.0     80.0   40.0          100.0
#                         SafeDecoding           0.0    0.0      0.0    0.0            0.0
# llama2_1x               No-Defense             0.0   30.0      2.0   18.0           10.0
#                         PPL                    0.0    0.0      2.0   18.0           10.0
#                         Self-Examination       0.0   10.0      0.0    0.0            2.0
#                         Retokenization         4.0    6.0      6.0   36.0           44.0
#                         Self-Reminder          0.0    0.0      2.0   14.0            2.0
#                         ICD                    0.0    2.0      0.0    0.0            0.0
#                         SafeDecoding           0.0    0.0      0.0    0.0            0.0
# dolphin_1x_not_original SafeDecoding         100.0   98.0    100.0   98.0          100.0
# dolphin_2x              SafeDecoding         100.0   98.0    100.0   98.0          100.0
# dolphin_4x              SafeDecoding         100.0   98.0    100.0   98.0          100.0
# dolphin_8x              SafeDecoding         100.0   98.0    100.0   98.0          100.0
# falcon_1x               SafeDecoding          18.0    8.0      0.0   12.0            0.0
# falcon_2x               SafeDecoding          22.0   12.0      0.0   16.0            0.0
# falcon_4x               SafeDecoding          22.0   16.0      0.0   14.0            0.0
# falcon_8x               SafeDecoding          30.0   14.0      2.0   22.0            0.0
# guanaco_1x_not_original SafeDecoding           2.0   30.0      4.0    4.0           16.0
# guanaco_2x              SafeDecoding           2.0   30.0     52.0   32.0           12.0
# guanaco_4x              SafeDecoding          56.0   82.0     92.0   66.0          100.0
# guanaco_8x              SafeDecoding          96.0  100.0    100.0  100.0          100.0
# llama2_1x_not_original  SafeDecoding           0.0    0.0      0.0    0.0            0.0
# llama2_2x               SafeDecoding           0.0    0.0      0.0   10.0            6.0
# llama2_4x               SafeDecoding           0.0    0.0      0.0    6.0            0.0
# llama2_8x               SafeDecoding           0.0    0.0      0.0    4.0            0.0
# vicuna_2x               SafeDecoding           2.0    4.0      0.0    6.0            0.0
# vicuna_4x               SafeDecoding           2.0    4.0     12.0    4.0            0.0
# vicuna_8x               SafeDecoding           2.0    4.0      0.0    2.0            0.0

store.close()