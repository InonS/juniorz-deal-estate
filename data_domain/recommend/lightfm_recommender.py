"""
Recommendation using LightFM.
"""
from lightfm import LightFM
from scipy import sparse

def train_recommender(interactions: sparse.coo_matrix) -> LightFM:
    """
    Train a LightFM hybrid recommendation model.

    Args:
        interactions: User-item interaction matrix.

    Returns:
        Trained LightFM model.

    >>> from scipy.sparse import coo_matrix
    >>> interactions = coo_matrix([[1, 0], [0, 1]])
    >>> model = train_recommender(interactions)
    >>> isinstance(model, LightFM)
    True
    """
    model = LightFM(loss="warp")
    model.fit(interactions, epochs=10, num_threads=2)
    return model