from great_tables import GT, style, loc

"""	            1x	2x	4x	8x
per category	2	4	8	16
unique prompts	36	72	144	288
max samples	    72	144	288	576
vicuna actual	71	128	252	472
llama2 actual	72	142	286	571
dophin actual	61	116	229	430
falcon actual	70	126	249	428
guanaco actual	69	123	234	434"""

data = {
"":["per category", "unique prompts", "max samples", "vicuna actual", "llama2 actual", "dolphin actual", "falcon actual", "guanaco actual"],
"1x":["2", "36", "72", "71", "72", "61", "70", "69"],
"2x":["4", "72", "144", "128", "142", "116", "126", "123"],
"4x":["8", "144", "288", "252", "286", "229", "249", "234"],
"8x":["16", "288", "576", "472", "571", "430", "428", "434"]
}

from pandas import DataFrame
dt_data = DataFrame(data)

(
    GT(data=dt_data)
    .tab_style(style=style.borders(sides=["all"], color="#d3d3d3"), locations=loc.body(columns=["1x", "2x", "4x", "8x"]))
    # .tab_style(style=style.borders(sides=["right"]), locations=loc.body(columns=["AdvBench (ours)", "GCG (ours)", "AutoDAN (ours)", "PAIR (ours)", "DeepInception (ours)"]))
    .save(file="dataset_size.png", web_driver="firefox")
)