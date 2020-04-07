""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import numpy as np

# format string to unpack BFHs in one go
BFHFS = 'iiihhhhhhhhhhhhhhhhhhhhhhhhiiiQQiii' + 'i' * 50 + 'BBhhihQQi' + 'i' * 17

# keys for BFH dictionary
BFHCOLS = ['job_id',
           'line_no',
           'reel_no',
           'traces_per_ensemble',
           'aux_traces_per_ensemble',
           'sample_interval',
           'sample_interval_orig',
           'samples_per_trace',
           'samples_per_trace_orig',
           'sample_format',
           'ensemble_fold',
           'trace_sorting',
           'vertical_sum',
           'sweep_freq_start',
           'sweep_freq_end',
           'sweep_length',
           'sweep_type',
           'sweep_channel',
           'sweep_taper_start',
           'sweep_taper_end',
           'taper_type',
           'correlated_flag',
           'binary_gain_recovery_flag',
           'amp_recovery_method',
           'measurement_system',  # 1 for meters, 2 for feet
           'impulse_polarity',
           'vibratory_polarity',
           'ext_traces_per_ensemble',
           'ext_aux_traces_per_ensemble',
           'ext_samples_per_trace',
           'ext_sample_interval',
           'ext_sample_interval_orig',
           'ext_samples_per_trace_orig',
           'ext_ensemble_fold',
           'integer_constant']
BFHCOLS += [f'unassigned_{i}' for i in range(1, 51)]
BFHCOLS += ['segy_revision_major',
            'segy_revision_minor',
            'fixed_trace_length_flag',
            'no_ext_tfhs',
            'no_additional_trace_headers',
            'time_basis',
            'no_traces',
            'byte_offset_of_data',
            'no_trailer_stanzas']
BFHCOLS += [f'unassigned_{i}' for i in range(51, 68)]

# sample format code dictionary. maps codes to (size, format letter, description)
SFC = {
    1: (4, None, '4-byte IBM floating-point'),
    2: (4, 'i', '4-byte signed integer'),
    3: (2, 'h', '2-byte signed integer'),
    5: (4, 'f', '4-byte IEEE floating-point'),
    6: (4, 'd', '8-byte IEEE floating-point'),
    8: (1, 'b', '1-byte signed integer'),
    9: (8, 'q', '8-byte signed integer'),
    10: (4, 'L', '4-byte, unsigned integer'),
    11: (2, 'H', '2-byte, unsigned integer'),
    12: (8, 'Q', '8-byte, unsigned integer'),
    16: (1, 'B', '1-byte, unsigned integer')
}

# format string to unpack trace headers in one go. after these 232 bytes go 8 bytes of text
THFS = 'iiiiiiihhhhiiiiiiiihhiiiihhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhiiiiihhihhhhhhhhihh'

# columns for Geometry DataFrame
THCOLS = ['TRACENO',  # ordinal number of a trace
          'fTRACENO',
          'FFID',  # unique number of a shot
          'CHAN',  # channel number
          'SOURCE',  # number of a source point
          'CDP',  # number of a common depth point
          'SEQNO',  # ordinal number of a trace in the ensemble
          'TRC_TYPE',  # ID code for a trace
          'STACKCNT',  # number of vertically stacked traces
          'TRFOLD',  # number of horizontally stacked traces
          'Data Use',
          'OFFSET',  # offset - distance between the source and the receiver
          'REC_ELEV',  # receiver elevation
          'SOU_ELEV',  # source elevation
          'DEPTH',  # source depth from the surface
          'REC_DATUM',  # elevation of the datum at the receiver
          'SOU_DATUM',  # elevation of the datum at the source
          'SOU_H2OD',  # water depth at the source
          'REC_H2OD',  # water depth at the receiver
          'ELEVSC',  # scalar to apply to the elevations
          'COORDSC',  # scalar to apply to the coordinates
          'SOU_X',
          'SOU_Y',
          'REC_X',
          'REC_Y',
          'Coordinate Units',
          'Weathering Velocity',
          'Subweathering Velocity',
          'UPHOLE',  # vertical time at the source, ms
          'REC_UPHOLE',  # vertical time at the receiver, ms
          'SOU_STAT',  # a static correction at the source, ms
          'REC_STAT',  # a static correction at the receiver, ms
          'TOT_STAT',  # total static correction, ms
          'Lag Time A',
          'Lag Time B',
          'Delay Recording Time',
          'TLIVE_S',  # starting time of muting, ms
          'TFULL_S',  # ending time of muting, ms
          'NUMSMP',  # number of samples in a trace (RadExPro needs this!)
          'DT',  # sample interval in microseconds (RadExPro needs this!)
          'IGAIN',  # code of the gain type of the instrument
          'PREAMP',  # amplification coefficient for instrument, dB
          'EARLYG',  # initial amplification of the instrument, dB
          'COR_FLAG',  # correlation flag (1 - no, 2 - yes)
          'SWEEPFREQSTART',  # starting frequency of the sweep, Hz
          'SWEEPFREQEND',  # ending frequency of the sweep, Hz
          'SWEEPLEN',  # length of the sweep, ms
          'SWEEPTYPE',  # code for the sweep type
          'Sweep Taper (start)',
          'Sweep Taper (end)',
          'Taper Type',
          'AAXFILT',  # frequency of the anti-aliasing filter, Hz
          'AAXSLOP',  # slope of the anti-aliasing filter, dB / oct
          'FREQXN',  # frequency of the reject filter, Hz
          'FXNSLOP',  # slope of the reject filter, dB / oct
          'FREQXL',  # low-cut frequency, Hz
          'FREQXH',  # high-cut frequency, Hz
          'FXLSLOP',  # low-cut slope, dB / oct
          'FXHSLOP',  # high-cut slope, dB / oct
          'YEAR',
          'DAY',
          'HOUR',
          'MINUTE',
          'SECOND',
          'Time Basis',
          'Weighting Factor',
          'Group No. of Roll Switch',
          'Group No. of First Trace',
          'Group No. of Last Trace',
          'Gap Size',
          'Over Travel',
          'CDP_X',
          'CDP_Y',
          'In-line No.',
          'Cross-line No.',
          'Shotpoint Number',
          'Shotpoint Scalar',
          'Trace Measurement Unit',
          'Transduction Constant (mantissa)',
          'Transduction Constant (10 power exponent)',
          'Transduction Units',
          'Device/Trace ID',
          'Times Scalar',
          'Source Type/Orientation',
          'Source Energy Direction (vertical)',
          'Source Energy Direction (cross-line)',
          'Source Energy Direction (in-line)',
          'Source Measurement (mantissa)',
          'Source Measurement (10 power exponent)',
          'Source Measurement Unit']
# then go 8 bytes of text - so called "Header name"

# dictionaries to map sample format code to data matrix dtype
DTYPEMAP = {
    1: np.float32,
    2: np.int32,
    3: np.int16,
    5: np.float32,
    6: np.float64,
    8: np.int8,
    9: np.int64,
    10: np.uint32,
    11: np.uint16
}

IDTYPEMAP = {
    'float32': 5,
    'int32': 2,
    'int16': 3,
    'float64': 6,
    'int8': 8,
    'int64': 9,
    'uint32': 10,
    'uint16': 11
}
