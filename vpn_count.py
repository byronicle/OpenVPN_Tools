# Import regular expressions
import re

# Import sys module for taking in arguemnts to program
import sys

# Import pygal for graphing statistics
import pygal


# Print count of VPN logins by sorted username
def print_login_counts(filename):
    logins = vpn_logins(filename)

    for key in sorted(logins.keys()):
        print key, logins[key]

# Print count of VPN logins sorted by most logins by username
# and create gprah of logins
def print_top_counts(filename):
    logins = vpn_logins(filename)

    top_vpn_logins = sorted(logins, key=logins.get, reverse=True)

    line_chart = pygal.HorizontalBar()

    for login in top_vpn_logins:
        line_chart.add(login, logins[login])
        print login, logins[login]

    line_chart.render_to_file('OpenVPN_Logins.svg')

# Print top 10 most VPN logins by username and make graph
def print_top_10(filename):

    # Gather all the logins by username
    print "Gathering all logins by username..."
    logins = vpn_logins(filename)

    # Sort dictionary of logins by value using .get
    print "Processing logins and sorting..."
    top_vpn_logins = sorted(logins, key=logins.get, reverse=True)

    # Line chart object for graphing
    line_chart = pygal.HorizontalBar()
    line_chart.title = "Top 10 OpenVPN Users"
    line_chart.x_title = "Number of logins"

    # Print only the top 10 logins and add to chart

    print "\nTop 10 VPN Logins\n"
    for login in top_vpn_logins[:10]:
        line_chart.add(login, logins[login])
        print login, logins[login]

    print "\nSaving Top 10 Logins chart to file OpenVPN_Logins_Top10.svg"

    line_chart.render_to_file('OpenVPN_Logins_Top10.svg')

# Function to read OpenVPN.log and return dictionary of usernames and login
# count
def vpn_logins(filename):
    f = open(filename, 'rU')

    vpn_logins = {}

    for line in f:
        login = re.search(r'TLS: Username\/Password authentication succeeded for username \'(\w+)\'', line, re.M|re.I)
        if login:
            vpn_logins[login.group(1)] = vpn_logins.get(login.group(1),0) + 1

    f.close()

    return vpn_logins

def tls_key_error(filename):
    f = open(filename, 'rU')

    print "Looking for TLS Key errors..."

    tls_key_errors = []
    for line in f:
        error = re.search(r'(TLS keys are out of sync:)', line, re.M|re.I)
        if error:
            tls_key_errors.append(line)


    print "Compiling a list of who has had TLS key errors..."
    tls_key_error_usernames = []
    for line in tls_key_errors:
        username = re.search(r'\d\s(\w+)\/\d', line, re.M|re.I)
        if username and username.group(1) not in tls_key_error_usernames:
            tls_key_error_usernames.append(username.group(1))

    print "The %s people have had TLS key errors" % (len(tls_key_error_usernames))

    for username in tls_key_error_usernames:
        print username


    f.close()

def vpn_logins_by_month(filename):
    vpn_logins_list = successful_logins(filename)

    months = [
        'Jan',
        'Feb',
        'Mar',
        'Apr',
        'Jun',
        'Jul',
        'Aug',
        'Sep',
        'Oct',
        'Nov',
        'Dec',
            ]

    logins_by_month = {}
    regex = r'Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec'
    for line in vpn_logins_list:
        login = re.search(regex, line, re.M)
        if login:
            logins_by_month[login.group()] = logins_by_month.get(login.group(),0) + 1

    month_chart = pygal.HorizontalBar()
    month_chart.title = "VPN Login Count by Month"
    month_chart.x_title = "Logins"

    for month in months:
        month_chart.add(month, logins_by_month.get(month, 0))
        print month, logins_by_month.get(month, 0)

    month_chart.render_to_file('OpenVPN_Logins_by_Month.svg')


def successful_logins(filename):
    f = open(filename, 'rU')

    vpn_logins = []
    for line in f:
        login = re.search(r'(TLS: Username\/Password authentication succeeded for username)', line, re.M|re.I)
        if login and login not in vpn_logins:
            vpn_logins.append(line)

    f.close()

    return vpn_logins


# This basic command line argument parsing code is provided and
# calls the functions
def main():
  if len(sys.argv) != 3:
    print 'usage: ./vpn_count.py {--login_counts | --top_counts | --top_10 | --tls_key_error | --vpn_logins_by_month} file'
    sys.exit(1)

  option = sys.argv[1]
  filename = sys.argv[2]
  if option == '--login_counts':
      print_login_counts(filename)
  elif option == '--top_counts':
      print_top_counts(filename)
  elif option == '--top_10':
      print_top_10(filename)
  elif option == '--tls_key_error':
      tls_key_error(filename)
  elif option == '--vpn_logins_by_month':
      vpn_logins_by_month(filename)

  else:
    print 'unknown option: ' + option
    sys.exit(1)

if __name__ == '__main__':
  main()
