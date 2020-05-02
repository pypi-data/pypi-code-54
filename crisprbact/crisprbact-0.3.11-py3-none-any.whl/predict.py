import numpy as np
import re
from importlib.resources import open_binary
from crisprbact.utils import rev_comp, NoRecordsException
from crisprbact.off_target import (
    compute_off_target_df,
    extract_records,
    extract_features,
)

with open_binary("crisprbact", "reg_coef.pkl") as handle:
    coef = np.load(handle, allow_pickle=True)

bases = ["A", "T", "G", "C"]
GUIDE_LEN = 20


def encode(seq):
    """One-hot encoding of a sequence (only non-ambiguous bases (ATGC) accepted)"""

    return np.array([[int(b == p) for b in seq] for p in bases])


# Quartiles: q1 > 0.4 > q2 > -0.08 > q3 > -0.59 > q4
def predict(X):
    return [np.sum(x * coef) for x in X]


def find_targets(seq):
    repam = "[ATGC]GG"
    L = len(seq)
    seq_revcomp = rev_comp(seq)
    matching_targets = re.finditer(
        "(?=([ATGC]{6}" + repam + "[ATGC]{16}))", seq_revcomp
    )
    for target in matching_targets:
        matching_target = target.group(1)
        start, end = target.span(1)
        start_min = 14
        if start >= start_min:
            guide_start = start - start_min
            guide_end = end - 16 - 3
            guide = seq_revcomp[guide_start:guide_end]
            assert len(guide) == GUIDE_LEN
            pos_seq_start = L - guide_end
            pos_seq_stop = L - guide_start
            pos_seq_pam = pos_seq_start - 3
            yield dict(
                [
                    ("target", matching_target),
                    ("guide", guide),
                    ("start", pos_seq_start),
                    ("stop", pos_seq_stop),
                    ("pam", pos_seq_pam),
                    ("ori", "-"),
                ]
            )


def get_strand_value(value):
    strand_dict = {"+": 1, "1": 1, "-": -1, "-1": -1}
    return strand_dict[str(value)]


def on_target_predict(seq, genome=None, seed_sizes=[8, 9, 10, 11, 12, GUIDE_LEN]):

    seq = seq.upper()  # make uppercase
    seq = re.sub(r"\s", "", seq)  # removes white space
    records = None
    genome_features = None

    if genome:
        records = extract_records(genome)
        if records is None:
            raise NoRecordsException(
                "No records found in sequence file. Check the sequence or the format"
            )
        else:
            genome_features = extract_features(records)
    alltargets = list(find_targets(seq))
    if alltargets:
        gen_targets = (target["target"] for target in alltargets)
        gen_clean_targets = remove_GG_of_PAM(gen_targets)
        X = reshape_targets(gen_clean_targets)
        preds = predict(X)
        for i, target in enumerate(alltargets):
            target_id = i + 1
            target.update({"target_id": target_id})
            target.update({"pred": preds[i]})
            if genome:
                # lookup for off-targets in genome
                off_targets_per_seed = list(
                    gen_off_target_per_seed_size(
                        i,
                        target["guide"],
                        records,
                        genome_features,
                        target_id,
                        seed_sizes,
                    )
                )
                target.update({"off_targets_per_seed": list(off_targets_per_seed)})
            else:
                target.update({"off_targets_per_seed": []})
        return alltargets
    else:
        return []


def remove_GG_of_PAM(targets):
    for target in targets:
        yield target[:7] + target[9:]


def reshape_targets(targets):
    X = np.array([encode(target) for target in targets])  # encode and remove GG of PAM
    return X.reshape(X.shape[0], -1)


def slice_off_targets_results(off_target_df):
    return off_target_df.loc[
        0:,
        [
            "start",
            "end",
            "pampos",
            "strand",
            "recid",
            "longest_perfect_match",
            "pam_seq",
            "features",
        ],
    ].values.tolist()


def is_good_orientation(feat, off_target_strand):
    if get_strand_value(off_target_strand) != get_strand_value(feat.location.strand):
        return True
    else:
        return False


def get_off_target_feature(feat):

    feature_dict = {
        "off_target_feat_strand": feat.location.strand,
        "off_target_feat_start": feat.location.start,
        "off_target_feat_end": feat.location.end,
        "off_target_feat_type": feat.type,
    }
    for k, feat in feat.qualifiers.items():
        if k != "translation":
            feature_dict["off_target_" + k] = "::".join(feat)
    return feature_dict


def gen_off_target_per_seed_size(
    index, guide, records, genome_features, target_id, seed_sizes
):
    for seed_size in seed_sizes:
        # off-target found for a guide
        off_target_df = compute_off_target_df(
            guide, seed_size, records, genome_features
        )
        if off_target_df is not None and not off_target_df.empty:
            off_targets = slice_off_targets_results(off_target_df)
            off_targets_list = list(
                gen_off_targets_dict_list(target_id, seed_size, off_targets)
            )
            yield {
                "id": str(index) + "-" + str(seed_size),
                "seed_size": seed_size,
                "off_targets": off_targets_list,
            }
        else:
            yield {
                "id": str(index) + "-" + str(seed_size),
                "seed_size": seed_size,
                "off_targets": [],
            }


def gen_off_targets_dict_list(target_id, seed_size, off_targets):
    for j, off_t in enumerate(off_targets):
        off_target_dict = {
            "off_target_id": str(target_id) + "-" + str(seed_size) + "-" + str(j),
            "off_target_start": off_t[0],
            "off_target_end": off_t[1],
            "off_target_pampos": off_t[2],
            "off_target_strand": off_t[3],
            "off_target_recid": off_t[4],
            "off_target_longest_perfect_match": off_t[5],
            "off_target_pam_seq": off_t[6],
            "off_target_good_orientation": None,
        }
        if (
            seed_size == GUIDE_LEN
            or len(off_target_dict["off_target_longest_perfect_match"]) != GUIDE_LEN
        ):
            index_features = 7
            # Get feature details associated
            # to an off-target position
            if len(off_t[index_features]) > 0:
                feat = off_t[index_features][0]
                off_target_dict["off_target_good_orientation"] = is_good_orientation(
                    feat, off_target_dict["off_target_strand"]
                )
                off_target_feature = get_off_target_feature(feat)
                yield {**off_target_feature, **off_target_dict}
            else:
                yield off_target_dict
