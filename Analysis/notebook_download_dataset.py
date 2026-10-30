import marimo

__generated_with = "0.25.2"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Accessing dataset Random Dot Kinematograms in Desert Locusts on Marimo notebook
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Marimo notebook is similar to jupyter notebook, where you can interact with codes cell by cell (or block by block). Nevertheless, the biggest difference between the two is that Marimo notebook can automatically synchronise the value of global variables to all of the activated cells. This helps demonstrate a database like this, because you do not need to remember which cell to activate and which one to skip, but it is tricky to prototype a script on Marimo.

    #### A useful tip for new Marimo notebook users: get used to local variables and global variables
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### What is a local variable on Marimo notebook?
    #### A variable whose name starts from an _, for example _file_name
    #### When a local variable gets updated, it will only affect code within the same cell. By contrast, a global variable will affect the entire notebook. Therefore, it is impossible to define two global variables with the same name.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Anyway, let us give it a try.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Session 0: loading package depandancies and environmental variables
    """)
    return


@app.cell
def _():
    import marimo as mo
    from pathlib import Path

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Session 1: Gaining access to the dataset
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Session 1.1: we used a 3-party package zenodo_get to download data from Zenodo (skip this session if you have access to the server of AG Couzin-Fuchs)
    """)
    return


@app.cell
def _(download):
    # the raw dataset is huge so I would recommend you to prepar a 10GB space to your local hard drive. 

    #"10.5281/zenodo.23565813" is the dataset ID on Zenodo

    # specify either the full file name or some pattern of the file name to download the data you want in file_glob. For example:
    ## to download the curated database, type "*.gzip"
    ## to download the raw database, type "*.zip"
    ## to download the metadata, type "*.xlsx"
    ## typing "*.pdf", will download both the protocol and manuscript, so I would recommend using the full name in this scenario

    files_local_location="/Users/chiyu_lee/Downloads"# change here to where you want to download the dataset
    download("10.5281/zenodo.23565813",output_dir=files_local_location,file_glob="*.zip")
    return


if __name__ == "__main__":
    app.run()
