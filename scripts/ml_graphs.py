import pickle
import plotly.graph_objs as go

def return_ml_figures(cnf_matrix_pkl):
    """Creates plotly visualization

    Args:
        cnf_matrix_pkl

    Returns:
        list (dict): list containing the plotly visualization
    """
    # load data
    file = open(cnf_matrix_pkl, 'rb')
    cnf_matrix = pickle.load(file)
    file.close()

    genre_list = ['Country','Electronic','Folk','Hip-Hop','Indie','Jazz',
                  'Metal','Not Available','Other','Pop','R&B','Rock']

    # Confusion matrix as heatmap
    graph_one = []

    graph_one.append(
        go.Heatmap(
            z = cnf_matrix,
            x = genre_list,
            y = genre_list
        )
    )

    layout_one = dict(
        xaxis = dict(title = 'Predicted Label'),
        yaxis = dict(title = 'True Label')
    )

    # add to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))

    return figures