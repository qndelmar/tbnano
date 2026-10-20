import os
from pathlib import Path

BASE = Path(os.environ.get("TBNANO_TASK_DIR", "/task"))
EXPECTED = 't,alt,v\n23,936,793\n38,915,302\n40,106,99\n59,857,440\n106,761,976\n125,174,17\n138,44,24\n140,207,325\n152,77,503\n156,191,851\n166,259,647\n186,509,55\n194,587,578\n195,959,668\n222,527,972\n255,403,954\n334,230,951\n393,0,966\n419,429,660\n434,476,528\n497,982,333\n512,457,870\n557,905,193\n667,942,26\n678,110,577\n769,2,371\n824,955,838\n828,73,956\n842,515,93\n843,306,331\n856,496,167\n879,442,663\n903,233,376\n982,26,512\n984,512,265\n'

def test_merged():
    p = BASE / "merged.csv"
    assert p.exists(), "merged.csv missing"
    assert p.read_text() == EXPECTED
