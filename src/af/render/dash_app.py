import dash_bio
from dash import html
from dash_bio.utils import PdbParser, create_mol3d_style
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash

app = DjangoDash("AF-Plots")

parser = PdbParser(
    "/Users/aradhya/Desktop/Uni-Projects/group-project/out/test_unrelaxed_rank_002_alphafold2_ptm_model_4_seed_000.pdb"
)

parser_2 = PdbParser(
    "/Users/aradhya/Desktop/Uni-Projects/group-project/out/test_unrelaxed_rank_004_alphafold2_ptm_model_5_seed_000.pdb"
)

data_2 = parser.mol3d_data()
styles_2 = create_mol3d_style(
    data_2["atoms"], visualization_type="cartoon", color_element="residue"
)
data = parser.mol3d_data()
styles = create_mol3d_style(
    data["atoms"], visualization_type="cartoon", color_element="residue"
)


app.layout = html.Div(
    [
        dash_bio.Molecule3dViewer(
            id="dashbio-default-molecule3d",
            modelData=data,
            styles=styles,
            style={"width": "50%"},
        ),
        dash_bio.Molecule3dViewer(
            id="dashbio-default-molecule3d-2",
            modelData=data_2,
            styles=styles_2,
            style={"width": "50%"},
        ),
    ],
    style={
        "background": "black",
        "height": "100vh",
        "width": "100vw",
        "display": "flex",
    },
)
