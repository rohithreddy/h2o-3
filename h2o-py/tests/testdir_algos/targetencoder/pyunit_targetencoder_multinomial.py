from __future__ import print_function
import os
import sys

from numpy.testing import assert_allclose

sys.path.insert(1, os.path.join("..","..","..",".."))
import h2o
from h2o.estimators import H2OTargetEncoderEstimator
from tests import pyunit_utils as pu

seed = 42

# NOT SUPPORTED YET


def load_dataset(incl_test=False, incl_foldc=False):
    fr = h2o.import_file(pu.locate("smalldata/titanic/titanic_expanded.csv"), header=1)
    target = "pclass"
    train = fr
    test = None
    if incl_test:
        fr = fr.split_frame(ratios=[.8], destination_frames=["titanic_train", "titanic_test"], seed=seed)
        train = fr[0]
        test = fr[1]
    if incl_foldc:
        train["foldc"] = train.kfold_column(3, seed)
    return pu.ns(train=train, test=test, target=target)


def test_multinomial_with_none():
    ds = load_dataset()
    te = H2OTargetEncoderEstimator(noise=0, data_leakage_handling="none")
    te.train(y=ds.target, training_frame=ds.train)
    encoded = te.transform(ds.train, as_training=True)
    print(encoded)
    # col_te_golden = [0.18874, 0.18874, 0.18874, 0.73177, 0.18874]
    # col_te = encoded['sex_te'].head(5).as_data_frame().values.reshape(-1).tolist()
    # assert_allclose(col_te, col_te_golden, atol=1e-5)

    # with open("./golden/multinomial_none.csv", "w") as f:
    #     f.write(encoded.get_frame_data())
    # golden = h2o.import_file("./golden/multinomial_none.csv")
    # assert pu.compare_frames(golden, encoded, 0, tol_numeric=1e-5)


def test_multinomial_with_kfold():
    ds = load_dataset(incl_foldc=True)
    te = H2OTargetEncoderEstimator(noise=0, data_leakage_handling="kfold")
    te.train(y=ds.target, training_frame=ds.train, fold_column="foldc")
    encoded = te.transform(ds.train, as_training=True)
    print(encoded)
    # col_te_golden = [0.18382, 0.20444, 0.17763, 0.72294, 0.17763]
    # col_te = encoded['sex_te'].head(5).as_data_frame().values.reshape(-1).tolist()
    # assert_allclose(col_te, col_te_golden, atol=1e-5)
    
    # with open("./golden/multinomial_kfold.csv", "w") as f:
    #     f.write(encoded.get_frame_data())
    # golden = h2o.import_file("./golden/multinomial_kfold.csv")
    # assert pu.compare_frames(golden, encoded, 0, tol_numeric=1e-5)


def test_multinomial_with_loo():
    ds = load_dataset()
    te = H2OTargetEncoderEstimator(noise=0, data_leakage_handling="leave_one_out")
    te.train(y=ds.target, training_frame=ds.train)
    encoded = te.transform(ds.train, as_training=True)
    print(encoded)
    # col_te_golden = [0.18902, 0.1875, 0.1875, 0.73107, 0.1875]
    # col_te = encoded['sex_te'].head(5).as_data_frame().values.reshape(-1).tolist()
    # assert_allclose(col_te, col_te_golden, atol=1e-5)
    
    # with open("./golden/multinomial_loo.csv", "w") as f:
    #     f.write(encoded.get_frame_data())
    # golden = h2o.import_file("./golden/multinomial_loo.csv")
    # assert pu.compare_frames(golden, encoded, 0, tol_numeric=1e-5)


pu.run_tests([
    # test_multinomial_with_none,
    # test_multinomial_with_kfold,
    # test_multinomial_with_loo,
])
