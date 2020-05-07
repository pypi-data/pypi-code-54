import sys
import logging
import pathlib
import numpy as np
import pylab as pl
from typing import Union, List, Iterable
from .molecule import IPMolecule
from .mzml import mzML
from .scripttime import ScriptTime
from .spectrum import Spectrum
from .tome import check_integer, bindata, slice_array
from .xlsx import XLSX


logger = logging.getLogger(__name__)


class BoundsError(Warning):
    """A warning class to handle bounds errors when integrating (used only by PyRSIR)"""

    def __init__(self):
        self.warned = {}

    def printwarns(self):
        """
        Prints a summary of all warnings for

        :return:
        """
        """prints the number of warnings if merited"""
        if len(self.warned) > 0:
            logger.warning(
                'The following peaks exceeded the bounds of the spectrum n number of times:\n'
                f'{", ".join([f"{name}: {self.warned[name]}" for name in self.warned])}'
            )

    def warn(self, name, intstart, intend, mzstart, mzend):
        """
        Emits a warning if the integration was outside of the bounds of the spectrum.

        :param name: name of the peak
        :param intstart: integration start value
        :param intend: integration end value
        :param mzstart: m/z start value
        :param mzend: m/z end value
        """
        if name not in self.warned:
            logger.warning(
                f'The peak "{name}" ({intstart}-{intend}) is outside of the bounds of the spectrum being summed '
                f'm/z {mzstart:.1f}-{mzend:.1f}\n'
            )
            self.warned[name] = 1
        else:
            self.warned[name] += 1


class RSIRTarget:
    # precision to use for sumspectrum
    SPECTRUM_PRECISION = 3

    def __init__(self,
                 formula: Union[IPMolecule, str],
                 bounds: List[float] = None,
                 affinity: str = '+',
                 function: int = 1,
                 store_spectra: bool = False,
                 name: str = None,
                 ):
        """
        Data class for RSIR data

        :param formula: molecular formula (or IPMolecule instance)
        :param bounds: manually specified bounds
        :param affinity: MS mode affinity (+ or -)
        :param function: MS function to find the data in
        :param store_spectra: flag to enable spectral storage if desired. If enabled, creates a Spectrum object
            associated with the instance.
        :param name: species name
        """
        # todo support manually specified resolution
        self._molecule: IPMolecule = None
        self._bounds = None
        self._affinity = None
        self._name = None
        # bounds error counter
        self._bounds_warnings = 0

        self.name = name
        self.formula = formula
        self.bounds = bounds
        self.affinity = affinity
        self.function = function

        # storage container for raw data
        self.raw_data = []

        # spectrum storage
        if store_spectra is True:
            self.spectrum = Spectrum(self.SPECTRUM_PRECISION)
        else:
            self.spectrum = None

    def __str__(self):
        return f'{self.__class__.__name__} {self.name}'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name})'

    @property
    def name(self) -> str:
        """species name"""
        if self._name is not None:
            return self._name
        elif self._molecule is not None:
            return self._molecule.molecular_formula
        elif self._bounds is not None:
            out = f'm/z {self._bounds[0]:.1f}'
            if self._bounds[1] is not None:
                out += f' - {self._bounds[1]:.1f}'
            return out
        return 'unnamed'

    @name.setter
    def name(self, value: str):
        self._name = value

    @name.deleter
    def name(self):
        self.name = None

    @property
    def formula(self) -> IPMolecule:
        """molecule object to reference"""
        return self._molecule

    @formula.setter
    def formula(self, value: Union[IPMolecule, str]):
        if value is None:
            self._molecule = None
        self._molecule = IPMolecule(value)

    @formula.deleter
    def formula(self):
        self._molecule = None

    @property
    def bounds(self) -> List[float]:
        """m/z bounds to use for intensity tracking"""
        # return manually set bounds if specified
        if self._bounds is not None:
            return self._bounds
        # or determined bounds from molecule class
        elif self._molecule is not None:
            return self._molecule.bounds
        else:
            raise AttributeError(f'Bounds have not been set for this instance')

    @bounds.setter
    def bounds(self, value: List[float]):
        if value is None:
            self._bounds = None
            return
        # if a single value was specified
        if len(value) != 2:
            raise ValueError('current functionality requires bounds to be fully specified')
            # todo enable ability to just specify single m/z
            value = [value, None]
        # if two values were specified, check range
        elif value[0] > value[1]:
            raise ValueError('the start m/z must be less than the end m/z')
        self._bounds = value

    @bounds.deleter
    def bounds(self):
        self.bounds = None

    @property
    def bounds_warnings(self) -> int:
        """count of the number of bounds warnings during processing"""
        return self._bounds_warnings

    @property
    def affinity(self) -> str:
        """MS type affinity (+/-/UV)"""
        return self._affinity

    @affinity.setter
    def affinity(self, value: str):
        if value not in ['+', '-', 'UV']:
            raise ValueError(f'the provided value "{value}" is not a valid affinity (+, -, or UV)')
        self._affinity = value

    def pull_from_mzml(self, mzml: mzML):
        """
        Retrieves corresponding data from an mzML file. The instance will automatically associate itself with the
        appropriate mzML function.

        :param mzml: mzML instance
        """
        pass

    def add_from_spectrum(self, x: Union[np.ndarray, List[float]], y: Union[np.ndarray, List[float]]):
        """
        Finds location within the the array and integrates, appending that value to the list of raw data.

        :param x: x array
        :param y: y array
        :return:
        """
        # casting to array is highly inefficient with the current structure but it works
        if isinstance(x, np.ndarray) is False:
            x = np.asarray(x)
        if isinstance(y, np.ndarray) is False:
            y = np.asarray(y)
        # slice array
        self_slice = slice_array(
            y,
            x,
            *self.bounds

        )
        if self.spectrum is not None:
            self.spectrum.add_spectrum(*self_slice)
        intensity = self_slice[1].sum()
        self.raw_data.append(intensity)
        return intensity

