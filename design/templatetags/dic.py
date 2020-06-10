from django import template

register = template.Library()


@register.filter("inverter_id_labeltag")
def inverter_id_labeltag(dict_data, key):
    """
        get inverter_id labeltag from ConfigForm
    """
    if key:
        form = dict_data.get(key)
        return form.__getitem__("inverter_id").label_tag()


@register.filter("inverter_id_value")
def inverter_id_value(dict_data, key):
    """
        get inverter_id value from ConfigForm
    """
    if key:
        form = dict_data.get(key)
        return form.__getitem__("inverter_id")


@register.filter("inverter_quantity_labeltag")
def inverter_quantity_labeltag(dict_data, key):
    """
        get inverter_quantity labeltag from ConfigForm
    """
    if key:
        form = dict_data.get(key)
        return form.__getitem__("inverter_quantity").label_tag()


@register.filter("inverter_quantity_value")
def inverter_quantity_value(dict_data, key):
    """
        get inverter_quantity value from ConfigForm
    """
    if key:
        form = dict_data.get(key)
        return form.__getitem__("inverter_quantity")


@register.filter("inverter_index_value")
def inverter_index_value(dict_data, key):
    """
        get inverter_index value from ConfigForm
    """
    if key:
        form = dict_data.get(key)
        return form.__getitem__("index")


@register.filter("mpp_serial_labeltag")
def mpp_serial_labeltag(dict_data, key):
    """
        get serial labeltag from MPPForm
    """
    if key:
        form = dict_data.get(key)
        return form.__getitem__("serial").label_tag()


@register.filter("mpp_serial_value")
def mpp_serial_value(dict_data, key):
    """
        get serial value from MPPForm
    """
    if key:
        form = dict_data.get(key)
        return form.__getitem__("serial")


@register.filter("mpp_parallel_labeltag")
def mpp_parallel_labeltag(dict_data, key):
    """
        get parallel labeltag from MPPForm
    """
    if key:
        form = dict_data.get(key)
        return form.__getitem__("parallel").label_tag()


@register.filter("mpp_parallel_value")
def mpp_parallel_value(dict_data, key):
    """
        get parallel value from MPPForm
    """
    if key:
        form = dict_data.get(key)
        return form.__getitem__("parallel")


@register.filter("mpp_index_value")
def mpp_index_value(dict_data, key):
    """
        get mpp_index value from MPPForm
    """
    if key:
        form = dict_data.get(key)
        return form.__getitem__("index")
