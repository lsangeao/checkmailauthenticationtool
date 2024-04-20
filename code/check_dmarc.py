import dns.resolver as dnsquery
import json


def query_dns(domain,selector=''):
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
    
r_domains=[]
r_domains.append(query_dns('uoc.com','mail'))
r_domains.append(query_dns('uned.es'))

print(json.dumps(r_domains, indent=4))

