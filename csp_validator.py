import requests
import json
import sys

def fetch_csp(url):
    print(f"\n🔄 Fetching GET request for URL: {url}")
    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException as e:
        print(f"❌ Error fetching URL {url}: {e}")
        return None
    
    if response.status_code == 200:
        print(f"✅ Request successful! Status code: {response.status_code}")
        print("\n🔍 Checking if 'Content-Security-Policy' header is present...\n")
        csp = response.headers.get('Content-Security-Policy')
        
        if csp:
            print(f"✅ 'Content-Security-Policy' found!\n")
            print(f"🔑 Original CSP:\n{csp}\n")
            
            csp_policies = {}
            for policy in csp.split(';'):
                directive, *sources = policy.strip().split(' ')
                csp_policies[directive] = sources
            
            print(f"✅ Conversion completed! Extracted structure:\n{json.dumps(csp_policies, indent=4)}\n")
            return csp_policies
        else:
            print("❌ 'Content-Security-Policy' not found in response header.")
            return None
    else:
        print(f"❌ Failed to fetch the URL. Status code: {response.status_code}")
        return None

def compare_domains(required_domain, csp_source):
    normalized_required = required_domain.replace('https://', '').replace('http://', '')
    normalized_csp = csp_source.replace('https://', '').replace('http://', '')
    return normalized_required in normalized_csp or normalized_csp in normalized_required

def validate_csp(csp_policies, required_domains):
    print("\n🔄 Starting validation of the provided directives and domains...\n")
    results = {}
    
    for directive, required_sources in required_domains.items():
        csp_sources = csp_policies.get(directive)
        if csp_sources:
            print(f"🔍 Checking directive '{directive}'...\n")
            missing_domains = []
            for required_domain in required_sources:
                if not any(compare_domains(required_domain, csp_source) for csp_source in csp_sources):
                    missing_domains.append(required_domain)

            if missing_domains:
                results[directive] = {
                    "status": "missing",
                    "missing": missing_domains
                }
                print(f"❌ Missing domains in '{directive}': {missing_domains}\n")
            else:
                results[directive] = {
                    "status": "passed",
                    "missing": []
                }
                print(f"✅ All domains in directive '{directive}' are present.\n")
        else:
            results[directive] = {
                "status": "absent",
                "missing": required_sources
            }
            print(f"❌ Directive '{directive}' is absent in the extracted CSP.\n")

    return results

def print_summary(url, results):
    print(f"📋 Summary of CSP Validation for {url}:")
    for directive, result in results.items():
        if result['status'] == 'passed':
            print(f"✅ '{directive}': All required domains are present.")
        elif result['status'] == 'missing':
            print(f"❌ '{directive}': Missing domains: {', '.join(result['missing'])}")
        elif result['status'] == 'absent':
            print(f"❌ '{directive}': Directive is absent in the extracted CSP.")
    print()

def main():
    if len(sys.argv) != 3:
        print("❌ Correct usage: python script.py <path_to_urls_json> <path_to_domains_json>")
        sys.exit(1)

    urls_file = sys.argv[1]
    domains_file = sys.argv[2]

    try:
        with open(urls_file, 'r') as f:
            urls = json.load(f)
        print(f"\n🔄 URLs JSON file loaded! URLs to process:\n{urls}\n")
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"❌ Error: Invalid URLs file '{urls_file}' or format is not JSON.")
        sys.exit(1)

    try:
        with open(domains_file, 'r') as f:
            required_domains = json.load(f)
        print(f"✅ Domains JSON file loaded successfully! Content:\n{json.dumps(required_domains, indent=4)}\n")
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"❌ Error: Invalid domains file '{domains_file}' or format is not JSON.")
        sys.exit(1)

    all_results = {}
    for url in urls:
        csp_policies = fetch_csp(url)
        if csp_policies:
            results = validate_csp(csp_policies, required_domains)
            print_summary(url, results)
            all_results[url] = results

    with open("results.json", 'w') as f:
        json.dump(all_results, f, indent=4)
    print("\n📂 All results saved to 'results.json'")

if __name__ == "__main__":
    main()
