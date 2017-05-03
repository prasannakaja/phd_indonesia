import re
import sys
import optparse
import csv
import urllib.request as urequest
import urllib.parse

class PizzahutIndonesia:
    def __init__(self, infile, csvfile):
        self.latlong_file = infile
        self.URL = "https://order.phd.co.id/en/frontend/pizza/getListOutlet"

        self.POST_DATA = {"limit": "99999999",
                          "start": "0",
                          "gpsLat": "",
                          "gpsLong": ""
                        }
        self.cookie = "phid_session=a%3A4%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22a408de44e7f8ce2e45b22759f19cfc95%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A12%3A%22172.31.1.133%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A120%3A%22Mozilla%2F5.0+%28Macintosh%3B+Intel+Mac+OS+X+10_11_6%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F57.0.2987.133+Safari%2F537.3%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1493175646%3B%7D11882d71f0cc2a570f89dd043de97cbc; _ga=GA1.3.1498102103.1489551641; _gat=1; _gat_clientTracker=1"

        ## OUTPUT CSV FILE
        if ".csv" not in csvfile:
            self.csvfile_name = csvfile+".csv"
        else: self.csvfile_name = csvfile

    def write_into_csv(self, outlet_details_list=[], mode='w'):
        """
            WRITE OUTLETS DATA INTO CSV FILE.
        """
        with open(self.csvfile_name, mode, newline='') as csvfile:
            locwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
            for loc in outlet_details_list:
                locwriter.writerow(loc)

    def read_latlongs(self):
        """
            READ LAT-LONG DATA FROM INPUT FILE.
        """
        lat_longs = [str(i.strip()) for i in open(self.latlong_file).readlines() if i.strip()]
        return lat_longs
    
    def process_response_data(self, response):
        """
            GET OUTLETS DATA.
        """
        outlets_list = []
       
        response_data = response.replace('true', '"true"')
        response_data = eval(response_data)

        outlets = response_data["data"]["outlet"]["items"]
        
        for outlet in outlets:
            outlets_list.append([outlet["OutletID"], outlet["OutletName"], outlet["Description"],
                    outlet["OpeningHours"], outlet["Location"], outlet["ImageSource"], outlet["Lat"], 
                    outlet["Long"], outlet["ContactNumber"]])
        return outlets_list

    def scrape_data(self):
        """
            SCRAPE OUTLETS DATA
        """
        #OPEN EMPTY CSV FILE
        self.write_into_csv()

        #READ LATLONGS
        lat_longs = self.read_latlongs()
        for latlong in lat_longs:
            latitude = latlong.split('::')[0].strip()
            longitude = latlong.split('::')[-1].strip()
            self.POST_DATA["gpsLat"] = latitude
            self.POST_DATA["gpsLong"] = longitude
            
            post_data = urllib.parse.urlencode(self.POST_DATA)
            post_data = post_data.encode('utf-8')
            post_url = urequest.Request(self.URL, post_data)
            post_url.add_header("Host", "order.phd.co.id")
            post_url.add_header("Referer", "https://order.phd.co.id/en/home")
            post_url.add_header("Cookie", self.cookie)
        
            response_data = urequest.urlopen(post_url).read().decode('utf8')
                    
            outlets = self.process_response_data(response_data)

            ## WRITE OUTLETS DATA INTO CSV FILE
            self.write_into_csv(outlets, mode='a')


def main(options): 
    """
        MAIN 
    """
    input_file = options.input_file
    output_filename = options.out_file

    if input_file and output_filename:
        phdObj = PizzahutIndonesia(input_file, output_filename)
        phdObj.scrape_data()

    else:
        print(""" Please provide "postcodes text file"  and  
                    "csv file name" to which you want to write output. 

                    script usage is below:

                 python <sciptname> -i<lat-long file> -o<name for csv file> 
        """)
        sys.exit(1)
        

if __name__=='__main__':
  
    usage = "usage: program.py -i <lat-longs file name> -o <desired csv filename>" 
    parser = optparse.OptionParser(usage=usage) 
    
    parser.add_option('-i', '--input-file',  help="Please provide latlongs.txt file")
    parser.add_option('-o', '--out-file',  help="OUTPUT Filename/provide csv file name")

    (options, args) = parser.parse_args()

    main(options)
 

