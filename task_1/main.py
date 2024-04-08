from regex import resolver_regex
from smc import resolver_smc
from gen import correct_generator


# irc://server2:25565/randomname?password
if __name__ == '__main__':
    # ts = resolver_smc.Resolver("irc://bMmFDVj798kQDheffp139xRX/WPNLYdqMkSLW")
    # ts.run()
    for i in range(1, 100):
        s = correct_generator.get_string()
        # ts = resolver_smc.Resolver(s)
        # if not ts.run():
        #     print(s, end="")
        if not resolver_regex.current_regex.match(s):
            print(s)