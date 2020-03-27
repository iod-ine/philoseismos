""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

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
