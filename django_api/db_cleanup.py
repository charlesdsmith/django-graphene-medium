# this module will periodically delete rows from the table


from oauth2_provider.management.commands.cleartokens import Command
from oauth2_provider.models import AccessToken
Command.handle()


