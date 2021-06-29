import binascii

# This script generates <span> tags for the few places in the guide that show binary data.
# Requires Python 3.

def print_title_code(title, code):
    print()
    print(title)
    print()
    print(code)

def format_binary(data_hex, width=24, indent=20, colorize=True):
    data = binascii.unhexlify(data_hex)
    out = ""

    for i in range(len(data)):
        if i % width == 0:
            out += " " * indent
        
        if colorize:
            out += "<span class=\"d{0}\">{1:02x}</span>".format(int(data[i] / 64), data[i])
        else:
            out += "<span>{0:02x}</span>".format(data[i])

        if (i + 1) % width == 0 and (i + 1) < len(data):
            out += "\n"

    return out

print_title_code("Network identifier", format_binary("d4a1cb88a66f02f8db635ce26441cc5dac1b08420ceaac230839b755845a9ffb", width=16, indent=16, colorize=False))
print_title_code("blobs.get: Box 1", format_binary("ffd8ffe000104a46494600010200000100010000ffdb004300080606070605080707070909080a0c140d0c0b0b0c1912130f141d1a1f1e1d1a1c1c20242e2720222c231c1c2837292c30313434341f27393d38323c2e333432ffdb"))
print_title_code("blobs.get: Box 2", format_binary("bae49231ce6874d0d4999e66b9f317ef2b20dc07a8ef8ad3b5b9330f349057a723a9f6359329b89252d2614918551d3eb4915bb2a12ce1467b77351ecac5f3dce8165b6907cf310de8d83519b58d1cc81f7311838c67f2ac291dc6"))
print_title_code("blobs.get: Box 3", format_binary("caf507ad376364afca7df3c558e48e07cbe9d68047f778f6a057220a36e08c1a79881438ede94ec83d074a70519c8345839885a25e31cd39536aae573dc7a54b9c1e339a724ac8b2051c483072074cfe94587cc3148eadd73e9438"))
print_title_code("blobs.getSlice", format_binary("bae49231ce6874d0d4999e66b9f317ef2b20dc07a8ef8ad3b5b9330f349057a723a9f6359329b89252d2614918551d3e"))
