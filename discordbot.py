import discord
import re
import numpy as np

TOKEN = ''

class MyClient(discord.Client):
  async def on_ready(self):
      print('Logged in as')
      print(self.user.name)
      print(self.user.id)
      print('------')

  async def on_message(self, message):
      if message.author.bot:
          return

      if re.match(r'/dice .*', message.content):  
        content = message.content.replace('/dice ', '')
        splitPlus = content.split('+')
        formatedContent = content.replace(' ', '').replace('+', ' + ')
        reply = message.author
        
        response = formatedContent + ": "

        result = 0
        for (i, context) in enumerate(splitPlus):
          splited = context.split('d')

          if len(splited) == 1:
            result = result + int(splited[0])
            response = response + splited[0]
          else:
            for dice in range(int(splited[0])):
              res = np.random.randint(1, splited[1])
              result = result + res
              response = response + str(res)

              # ダイスが1個以上の時
              if not (int(splited[0]) == 1):
                # 最後のダイスじゃない時
                if not ((dice == (int(splited[0]) - 1))):            
                  response = response + " + "
                # 最後のダイスかつ、ダイスセットが１つだけの時
                elif (dice == int(splited[0]) - 1) and (len(splitPlus) == 1):
                  response = response + " = " + str(result)

          # ダイスセットが1個以上の時
          if not (len(splitPlus) == 1):
            # 最後のダイスセットじゃない時
            if not (i == (len(splitPlus) - 1)):
              response = response + " + "
            # 最後のダイスセットの時
            elif (i == len(splitPlus) - 1):
              response = response + " = " + str(result)

        await message.reply(response, mention_author=True)

client = MyClient()
client.run(TOKEN)