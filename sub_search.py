import subprocess , optparse , sys, os

def Args():
    Parser = optparse.OptionParser()
    Parser.add_option("--d", "--domain", dest="domain", help="Main domain")
    Parser.add_option("--l", "--list", dest="list", help="list of the Sub-domains ")
    (arguments, values) = Parser.parse_args()
    return arguments
sRed , eRed = "\033[1;31m" , "\033[1;m"

subs = []
def sub_search(domain , list , level):
    try:
        with open(list, 'r') as sub:
            for subdomain in sub.read().splitlines():
                #host - DNS lookup utility | -t: the type > A dns Record
                hostCommand  = subprocess.run(["host -t A "+subdomain+"."+domain+"", ""], capture_output=True,shell=True).stdout.decode()
                #print(hostCommand) #debugging | to see all the dns lookup queries being sent
                if 'not found' not in hostCommand and domain in hostCommand: 
                    #Verbosity
                    print(hostCommand.rsplit()[0])
                    subs.append(hostCommand.rsplit()[0])
                else:
                    pass
    except FileNotFoundError:
        print("\n Sub-Domains list is Not Found \n")
           
    #Gitting into the next Level
    #len(subs[level:]) != 0 | here we're saying that since there are more sub-domains keep brute-forcing
    if len(subs[level:]) != 0:
        for next_sub in subs[level:]:
            return sub_search(next_sub , list , level+1)
    #Recursion Breaking Point
    #here we're saying that since there are no more sub-domains stop brute-forcing and print out the results
    else:
        print("\n\n"+sRed+"..| Final Results . Output saved in {}/output.txt |.. ".format(os.getcwd())+eRed)
        with open('output.txt','a+') as w:
            for _ in subs:
                print(_)
                w.write(_+"\n")
            w.close()
            quit()
            
        

def main():
    arguments = Args()
    if len(sys.argv) == 5:
        print("\n\n"+sRed+"..| Verbosity |.. "+eRed)
        sub_search(arguments.domain , arguments.list , 0)
    else:
        print("Usage python3 sub_rec --d logitech.com --l /root/tools/shubs-subdomains.txt")
    quit()

if __name__ == '__main__':
    main()
