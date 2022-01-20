# [(name, type, required, label, help, special_tags, _)]

_address_g_s_help = 'Should start with <span class="text-monospace">http[s]://...</span> or <span class="text-monospace">mqtt[s]://...</span>'
_path_g_s_help = 'Path to send the <span class="text-monospace">POST</span> request to, or in case of MQTT broker topic.'

_address_gf_s_help = 'Should start with <span class="text-monospace">http[s]://...</span>'
_path_gf_s_help = 'Path to send the <span class="text-monospace">POST</span> request to'

GENERATOR_GETTER = ( # type: ignore
    ("url",    "text",     False, "New url",        "URL to get the data from",                       None, []),
    ("path_g", "text",     True,  "New path",       "Path to file on disk or to given json resource", None, []),
    ("json",   "checkbox", False, "Is json?",       "",                                               None, []),
    ("type",   "select",   False, "Type of getter", "",                                 None, ["HTTP", "file"]),
)

GENERATOR_SENDER = ( # type: ignore
    ("address_s", "text", True, "New address", _address_g_s_help, None, []),
    ("path_s",    "text", True, "New path",    _path_g_s_help,    None, []),
)

AGGREGATOR_REMOVE = ( # type: ignore
    ["remove", "select", True, "Remove aggregator", "", None, ["you", "shouldn't", "see", "this", "here"]],
)
AGGREGATOR_ADD = ( # type: ignore
    ("add",  "text",        True, "New aggregator name", '<span class="text-monospace">/&lt;name&gt;/&lt;endpoint&gt;/</span>', None, []),
    ("add_time", "number",  True, "Aggregator timespan", '<span class="text-monospace">>0, integer</span>', 'min="1"',   []),
    ("add_type", "select",  True, "New aggregator type", "",                  None, ["append", "max", "min", "mean", "sum"]),
)

# TODO: add and change are exactly the same, i should merge them

AGGREGATOR_CHANGE = ( # type: ignore
    ["change",  "select", True, "Change aggregator", "Which one?",     None, ["you", "shouldn't", "see", "this", "here"]],
    ("ch_time", "number", True, "Aggregator timespan", '<span class="text-monospace">>0, integer</span>', 'min="1"',  []),
    ("ch_type", "select", True, "Change aggregator type", "",              None, ["append", "max", "min", "mean", "sum"]),
)

FILTER_CHANGE = ( # type: ignore
    ("soft", "checkbox", False, "Soft?",                 "", None,                   []),
    ("path", "text",     True,  "Path to entry in json", "", "class='filter-entry'", [])
)

FILTER_SENDER = ( # type: ignore
    ("address_s", "text", True, "New address", _address_gf_s_help, None, []),
    ("path_s",    "text", True, "New path",    _path_gf_s_help,    None, []),
)

FILTER_GETTER = ( # type: ignore
    ("url", "text", False, "New url", "URL to get the data from", None, []),
)

AGGREGATOR_GRAPH_CHANGE = ( # type: ignore
    ("ch_time",     "number", True, "Aggregator timespan",    '<span class="text-monospace">>0, integer</span>', 'min="1"',  []),
    ("ch_agg_type", "select", True, "Change aggregator type", "",                 None,           ["max", "min", "mean", "sum"]),
    ("ch_gra_type", "select", True, "Change graph type",      "",                 None,                  ["plain", "histogram"]),
)