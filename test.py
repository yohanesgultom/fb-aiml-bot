import ConfigParser
import aiml

k = aiml.Kernel()
k.learn('std-startup.xml')
k.respond('load aiml b')

config = ConfigParser.RawConfigParser()
config.read('config')

if config.has_section('botprofile'):
    for key, val in config.items('botprofile'):
        k.setBotPredicate(key, val)

while True:
    print k.respond(raw_input('> '))
