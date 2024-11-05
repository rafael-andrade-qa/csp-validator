import json

def parse_csp(csp_string):
    csp_dict = {}

    directives = csp_string.strip().split(';')

    print("\n🚀 Starting CSP parsing process...\n")

    for directive in directives:
        directive = directive.strip()
        if not directive:
            continue
        
        name, *values = directive.split()
        if values:
            csp_dict[name] = values
            print(f"✅ Directive '{name}' added with {len(values)} values.")

    print("\n🎉 CSP parsing completed!")
    return csp_dict

def save_csp_to_json(csp_dict, filename="domains.json"):
    with open(filename, 'w') as json_file:
        json.dump(csp_dict, json_file, indent=4)
    print(f"\n📂 File '{filename}' successfully created with JSON structure!\n")

print("👋 Please enter the Content Security Policy (CSP) string below:\n")
csp_string = input("🔑 CSP: ")

csp_dict = parse_csp(csp_string)

save_csp_to_json(csp_dict)

print("✅ Process complete. The JSON file is ready to use!")
