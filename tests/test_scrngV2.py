import rqcrypt.scrngV2.scrngV2 as sc


def test_scrngV2():
    nums = sc.random_nums(1, 10, 10, digits=0)
    assert isinstance(nums, list)