# todo
#   - time course class (with function number so that Targets can be associated with time runs)

class PyRSIR:
    def __init__(self,
                 filename: str,
                 xlsx: str,
                 n: Union[int, Iterable[int]],
                 plot: bool = True,
                 bounds_confidence: float = None,
                 combine_spectra: bool = True,
                 ):
        pass

    def prepformula(self, dct):
        """looks for formulas in a dictionary and prepares them for pullspeciesdata"""
        for species in dct:
            if 'affin' not in dct[species]:  # set affinity if not specified
                fn = dct[species]['function']
                if mzml.functions[fn]['type'] == 'MS':
                    dct[species]['affin'] = mzml.functions[fn]['mode']
                if mzml.functions[fn]['type'] == 'UV':
                    dct[species]['affin'] = 'UV'
            if 'formula' in dct[species] and dct[species]['formula'] is not None:
                try:
                    dct[species]['mol'].res = res  # sets resolution in Molecule object
                except NameError:
                    res = int(mzml.auto_resolution())
                    dct[species]['mol'].res = res
                # dct[species]['mol'].sigma = dct[species]['mol'].sigmafwhm()[1]  # recalculates sigma with new resolution
                dct[species]['bounds'] = dct[species]['mol'].bounds  # caclulates bounds
        return dct


