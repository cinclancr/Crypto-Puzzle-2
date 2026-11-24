import numpy as np


def test_median_consensus_two_out_of_three():
    obs=np.array([[[0,1],[1,1]],[[0,1],[1,0]],[[1,1],[0,1]]])
    assert (obs.sum(axis=0)>=2).astype(int).tolist()==[[0,1],[1,1]]


def test_layer_union_not_independent_message():
    a=np.array([[1,0],[0,1]],dtype=bool)
    c=np.array([[0,1],[0,1]],dtype=bool)
    b=a|c
    assert b.tolist()==[[True,True],[False,True]]
