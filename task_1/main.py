from regex import resolver_regex
from smc import resolver_smc
from gen import correct_generator
from gen import incorrect_generator


# irc://server2:25565/randomname?password
if __name__ == '__main__':
    # ts = resolver_smc.Resolver("irc://bMmFDVj798kQDheffp139xRX/WPNLYdqMkSLW")
    # ts.run()
    for i in range(1, 100000):
        s = incorrect_generator.get_string()
        # print(s)
        ts = resolver_smc.Resolver(s)
        if ts.run():
            print(s, end="")
        if resolver_regex.current_regex.match(s):
            print(s)