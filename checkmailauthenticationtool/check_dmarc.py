import dns.resolver as dnsquery
import json
import csv
import sys




def write_results(results):
    # Save current results to csv file
    with open('current_results.csv', 'w') as f:
        f.write('domain,dmarc,spf,dkim\n')
        for e in results:
            domain=e['domain']
            dmarc= e['dmarc'][1]
            spf= e['spf'][1]
            dkim= e['dkim'][1]
            f.write(f"{domain},{dmarc},{spf},{dkim}\n")
    # Save current results to json file
    with open('current_results.json', 'w') as f:
        json.dump(results, f, indent=4)

def read_csv(file_path):
    """
    Reads a CSV file and returns its contents as a dictionary.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        dict: A dictionary containing the contents of the CSV file.
    """
    data = {}
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    return data

def query_dns(domain,selector=''):
    """
    Queries DNS records for a given domain and returns information about DMARC, SPF, and DKIM records.

    Args:
        domain (str): The domain to query DNS records for.
        selector (str, optional): The DKIM selector (if applicable). Defaults to ''.

    Returns:
        dict: A dictionary containing the following information:
            - 'domain': The queried domain.
            - 'dmarc': A list with the count of DMARC records found and a comma-separated string of DMARC records.
            - 'spf': A list with the count of SPF records found and a comma-separated string of SPF records.
            - 'dkim': A list with the count of DKIM records found and a comma-separated string of DKIM records.
    """
    try:
        dmarc = [ str(x).split('"')[1] for x in dnsquery.resolve('_dmarc.' + domain , 'TXT').rrset if 'v=DMARC1' in str(x)]

    except:
        dmarc=[f'Unable to get DMARC record for "{domain}"']
    try:
        spf = [str(x).split('"')[1]  for x in dnsquery.resolve(domain , 'TXT').rrset if 'v=spf1' in str(x)] 
    except:
        spf=[f'Unable to get SPF record for "{domain}"']
    
    try:   
        dkim = [str(x).split('"')[1]  for x in dnsquery.resolve(selector + '._domainkey.' + domain , 'TXT').rrset if 'v=DKIM1' in str(x)]     
    except:
        dkim=[f'Unable to get DKIM record for "{domain}" with selector "{selector}"']
    
    
    result={
        "domain": domain,
        "dmarc": [len(dmarc), ','.join(dmarc)],
        "spf":   [len(spf), ','.join(spf)],
        "dkim":  [len(dkim), ','.join(dkim)]
        
    }
    
    return(result)
    
def compare_dicts(dict1, dict2):
    diff = {}
    for key in dict1.keys() | dict2.keys():
        domain=dict1.get("domain")
        if dict1.get(key) != dict2.get(key):
            diff[f"The domain {domain} has changes in {key} record"] = {'Current': dict1.get(key), 'Previous': dict2.get(key)}
    return diff

def main(args=sys.argv):
    # Parse command-line arguments
    f_domains=args[0]
    p_domains=args[1]

    # Initialize variables
    results=[]
    mail_results=[]
    
    # Read Domains from CSV file
    domains=read_csv(f_domains) 
    
    # Load previous results
    with open( p_domains) as f:
        previous_results = json.loads(f.read())
    
    # Query DNS records for each domain     
    
    for domain in domains:
        c_domain_result=query_dns(domain["domain"],domain["selector"])
        results.append(c_domain_result)
        p_domain_result = [e for e in previous_results if e["domain"]==domain["domain"]]
        diff=compare_dicts(c_domain_result,p_domain_result[0])
        if len(diff)>0:
            mail_results.append(diff)


    # Save results
    write_results(results)        

    # Prettyfy mail_results 
    strtext=""
    
    for element in mail_results:
        key=list(element.keys())[0]
        data=element[key]
        strtext+=f"{key}:"
        strtext+=f"\n\tPrevious: {data['Previous'][1]}"
        strtext+=f"\n\tCurrent: {data['Current'][1]}\n\n"
    
    
    if len(strtext) == 0:
        strtext = "There are no changes"
    
    with open('output.txt','w') as f:
        f.write(strtext)

    exit()