def pyrsir(
        filename,
        xlsx,
        n,
        plot=True,  # plot the data for a quick look
        verbose=True,  # chatty
        bounds_confidence=0.99,  #
        combine_spectra=True,  # whether or not to output a summed spectrum
        return_data=False,  #
):
    """
    A method for generating reconstructed single ion monitoring traces.

    :param filename: path to mzML or raw file to process
    :param xlsx: path to excel file with correctly formatted columns
    :param n: number of scans to sum together (for binning algorithm)
    :param plot: whether to plot and show the data for a quick look
    :param verbose: chatty mode
    :param bounds_confidence: confidence interval for automatically generated bounds (only applicable if molecular
        formulas are provided).
    :param combine_spectra: whether to output a summed spectrum
    :param return_data: whether to return data (if the data from the function is required by another function)
    :return:
    """

    def plots():
        """
        Function for generating a set of plots for rapid visual assessment of the supplied n-level
        Outputs all MS species with the same sum level onto the same plot
        requirements: pylab as pl
        """
        pl.clf()  # clears and closes old figure (if still open)
        pl.close()
        nplots = len(n) + 1

        # raw data
        pl.subplot(nplots, 1, 1)  # top plot

        for mode in mskeys:
            modekey = 'raw' + mode
            if modekey in rtime.keys():
                pl.plot(rtime[modekey], tic[modekey], linewidth=0.75, label='TIC')  # plot tic
                for key in sp:  # plot each species
                    if sp[key]['affin'] is mode:
                        pl.plot(rtime[modekey], sp[key]['raw'], linewidth=0.75, label=key)
        pl.title('Raw Data')
        pl.ylabel('Intensity')
        pl.tick_params(axis='x', labelbottom='off')

        # summed data
        loc = 2
        for num in n:
            pl.subplot(nplots, 1, loc)
            sumkey = str(num) + 'sum'
            for mode in mskeys:
                modekey = str(num) + 'sum' + mode
                if modekey in rtime.keys():
                    pl.plot(rtime[modekey], tic[modekey], linewidth=0.75, label='TIC')  # plot tic
                    for key in sp:
                        if sp[key]['affin'] is mode:  # if a MS species
                            pl.plot(rtime[modekey], sp[key][sumkey], linewidth=0.75, label=key)
            pl.title('Summed Data (n=%i)' % (num))
            pl.ylabel('Intensity')
            pl.tick_params(axis='x', labelbottom='off')
            loc += 1
        pl.tick_params(axis='x', labelbottom='on')
        pl.show()

    def output():
        """
        Writes the retrieved and calculated values to the excel workbook using the XLSX object
        """
        if newpeaks is True:  # looks for and deletes any sheets where the data will be changed
            if verbose is True:
                sys.stdout.write('Clearing duplicate XLSX sheets.')
            delete = []
            for key in newsp:  # generate strings to look for in excel file
                delete.append('Raw Data (' + sp[key]['affin'] + ')')
                for num in n:
                    delete.append(str(num) + ' Sum (' + sp[key]['affin'] + ')')
                    delete.append(str(num) + ' Normalized (' + sp[key]['affin'] + ')')
            delete.append('Isotope Patterns')
            xlfile.removesheets(delete)  # remove those sheets
            if verbose is True:
                sys.stdout.write(' DONE.\n')

        if verbose is True:
            sys.stdout.write('Writing to "%s"' % xlfile.bookname)
            sys.stdout.flush()

        for mode in mskeys:  # write raw data to sheets
            modekey = 'raw' + mode
            if modekey in rtime.keys():
                sheetname = 'Raw Data (' + mode + ')'
                xlfile.writersim(sp, rtime[modekey], 'raw', sheetname, mode, tic[modekey])

        for num in n:  # write summed and normalized data to sheets
            sumkey = str(num) + 'sum'
            normkey = str(num) + 'norm'
            for mode in mskeys:
                modekey = 'raw' + mode
                if modekey in rtime.keys():
                    if max(n) > 1:  # if data were summed
                        sheetname = str(num) + ' Sum (' + mode + ')'
                        xlfile.writersim(sp, rtime[sumkey + mode], sumkey, sheetname, mode,
                                         tic[sumkey + mode])  # write summed data
                    sheetname = str(num) + ' Normalized (' + mode + ')'
                    xlfile.writersim(sp, rtime[sumkey + mode], normkey, sheetname, mode)  # write normalized data

        for key in sorted(sp.keys(), key=lambda x: str(x)):  # write isotope patterns
            if sp[key]['affin'] in mskeys:
                xlfile.writemultispectrum(
                    sp[key]['spectrum'][0],  # x values
                    sp[key]['spectrum'][1],  # y values
                    key,  # name of the spectrum
                    xunit='m/z',  # x unit
                    yunit='Intensity (counts)',  # y unit
                    sheetname='Isotope Patterns',  # sheet name
                    chart=True,  # output excel chart
                )

        if rd is None:
            for key, val in sorted(chroms.items()):  # write chromatograms
                xlfile.writemultispectrum(chroms[key]['x'], chroms[key]['y'], chroms[key]['xunit'],
                                          chroms[key]['yunit'], 'Function Chromatograms', key)

        uvstuff = False
        for key in sp:  # check for UV-Vis spectra
            if sp[key]['affin'] is 'UV':
                uvstuff = True
                break
        if uvstuff is True:
            for ind, val in enumerate(tic['rawUV']):  # normalize the UV intensities
                tic['rawUV'][ind] = val / 1000000.
            xlfile.writersim(sp, rtime['rawUV'], 'raw', 'UV-Vis', 'UV', tic['rawUV'])  # write UV-Vis data to sheet

        if sum_spectra is not None:  # write all summed spectra
            for fn in sum_spectra:
                specname = '%s %s' % (mzml.functions[fn]['mode'], mzml.functions[fn]['level'])
                if 'target' in mzml.functions[fn]:
                    specname += ' %.3f' % mzml.functions[fn]['target']
                specname += ' (%.3f-%.3f)' % (mzml.functions[fn]['window'][0], mzml.functions[fn]['window'][1])
                xlfile.writemultispectrum(
                    sum_spectra[fn][0],  # x values
                    sum_spectra[fn][1],  # y values
                    specname,  # name of the spectrum
                    xunit='m/z',  # x unit
                    yunit='Intensity (counts)',  # y unit
                    sheetname='Summed Spectra',  # sheet name
                    chart=True,  # output excel chart
                )

        if verbose is True:
            sys.stdout.write(' DONE\n')

    def prepformula(dct):
        """looks for formulas in a dictionary and prepares them for pullspeciesdata"""
        for species in dct:
            if 'affin' not in dct[species]:  # set affinity if not specified
                fn = dct[species]['function']
                if mzml.functions[fn]['type'] == 'MS':
                    dct[species]['affin'] = mzml.functions[fn]['mode']
                if mzml.functions[fn]['type'] == 'UV':
                    dct[species]['affin'] = 'UV'
            if 'formula' in dct[species] and dct[species]['formula'] is not None:
                try:
                    dct[species]['mol'].res = res  # sets resolution in Molecule object
                except NameError:
                    res = int(mzml.auto_resolution())
                    dct[species]['mol'].res = res
                # dct[species]['mol'].sigma = dct[species]['mol'].sigmafwhm()[1]  # recalculates sigma with new resolution
                dct[species]['bounds'] = dct[species]['mol'].bounds  # caclulates bounds
        return dct

    # ----------------------------------------------------------
    # -------------------PROGRAM BEGINS-------------------------
    # ----------------------------------------------------------

    if verbose is True:
        stime = ScriptTime()
        stime.printstart()

    n = check_integer(n, 'number of scans to sum')  # checks integer input and converts to list

    if type(xlsx) != dict:
        if verbose is True:
            sys.stdout.write('Loading processing parameters from excel file')
            sys.stdout.flush()
        xlfile = XLSX(xlsx, verbose=verbose)
        sp = xlfile.pullrsimparams()
    else:  # if parameters were provided in place of an excel file
        sp = xlsx

    mskeys = ['+', '-']
    for key in sp:
        if 'formula' in sp[key] and sp[key]['formula'] is not None:  # if formula is specified
            sp[key]['mol'] = IPMolecule(sp[key]['formula'])  # create Molecule object
            sp[key]['bounds'] = sp[key]['mol'].calculate_bounds(
                bounds_confidence
            )  # generate bounds from molecule object with this confidence interval
    if verbose is True:
        sys.stdout.write(' DONE\n')

    rtime = {}  # empty dictionaries for time and tic
    tic = {}
    rd = False
    for mode in mskeys:  # look for existing positive and negative mode raw data
        try:
            modedata, modetime, modetic = xlfile.pullrsim('Raw Data (' + mode + ')')
        except KeyError:
            continue
        except UnboundLocalError:  # catch for if pyrsir was not handed an excel file
            continue
        if verbose is True:
            sys.stdout.write('Existing (%s) mode raw data were found, grabbing those values.' % mode)
            sys.stdout.flush()
        rd = True  # bool that rd is present
        modekey = 'raw' + mode
        sp.update(modedata)  # update sp dictionary with raw data
        for key in modedata:  # check for affinities
            if 'affin' not in sp[key]:
                sp[key]['affin'] = mode
        rtime[modekey] = list(modetime)  # update time list
        tic[modekey] = list(modetic)  # update tic list
        if verbose is True:
            sys.stdout.write(' DONE\n')

    # sp = prepformula(sp)
    newpeaks = False
    if rd is True:
        newsp = {}
        sum_spectra = None
        for key in sp:  # checks whether there is a MS species that does not have raw data
            if 'raw' not in sp[key]:
                newsp[key] = sp[key]  # create references in the namespace
        if len(newsp) is not 0:
            newpeaks = True
            if verbose is True:
                sys.stdout.write('Some peaks are not in the raw data, extracting these from raw file.\n')
            ips = xlfile.pullmultispectrum(
                'Isotope Patterns')  # pull predefined isotope patterns and add them to species
            for species in ips:  # set spectrum list
                sp[species]['spectrum'] = [ips[species]['x'], ips[species]['y']]
            mzml = mzML(filename)  # load mzML class
            sp = prepformula(sp)  # prep formula etc for summing
            newsp = prepformula(newsp)  # prep formula species for summing
            for species in newsp:
                if 'spectrum' not in newsp[species]:
                    newsp[species]['spectrum'] = Spectrum(3, newsp[species]['bounds'][0], newsp[species]['bounds'][1])
            newsp = mzml.pull_species_data(newsp)  # pull data
        else:
            if verbose is True:
                sys.stdout.write('No new peaks were specified. Proceeding directly to summing and normalization.\n')

    if rd is False:  # if no raw data is present, process mzML file
        mzml = mzML(filename, verbose=verbose)  # load mzML class
        sp = prepformula(sp)
        sp, sum_spectra = mzml.pull_species_data(sp, combine_spectra)  # pull relevant data from mzML
        chroms = mzml.pull_chromatograms()  # pull chromatograms from mzML
        rtime = {}
        tic = {}
        for key in sp:  # compare predicted isotope patterns to the real spectrum and save standard error of the regression
            func = sp[key]['function']
            if mzml.functions[func]['type'] == 'MS':  # determine mode key
                if combine_spectra is True:
                    sp[key]['spectrum'] = sum_spectra[sp[key]['function']].trim(
                        xbounds=sp[key]['bounds'])  # extract the spectrum object
                mode = 'raw' + mzml.functions[func]['mode']
            if mzml.functions[func]['type'] == 'UV':
                mode = 'rawUV'
            if mode not in rtime:  # if rtime and tic have not been pulled from that function
                rtime[mode] = mzml.functions[func]['timepoints']
                tic[mode] = mzml.functions[func]['tic']
            # if 'formula' in sp[key] and sp[key]['formula'] is not None:
            #     sp[key]['match'] = sp[key]['mol'].compare(sp[key]['spectrum'])
        if combine_spectra is True:
            for fn in sum_spectra:
                sum_spectra[fn] = sum_spectra[fn].trim()  # convert Spectrum objects into x,y lists

    # if max(n) > 1: # run combine functions if n > 1
    for num in n:  # for each n to sum
        if verbose is True:
            sys.stdout.write('\r%d Summing species traces.' % num)
        sumkey = str(num) + 'sum'
        for key in sp:  # bin each species
            if sp[key]['affin'] in mskeys or mzml.functions[sp[key]['function']][
                'type'] == 'MS':  # if species is MS related
                sp[key][sumkey] = bindata(num, sp[key]['raw'])
        for mode in mskeys:
            sumkey = str(num) + 'sum' + mode
            modekey = 'raw' + mode
            if modekey in rtime.keys():  # if there is data for that mode
                rtime[sumkey] = bindata(num, rtime[modekey], num)
                tic[sumkey] = bindata(num, tic[modekey])
    if verbose is True:
        sys.stdout.write(' DONE\n')
        sys.stdout.flush()
    # else:
    #    for key in sp: # create key for normalization
    #        sp[key]['1sum'] = sp[key]['raw']

    for num in n:  # normalize each peak's chromatogram
        if verbose is True:
            sys.stdout.write('\r%d Normalizing species traces.' % num)
            sys.stdout.flush()
        sumkey = str(num) + 'sum'
        normkey = str(num) + 'norm'
        for mode in mskeys:
            modekey = 'raw' + mode
            if modekey in rtime.keys():  # if there is data for that mode
                for key in sp:  # for each species
                    if sp[key]['affin'] in mskeys or mzml.functions[sp[key]['function']][
                        'type'] == 'MS':  # if species has affinity
                        sp[key][normkey] = []
                        for ind, val in enumerate(sp[key][sumkey]):
                            # sp[key][normkey].append(val/(mzml.function[func]['tic'][ind]+0.01)) #+0.01 to avoid div/0 errors
                            sp[key][normkey].append(
                                val / (tic[sumkey + sp[key]['affin']][ind] + 0.01))  # +0.01 to avoid div/0 errors
    if verbose is True:
        sys.stdout.write(' DONE\n')

    if return_data is True:  # if data is to be used by another function, return the calculated data
        return mzml, sp, rtime, tic, chroms

    # import pickle #pickle objects (for troubleshooting)
    # pickle.dump(rtime,open("rtime.p","wb"))
    # pickle.dump(tic,open("tic.p","wb"))
    # pickle.dump(chroms,open("chroms.p","wb"))
    # pickle.dump(sp,open("sp.p","wb"))

    output()  # write data to excel file

    if verbose is True:
        sys.stdout.write('\rUpdating paramters')
        sys.stdout.flush()
    xlfile.updatersimparams(sp)  # update summing parameters
    if verbose is True:
        sys.stdout.write(' DONE\n')

    if verbose is True:
        sys.stdout.write('\rSaving "%s" (this may take some time)' % xlfile.bookname)
        sys.stdout.flush()
    xlfile.save()
    if verbose is True:
        sys.stdout.write(' DONE\n')

    if verbose is True:
        if verbose is True:
            sys.stdout.write('Plotting traces')
        if plot is True:
            plots()  # plots for quick review
        if verbose is True:
            sys.stdout.write(' DONE\n')
    if verbose is True:
        stime.printelapsed()
