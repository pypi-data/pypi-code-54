# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

from ..compat import DTYPE

__all__ = [
    'load_ausbeer'
]


def load_ausbeer(as_series=False, dtype=DTYPE):
    """Quarterly beer production data.

    Total quarterly beer production in Australia (in megalitres)
    from 1956:Q1 to 2008:Q3

    Parameters
    ----------
    as_series : bool, optional (default=False)
        Whether to return a Pandas series. If False, will return a 1d
        numpy array.

    dtype : type, optional (default=np.float64)
        The type to return for the array. Default is np.float64, which is used
        throughout the package as the default type.

    Returns
    -------
    rslt : array-like, shape=(n_samples,)
        The ausbeer vector.

    Examples
    --------
    >>> from pmdarima.datasets import load_ausbeer
    >>> load_ausbeer()
    array([284., 213., 227., 308., 262., 228., 236., 320., 272., 233., 237.,
           313., 261., 227., 250., 314., 286., 227., 260., 311., 295., 233.,
           257., 339., 279., 250., 270., 346., 294., 255., 278., 363., 313.,
           273., 300., 370., 331., 288., 306., 386., 335., 288., 308., 402.,
           353., 316., 325., 405., 393., 319., 327., 442., 383., 332., 361.,
           446., 387., 357., 374., 466., 410., 370., 379., 487., 419., 378.,
           393., 506., 458., 387., 427., 565., 465., 445., 450., 556., 500.,
           452., 435., 554., 510., 433., 453., 548., 486., 453., 457., 566.,
           515., 464., 431., 588., 503., 443., 448., 555., 513., 427., 473.,
           526., 548., 440., 469., 575., 493., 433., 480., 576., 475., 405.,
           435., 535., 453., 430., 417., 552., 464., 417., 423., 554., 459.,
           428., 429., 534., 481., 416., 440., 538., 474., 440., 447., 598.,
           467., 439., 446., 567., 485., 441., 429., 599., 464., 424., 436.,
           574., 443., 410., 420., 532., 433., 421., 410., 512., 449., 381.,
           423., 531., 426., 408., 416., 520., 409., 398., 398., 507., 432.,
           398., 406., 526., 428., 397., 403., 517., 435., 383., 424., 521.,
           421., 402., 414., 500., 451., 380., 416., 492., 428., 408., 406.,
           506., 435., 380., 421., 490., 435., 390., 412., 454., 416., 403.,
           408., 482., 438., 386., 405., 491., 427., 383., 394., 473., 420.,
           390., 410.,  nan])

    >>> load_ausbeer(True).head()
    0    284.0
    1    213.0
    2    227.0
    3    308.0
    4    262.0
    dtype: float64

    Notes
    -----
    This is quarterly data, so *m* should be set to 4 when using in a seasonal
    context.

    References
    ----------
    .. [1] https://www.rdocumentation.org/packages/fpp/versions/0.5/topics/ausbeer
    """  # noqa: E501
    rslt = np.array([284., 213., 227., 308.,
                     262., 228., 236., 320.,
                     272., 233., 237., 313.,
                     261., 227., 250., 314.,
                     286., 227., 260., 311.,
                     295., 233., 257., 339.,
                     279., 250., 270., 346.,
                     294., 255., 278., 363.,
                     313., 273., 300., 370.,
                     331., 288., 306., 386.,
                     335., 288., 308., 402.,
                     353., 316., 325., 405.,
                     393., 319., 327., 442.,
                     383., 332., 361., 446.,
                     387., 357., 374., 466.,
                     410., 370., 379., 487.,
                     419., 378., 393., 506.,
                     458., 387., 427., 565.,
                     465., 445., 450., 556.,
                     500., 452., 435., 554.,
                     510., 433., 453., 548.,
                     486., 453., 457., 566.,
                     515., 464., 431., 588.,
                     503., 443., 448., 555.,
                     513., 427., 473., 526.,
                     548., 440., 469., 575.,
                     493., 433., 480., 576.,
                     475., 405., 435., 535.,
                     453., 430., 417., 552.,
                     464., 417., 423., 554.,
                     459., 428., 429., 534.,
                     481., 416., 440., 538.,
                     474., 440., 447., 598.,
                     467., 439., 446., 567.,
                     485., 441., 429., 599.,
                     464., 424., 436., 574.,
                     443., 410., 420., 532.,
                     433., 421., 410., 512.,
                     449., 381., 423., 531.,
                     426., 408., 416., 520.,
                     409., 398., 398., 507.,
                     432., 398., 406., 526.,
                     428., 397., 403., 517.,
                     435., 383., 424., 521.,
                     421., 402., 414., 500.,
                     451., 380., 416., 492.,
                     428., 408., 406., 506.,
                     435., 380., 421., 490.,
                     435., 390., 412., 454.,
                     416., 403., 408., 482.,
                     438., 386., 405., 491.,
                     427., 383., 394., 473.,
                     420., 390., 410., None]).astype(dtype)

    if as_series:
        return pd.Series(rslt)
    return rslt
