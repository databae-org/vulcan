import csv, json, os, requests
from BeautifulSoup import BeautifulSoup

import trump_emailer

h2a_url = 'https://lcr-pjr.doleta.gov/index.cfm?event=ehLCJRExternal.dspAdvJobOrderSearchGridData&&startSearch=1&case_number=&employer_business_name=trump&visa_class_id=8&status_id=All&state_id=all&location_range=10&location_zipcode=&job_title=&crop_id=&start_date_from=mm/dd/yyyy&start_date_to=mm/dd/yyyy&create_date=mm/dd/yyyy&post_end_date=mm/dd/yyyy&naic_code=&soc_code_id=&nd=1487348162229&page=1&rows=10&sidx=create_date&sord=desc&nd=1487348162232&_search=false'

# H-2A search for 'Trump'
r = requests.get(h2a_url)
r.raise_for_status()
h2a_json = json.loads(r.text)
h2a_data = h2a_json['ROWS']
h2a_outfile = open('data/h2a_data_new.csv', 'w')
csvwriter = csv.writer(h2a_outfile)
for h2a in h2a_data:
    csvwriter.writerow(h2a)

h2a_outfile.close()

with open('data/h2a_data.csv', 'rb') as h2a_csv:
    with open('data/h2a_data_new.csv', 'rb') as h2a_csv_new:
        reader1 = csv.reader(h2a_csv)
        reader2 = csv.reader(h2a_csv_new)
        rows1_col_a = [row[0] for row in reader1]
        rows2 = [row for row in reader2]
        only_b = []
        for row in rows2:
            if row[0] not in rows1_col_a:
                only_b.append(row)

if only_b:
    to_send = open('data/h2aupdates.csv', 'w')
    csvwriter2 = csv.writer(to_send)
    for data in only_b:
        csvwriter2.writerow(data)
    to_send.close()

    with open('data/h2aupdates.csv', 'rb') as send_file:
        reader = csv.reader(send_file)
        for row in reader:
            link = row[0]
            h2a_email = trump_emailer.Email(to=conflicts, subject='Trump H-2A alert')
            h2a_email.text('Howdy team,\n\nI think a Trump Organization business may be seeking to hire foreign laborers through the H-2A visa program. Here is the link on DOL\'s site to the Job Order Record: https://lcr-pjr.doleta.gov/index.cfm?event=ehLCJRExternal.dspJobOrderView&frm=PJR&task=view_job_order&view=external&lcjr_id=' + str(link) + '\n\nI hope this is helpful,\n\nRobot Steven Rich')
            h2a_email.html('<html><body>Howdy team,\n\nI think a Trump Organization business may be seeking to hire foreign laborers through the H-2A visa program. Here is the link on DOL\'s site to the Job Order Record: https://lcr-pjr.doleta.gov/index.cfm?event=ehLCJRExternal.dspJobOrderView&frm=PJR&task=view_job_order&view=external&lcjr_id=' + str(link) + '\n\nI hope this is helpful,\n\nRobot Steven Rich</body></html>')
            h2a_email.send()

os.rename('data/h2a_data_new.csv', 'data/h2a_data.csv')
