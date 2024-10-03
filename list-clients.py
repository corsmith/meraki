#!/usr/bin/env python3

import meraki, csv

# set the environment variable with your API key MERAKI_DASHBOARD_API_KEY
dashboard = meraki.DashboardAPI(print_console=False)

def getorgs(orgname=''):
    orgs = dashboard.organizations.getOrganizations()
    if orgname == '':
        return orgs
    else:
        return [ org for org in orgs if org['name'] == orgname ]

def getnetworks(orgid):
    return dashboard.organizations.getOrganizationNetworks(orgid, total_pages='all')

def getclients(netid):
    try:
        return dashboard.networks.getNetworkClients(netid, total_pages='all')
    except meraki.exceptions.APIError as error:
        if error.message['errors'][0] == 'Invalid device type':
            return []
        raise error

def writecsv(orgname, netname, clients):
    with open(f'clients-{orgname}_-_{netname}.csv', 'w', newline='') as csvfile:
        fieldnames = sorted(clients[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(clients)

for org in getorgs():
    print(org['name'])

    for network in getnetworks(org['id']):
        print('  ' + network['name'])
        clients = getclients(network['id'])
        if len(clients) > 0:
            writecsv(org['name'], network['name'], clients)


