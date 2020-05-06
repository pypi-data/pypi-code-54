
# Term regex assignment module
R, I, L = r'[0-9./]+', r'(\[[0-9-+]+\])√[-+]?[0-9./]+', r'([a-z](\^[()0-9\-+/*])?)+'

tr_1a = R + I + L
tr_1b = R + L + I
tr_1c = I + L + R
tr_1d = I + R + L
tr_1e = L + R + I
tr_1f = L + I + R
TR_1 = r'|'.join([tr_1a, tr_1b, tr_1c, tr_1d, tr_1e, tr_1f])

tr_2a, tr_2b = R + L, L + R
tr_3a, tr_3b = I + L, I + L
tr_4a, tr_4b = R + I, I + R
TR_2 = r'|'.join([tr_2a, tr_2b, tr_3a, tr_3b, tr_4a, tr_4b])

tr_5 = R
tr_6 = I
tr_7 = L
TR_3 = r'|'.join([tr_5, tr_6, tr_7])

TR = r'|'.join([TR_1, TR_2, TR_3])
