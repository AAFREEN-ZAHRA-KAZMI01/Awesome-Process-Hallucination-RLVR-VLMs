Editable draw.io sources of every diagram in the paper
-------------------------------------------------------
Geometry copied from the paper figures: every box has the same position, size, colour and text as in the
PDF (read from the LaTeX/TikZ node coordinates and from framework_fig.py). Only line breaks inside a box can
differ slightly, because draw.io and LaTeX wrap text differently. previews/ shows how each file renders.

26I-7675_all_diagrams.drawio  -> all five diagrams, one per page (tabs at the bottom in draw.io)
fig1_teaser.drawio            -> Fig. 1  process-hallucination example
fig2_research_design.drawio   -> Fig. 2  research design flowchart
fig3_prisma_2020.drawio       -> Fig. 3  PRISMA 2020 flow diagram
fig10_framework.drawio        -> Fig. 10 two-axis framework (verification target x source)
fig12_case_study.drawio       -> Fig. 12 manufacturing inspection case study

How to open: go to https://app.diagrams.net -> File -> Open from -> Device -> choose a .drawio file.
How to paste instead: draw.io -> Extras -> Edit Diagram -> delete the text there -> paste the content of a file
in paste_xml/ -> OK.

The data charts (Figs. 4-9, 11, 13) are not drawings: their editable source is the Python code in
scripts/ and the notebook (26I-7675_MAI-1B.ipynb), which regenerates them from the data.
