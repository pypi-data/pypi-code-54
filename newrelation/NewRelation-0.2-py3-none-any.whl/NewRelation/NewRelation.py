import pandas as pd
def word_freq(data, keyword):
    list_freq = []
    for d in data:
        freq_factor = 0
        d_split = d.split()
        count = 0
        SET = set(d_split)
        freq_factor = 10 
        st = len(SET)
        for s in d_split:
            if s == keyword:
                count+=1
            count = count - 0.2 * count
        list_freq.append(count/freq_factor)
    return list_freq
    
def transform(data, fit_dataframe):
    target_keys = fit_dataframe.columns
    df = {}
    for tk in target_keys:
        df[tk] = word_freq([data], tk)
    df = pd.DataFrame(df)
    #return df
    df = pd.DataFrame(df.values*fit_dataframe.values, index = fit_dataframe.index)
    #return df
    df = pd.DataFrame(df.sum(axis = 1, skipna = True), columns=["sum"])
    #return df

    get_max = df.loc[df['sum'].idxmax()]

    if(type(get_max) == pd.core.series.Series):
        return int(get_max.name[1:]), get_max['sum']
    else:
        return list(get_max.index)